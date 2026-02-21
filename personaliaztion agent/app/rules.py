from typing import Tuple, List, Optional
from app.logger import setup_logger

logger = setup_logger(__name__)


def apply_rules(user, stats, option: dict) -> Tuple[float, List[str]]:
    """
    Apply business rules to score an option
    
    Args:
        user: User profile object
        stats: Booking stats object (can be None)
        option: Option dictionary
        
    Returns:
        Tuple of (score, list of reasons)
    """
    score = 0.0
    reasons = []
    
    try:
        # Rule 1: High cancellation rate + refundable option
        if stats and hasattr(stats, 'cancellation_rate'):
            if stats.cancellation_rate > 0.3 and option.get("refundable", False):
                score += 0.2
                reasons.append("Prefers refundable options")
                logger.debug(f"Applied refundable rule: +0.2")
        
        # Rule 2: Budget preference match
        if hasattr(user, 'budget_pref') and user.budget_pref == option.get("price_bucket"):
            score += 0.15
            reasons.append("Matches budget preference")
            logger.debug(f"Applied budget rule: +0.15")
        
        # Rule 3: Preferred supplier
        if hasattr(user, 'preferred_suppliers') and option.get("supplier_id"):
            if option["supplier_id"] in user.preferred_suppliers:
                score += 0.25
                reasons.append("Preferred supplier")
                logger.debug(f"Applied supplier rule: +0.25")
        
        # Rule 4: High rating preference
        if hasattr(user, 'refund_pref'):
            if user.refund_pref == 'high' and option.get('rating_bucket') == 'high':
                score += 0.1
                reasons.append("High rating match")
                logger.debug(f"Applied rating rule: +0.1")
        
        # Rule 5: Conversion rate optimization
        if stats and hasattr(stats, 'conversion_rate'):
            if stats.conversion_rate < 0.1 and option.get('price_bucket') == 'low':
                score += 0.15
                reasons.append("Price-optimized for conversion")
                logger.debug(f"Applied conversion rule: +0.15")
        
    except Exception as e:
        logger.error(f"Error applying rules: {str(e)}")
        # Return partial results if any rules failed
    
    return score, reasons
