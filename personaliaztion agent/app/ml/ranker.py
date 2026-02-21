import joblib
import numpy as np
from pathlib import Path
from typing import Optional
from app.features import featurize
from app.config import settings
from app.logger import setup_logger

logger = setup_logger(__name__)


class MLRanker:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or settings.model_path
        self.model = None
        self.is_available = False
        self._load_model()
    
    def _load_model(self):
        """Load ML model with error handling"""
        try:
            if Path(self.model_path).exists():
                self.model = joblib.load(self.model_path)
                self.is_available = True
                logger.info(f"ML model loaded successfully from {self.model_path}")
            else:
                logger.warning(f"ML model not found at {self.model_path}. Using fallback scoring.")
                self.is_available = False
        except Exception as e:
            logger.error(f"Error loading ML model: {str(e)}")
            self.is_available = False
    
    def reload_model(self):
        """Reload the model (useful after retraining)"""
        logger.info("Reloading ML model...")
        self._load_model()
    
    def score(self, opt: dict) -> float:
        """
        Score an option using ML model or fallback
        
        Args:
            opt: Option dictionary with features
            
        Returns:
            float: ML score (0-1 range typically)
        """
        if not settings.enable_ml_scoring or not self.is_available:
            logger.debug("ML scoring disabled or model unavailable, using fallback")
            return settings.model_fallback_score
        
        try:
            x = featurize(opt).reshape(1, -1)
            score = float(self.model.predict_proba(x)[0][1])
            logger.debug(f"ML score for option {opt.get('option_id', 'unknown')}: {score:.4f}")
            return score
        except Exception as e:
            logger.error(f"Error scoring option: {str(e)}")
            return settings.model_fallback_score
