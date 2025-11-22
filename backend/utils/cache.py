"""
Simple in-memory cache for API responses with TTL-based expiration.
Reduces redundant API calls and improves data availability.
"""
from datetime import datetime, timedelta
from typing import Any, Optional
import hashlib
import json


class SimpleCache:
    """In-memory cache with TTL support."""
    
    def __init__(self, ttl_seconds: int = 3600):
        self.cache = {}
        self.ttl_seconds = ttl_seconds
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from function arguments."""
        key_data = {
            'args': args,
            'kwargs': kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if exists and not expired."""
        if key not in self.cache:
            return None
        
        value, expiry = self.cache[key]
        
        if datetime.now() > expiry:
            # Expired, remove from cache
            del self.cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache with TTL."""
        expiry = datetime.now() + timedelta(seconds=self.ttl_seconds)
        self.cache[key] = (value, expiry)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()


# Global cache instance
cache = SimpleCache(ttl_seconds=3600)
