"""Redis cache implementation."""

from typing import Any, Dict, List, Optional, Union
import json
import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.config import get_settings

settings = get_settings()


class AsyncRedisCache:
    """Async Redis cache implementation."""
    
    def __init__(self):
        self.redis: Optional[Redis] = None
    
    async def connect(self):
        """Connect to Redis."""
        self.redis = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            socket_timeout=settings.REDIS_TIMEOUT,
            socket_connect_timeout=settings.REDIS_TIMEOUT,
        )
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key."""
        if not self.redis:
            await self.connect()
        return await self.redis.get(key)
    
    async def set(
        self, 
        key: str, 
        value: Union[str, int, float, dict, list], 
        ttl: Optional[int] = None
    ) -> bool:
        """Set key-value pair with optional TTL."""
        if not self.redis:
            await self.connect()
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        return await self.redis.set(key, value, ex=ttl)
    
    async def delete(self, key: str) -> int:
        """Delete key."""
        if not self.redis:
            await self.connect()
        return await self.redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        if not self.redis:
            await self.connect()
        return await self.redis.exists(key)
    
    async def hincrby(self, key: str, field: str, amount: int = 1) -> int:
        """Increment hash field by amount."""
        if not self.redis:
            await self.connect()
        return await self.redis.hincrby(key, field, amount)
    
    async def hincrbyfloat(self, key: str, field: str, amount: float) -> float:
        """Increment hash field by float amount."""
        if not self.redis:
            await self.connect()
        return await self.redis.hincrbyfloat(key, field, amount)
    
    async def hgetall(self, key: str) -> Dict[str, str]:
        """Get all fields and values in hash."""
        if not self.redis:
            await self.connect()
        return await self.redis.hgetall(key)
    
    async def hset(self, key: str, field: str, value: Union[str, int, float]) -> int:
        """Set hash field."""
        if not self.redis:
            await self.connect()
        return await self.redis.hset(key, field, value)
    
    async def expire(self, key: str, ttl: int) -> bool:
        """Set TTL for key."""
        if not self.redis:
            await self.connect()
        return await self.redis.expire(key, ttl)
    
    async def lpush(self, key: str, *values: str) -> int:
        """Push values to the head of list."""
        if not self.redis:
            await self.connect()
        return await self.redis.lpush(key, *values)
    
    async def lrange(self, key: str, start: int, end: int) -> List[str]:
        """Get range of list elements."""
        if not self.redis:
            await self.connect()
        return await self.redis.lrange(key, start, end)
    
    async def ltrim(self, key: str, start: int, end: int) -> bool:
        """Trim list to specified range."""
        if not self.redis:
            await self.connect()
        return await self.redis.ltrim(key, start, end)


# Global cache instance
cache = AsyncRedisCache()


async def get_cache() -> AsyncRedisCache:
    """Dependency for getting cache instance."""
    return cache
