"""
Configuration for testing without database
"""

class MockSettings:
    """Mock settings that work without environment variables"""
    
    # Database (not used in mock mode)
    database_url: str = "mock://localhost"
    
    # Application
    app_name: str = "Personalization Agent (Mock Mode)"
    debug: bool = True
    log_level: str = "INFO"
    
    # ML Model
    model_path: str = "model.joblib"
    min_training_samples: int = 100
    model_fallback_score: float = 0.0
    
    # Scoring weights
    rule_weight: float = 1.0
    ml_weight: float = 1.0
    
    # Cache settings
    cache_ttl: int = 300
    
    # Performance
    batch_size: int = 100
    max_options_per_request: int = 100
    
    # Feature flags
    enable_ml_scoring: bool = True
    enable_caching: bool = True
    enable_metrics: bool = True


settings = MockSettings()
