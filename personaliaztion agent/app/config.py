from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str
    
    # Application
    app_name: str = "Personalization Agent"
    debug: bool = False
    log_level: str = "INFO"
    
    # ML Model
    model_path: str = "model.joblib"
    min_training_samples: int = 100
    model_fallback_score: float = 0.0
    
    # Scoring weights
    rule_weight: float = 1.0
    ml_weight: float = 1.0
    
    # Cache settings
    cache_ttl: int = 300  # 5 minutes
    
    # Performance
    batch_size: int = 100
    max_options_per_request: int = 100
    
    # Feature flags
    enable_ml_scoring: bool = True
    enable_caching: bool = True
    enable_metrics: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
