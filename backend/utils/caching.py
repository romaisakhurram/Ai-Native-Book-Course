"""
Caching utilities for performance optimization
"""
from typing import Any, Optional
import asyncio
from functools import wraps
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        """Connect to Redis if available, otherwise use in-memory cache"""
        try:
            import redis.asyncio as redis_lib
            self.redis = await redis_lib.Redis.from_url(self.redis_url, decode_responses=True)
            logger.info("Connected to Redis cache")
        except ImportError:
            logger.warning("Redis not available, using in-memory cache")
            self.redis = None  # Will use in-memory solution
        except Exception as e:
            logger.error(f"Could not connect to Redis cache: {e}")
            self.redis = None  # Fallback to in-memory solution

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache"""
        if not self.redis:
            return None
            
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    async def set(self, key: str, value: Any, expire: int = 3600):
        """Set a value in cache"""
        if not self.redis:
            return
            
        try:
            json_value = json.dumps(value, default=str)
            await self.redis.setex(key, expire, json_value)
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    async def delete(self, key: str):
        """Delete a value from cache"""
        if not self.redis:
            return
            
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")

# Global cache manager instance
cache_manager = CacheManager()

def cache_result(expire: int = 3600):
    """
    Decorator to cache function results
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key_parts = [func.__name__] 
            cache_key_parts.extend([str(arg) for arg in args])
            cache_key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
            cache_key = hashlib.md5("|".join(cache_key_parts).encode()).hexdigest()
            
            # Try to get from cache first
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for key: {cache_key}")
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_manager.set(cache_key, result, expire)
            logger.debug(f"Cache set for key: {cache_key}")
            return result
        return wrapper
    return decorator

# Initialize cache when module is loaded
async def init_cache():
    await cache_manager.connect()

# Run cache initialization
asyncio.create_task(init_cache())