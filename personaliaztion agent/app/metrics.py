from typing import Dict, Any
from datetime import datetime
from collections import defaultdict
import threading
from app.logger import setup_logger

logger = setup_logger(__name__)


class MetricsCollector:
    """Simple in-memory metrics collector for monitoring"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.reset()
    
    def reset(self):
        """Reset all metrics"""
        with self._lock:
            self.request_count = 0
            self.error_count = 0
            self.total_latency = 0.0
            self.ml_score_count = 0
            self.rule_score_count = 0
            self.cache_hits = 0
            self.cache_misses = 0
            self.options_scored = 0
            self.start_time = datetime.utcnow()
    
    def record_request(self, latency: float):
        """Record a successful request"""
        with self._lock:
            self.request_count += 1
            self.total_latency += latency
    
    def record_error(self):
        """Record an error"""
        with self._lock:
            self.error_count += 1
    
    def record_ml_score(self):
        """Record ML scoring"""
        with self._lock:
            self.ml_score_count += 1
    
    def record_rule_score(self):
        """Record rule-based scoring"""
        with self._lock:
            self.rule_score_count += 1
    
    def record_cache_hit(self):
        """Record cache hit"""
        with self._lock:
            self.cache_hits += 1
    
    def record_cache_miss(self):
        """Record cache miss"""
        with self._lock:
            self.cache_misses += 1
    
    def record_options_scored(self, count: int):
        """Record number of options scored"""
        with self._lock:
            self.options_scored += count
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot"""
        with self._lock:
            uptime = (datetime.utcnow() - self.start_time).total_seconds()
            avg_latency = (
                self.total_latency / self.request_count 
                if self.request_count > 0 
                else 0
            )
            cache_hit_rate = (
                self.cache_hits / (self.cache_hits + self.cache_misses)
                if (self.cache_hits + self.cache_misses) > 0
                else 0
            )
            error_rate = (
                self.error_count / self.request_count
                if self.request_count > 0
                else 0
            )
            
            return {
                "uptime_seconds": round(uptime, 2),
                "total_requests": self.request_count,
                "total_errors": self.error_count,
                "error_rate": round(error_rate, 4),
                "avg_latency_seconds": round(avg_latency, 4),
                "ml_scores": self.ml_score_count,
                "rule_scores": self.rule_score_count,
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "cache_hit_rate": round(cache_hit_rate, 4),
                "options_scored": self.options_scored,
                "requests_per_second": round(
                    self.request_count / uptime if uptime > 0 else 0,
                    2
                )
            }


# Global metrics collector instance
metrics = MetricsCollector()
