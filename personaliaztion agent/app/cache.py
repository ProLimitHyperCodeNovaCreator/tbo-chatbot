from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.config import settings
from app.logger import setup_logger

logger = setup_logger(__name__)


class SimpleCache:
    """Simple in-memory cache with TTL support"""
    def __init__(self, ttl: int = settings.cache_ttl):
        self.cache: Dict[str, tuple[Any, datetime]] = {}
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.utcnow() - timestamp < timedelta(seconds=self.ttl):
                logger.debug(f"Cache hit for key: {key}")
                return value
            else:
                logger.debug(f"Cache expired for key: {key}")
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache with current timestamp"""
        self.cache[key] = (value, datetime.utcnow())
        logger.debug(f"Cache set for key: {key}")
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def remove(self, key: str) -> None:
        """Remove specific key from cache"""
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache removed for key: {key}")


# Global cache instance
cache = SimpleCache()
