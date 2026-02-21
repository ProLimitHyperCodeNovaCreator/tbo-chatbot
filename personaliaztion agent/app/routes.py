from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from datetime import datetime
from app.model import PersonalizeRequest, Option
from app.db import db
from app.rules import apply_rules
from app.ml.ranker import MLRanker
from app.ml.trainer import train_model
from app.cache import cache
from app.config import settings
from app.logger import setup_logger
from app.metrics import metrics
from app.exceptions import (
    user_not_found_exception,
    invalid_request_exception,
    internal_error_exception
)

logger = setup_logger(__name__)
router = APIRouter()

# Initialize ranker globally
ranker = None


def get_ranker() -> MLRanker:
    """Get or initialize the ML ranker"""
    global ranker
    if ranker is None:
        ranker = MLRanker()
    return ranker


@router.post("/personalize")
async def personalize(req: PersonalizeRequest):
    """
    Personalize and rank options for a user
    
    Returns ranked list of options with scores and explanations
    """
    try:
        logger.info(f"Personalizing {len(req.options)} options for user {req.user_id}")
        
        # Validate request
        if len(req.options) > settings.max_options_per_request:
            raise invalid_request_exception(
                f"Too many options. Maximum allowed: {settings.max_options_per_request}"
            )
        
        if not req.options:
            raise invalid_request_exception("No options provided")
        
        # Try to get user from cache
        cache_key = f"user:{req.user_id}"
        user = None
        
        if settings.enable_caching:
            user = cache.get(cache_key)
        
        # Fetch user profile if not cached
        if user is None:
            user = await db.user_profile.find_unique(where={"user_id": req.user_id})
            if user is None:
                logger.warning(f"User not found: {req.user_id}")
                raise user_not_found_exception(req.user_id)
            
            if settings.enable_caching:
                cache.set(cache_key, user)
                metrics.record_cache_miss()
        else:
            logger.debug(f"User loaded from cache: {req.user_id}")
            metrics.record_cache_hit()
        
        # Fetch booking stats (with caching)
        stats = None
        stats_cache_key = f"stats:{user.agency_id}"
        
        if settings.enable_caching:
            stats = cache.get(stats_cache_key)
        
        if stats is None:
            stats = await db.booking_stats.find_unique(
                where={"agency_id": user.agency_id}
            )
            if stats and settings.enable_caching:
                cache.set(stats_cache_key, stats)
                metrics.record_cache_miss()
        else:
            metrics.record_cache_hit()
        
        # Get ML ranker
        ml_ranker = get_ranker()
        
        # Score each option
        results = []
        scored_options = []
        
        for opt in req.options:
            try:
                opt_dict = opt.dict()
                
                # Apply rules
                rule_score, reasons = apply_rules(user, stats, opt_dict)
                metrics.record_rule_score()
                
                # Get ML score
                ml_score = ml_ranker.score(opt_dict) if settings.enable_ml_scoring else 0.0
                if settings.enable_ml_scoring:
                    metrics.record_ml_score()
                
                # Calculate final score
                final_score = (
                    opt.base_score + 
                    (rule_score * settings.rule_weight) + 
                    (ml_score * settings.ml_weight)
                )
                
                result = {
                    "option_id": opt.option_id,
                    "final_score": round(final_score, 4),
                    "base_score": opt.base_score,
                    "rule_score": round(rule_score, 4),
                    "ml_score": round(ml_score, 4),
                    "reasons": reasons
                }
                
                results.append(result)
                scored_options.append({
                    "user_id": req.user_id,
                    "option_id": opt.option_id,
                    "final_score": final_score,
                    "reasons": reasons
                })
                
            except Exception as e:
                logger.error(f"Error scoring option {opt.option_id}: {str(e)}")
                # Continue with other options
                continue
        
        # Sort by final score
        results.sort(key=lambda x: x["final_score"], reverse=True)
        
        # Batch insert/update personalization scores
        try:
            for scored_opt in scored_options:
                await db.personalization_scores.upsert(
                    where={
                        "user_id_option_id": {
                            "user_id": scored_opt["user_id"],
                            "option_id": scored_opt["option_id"]
                        }
                    },
                    data={
                        "create": {
                            "user_id": scored_opt["user_id"],
                            "option_id": scored_opt["option_id"],
                            "final_score": scored_opt["final_score"],
                            "reasons": scored_opt["reasons"],
                            "updated_at": datetime.utcnow()
                        },
                        "update": {
                            "final_score": scored_opt["final_score"],
                            "reasons": scored_opt["reasons"],
                            "updated_at": datetime.utcnow()
                        }
                    }
                )
        except Exception as e:
            # Log but don't fail the request
            logger.error(f"Error saving personalization scores: {str(e)}")
        
        logger.info(f"Successfully personalized {len(results)} options for user {req.user_id}")
        
        # Record metrics
        metrics.record_options_scored(len(results))
        
        return {
            "user_id": req.user_id,
            "total_options": len(results),
            "ranked_options": results,
            "ml_available": ml_ranker.is_available
        }
        
    except HTTPException:
        metrics.record_error()
        raise
    except Exception as e:
        metrics.record_error()
        logger.error(f"Unexpected error in personalize: {str(e)}", exc_info=True)
        raise internal_error_exception(str(e))


@router.post("/feedback")
async def record_feedback(
    user_id: str,
    option_id: str,
    accepted: bool,
    price_bucket: str,
    distance_bucket: str,
    rating_bucket: str,
    supplier_id: str,
    refundable: bool
):
    """
    Record user feedback for training
    
    Creates a training event that can be used to retrain the model
    """
    try:
        logger.info(f"Recording feedback for user {user_id}, option {option_id}")
        
        training_event = await db.training_events.create(
            data={
                "user_id": user_id,
                "option_id": option_id,
                "price_bucket": price_bucket,
                "distance_bucket": distance_bucket,
                "rating_bucket": rating_bucket,
                "supplier_id": supplier_id,
                "refundable": refundable,
                "accepted": accepted,
                "created_at": datetime.utcnow()
            }
        )
        
        logger.info(f"Feedback recorded: {training_event.event_id}")
        
        return {
            "status": "success",
            "event_id": training_event.event_id,
            "message": "Feedback recorded successfully"
        }
        
    except Exception as e:
        logger.error(f"Error recording feedback: {str(e)}", exc_info=True)
        raise internal_error_exception("Failed to record feedback")


@router.post("/train")
async def trigger_training(background_tasks: BackgroundTasks):
    """
    Trigger model retraining
    
    Runs training in background and reloads the model when complete
    """
    try:
        logger.info("Triggering model training")
        
        async def train_and_reload():
            metrics = await train_model()
            if metrics:
                # Reload the model
                global ranker
                if ranker:
                    ranker.reload_model()
                logger.info("Model retrained and reloaded successfully")
        
        background_tasks.add_task(train_and_reload)
        
        return {
            "status": "training_started",
            "message": "Model training initiated in background"
        }
        
    except Exception as e:
        logger.error(f"Error triggering training: {str(e)}", exc_info=True)
        raise internal_error_exception("Failed to trigger training")


@router.post("/cache/clear")
async def clear_cache():
    """Clear the application cache"""
    try:
        cache.clear()
        return {"status": "success", "message": "Cache cleared"}
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise internal_error_exception("Failed to clear cache")


@router.get("/model/status")
async def model_status():
    """Get ML model status"""
    ml_ranker = get_ranker()
    return {
        "model_available": ml_ranker.is_available,
        "model_path": ml_ranker.model_path,
        "ml_scoring_enabled": settings.enable_ml_scoring
    }


@router.get("/metrics")
async def get_metrics():
    """Get application metrics"""
    return metrics.get_metrics()


@router.post("/metrics/reset")
async def reset_metrics():
    """Reset metrics counters"""
    try:
        metrics.reset()
        return {"status": "success", "message": "Metrics reset"}
    except Exception as e:
        logger.error(f"Error resetting metrics: {str(e)}")
        raise internal_error_exception("Failed to reset metrics")
