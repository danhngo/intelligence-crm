"""Redis Cache Management

This module provides Redis client setup and cache management utilities with 
tenant isolation, TTL management, and semantic similarity caching for LLM responses.
"""

from typing import Optional, Any, Dict
import json
import asyncio
from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool
import numpy as np
# from sentence_transformers import SentenceTransformer
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

# Initialize embedding model for semantic caching - temporarily disabled
EMBEDDING_MODEL = None
# if settings.CACHE_EMBEDDINGS:
#     EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# Create Redis connection pool
redis_pool = ConnectionPool.from_url(
    str(settings.REDIS_URL),
    max_connections=20,
    decode_responses=True
)

# Create Redis client instance
redis_client = Redis(
    connection_pool=redis_pool,
    encoding='utf-8',
    decode_responses=True
)


def get_tenant_key(key: str, tenant_id: str) -> str:
    """Generate tenant-scoped Redis key.
    
    Args:
        key: Base Redis key
        tenant_id: Tenant identifier
        
    Returns:
        Tenant-scoped Redis key
    """
    return f"{tenant_id}:{key}"


async def set_cache(
    key: str,
    value: Any,
    tenant_id: str,
    ttl: Optional[int] = None,
    embeddings: Optional[np.ndarray] = None
) -> bool:
    """Set value in Redis with tenant isolation and optional TTL.
    
    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        tenant_id: Tenant identifier
        ttl: Optional TTL in seconds
        embeddings: Optional vector embeddings for semantic caching
        
    Returns:
        True if successful, False otherwise
    """
    try:
        tenant_key = get_tenant_key(key, tenant_id)
        json_value = json.dumps({
            "value": value,
            "embeddings": embeddings.tolist() if embeddings is not None else None
        })
        
        async with redis_client.pipeline(transaction=True) as pipe:
            await pipe.set(tenant_key, json_value)
            if ttl:
                await pipe.expire(tenant_key, ttl)
            await pipe.execute()
            
        logger.debug(
            "Cache set successful",
            key=key,
            tenant_id=tenant_id,
            ttl=ttl
        )
        return True
        
    except Exception as e:
        logger.error(
            "Cache set failed",
            key=key,
            tenant_id=tenant_id,
            error=str(e)
        )
        return False


async def get_cache(key: str, tenant_id: str) -> Optional[Any]:
    """Get value from Redis with tenant isolation.
    
    Args:
        key: Cache key
        tenant_id: Tenant identifier
        
    Returns:
        Cached value if found, None otherwise
    """
    try:
        tenant_key = get_tenant_key(key, tenant_id)
        cached = await redis_client.get(tenant_key)
        
        if cached:
            cached_data = json.loads(cached)
            logger.debug(
                "Cache hit",
                key=key,
                tenant_id=tenant_id
            )
            return cached_data["value"]
            
        logger.debug(
            "Cache miss",
            key=key,
            tenant_id=tenant_id
        )
        return None
        
    except Exception as e:
        logger.error(
            "Cache get failed",
            key=key,
            tenant_id=tenant_id,
            error=str(e)
        )
        return None


async def get_semantic_cache(
    text: str,
    tenant_id: str,
    similarity_threshold: float = settings.SEMANTIC_CACHE_SIMILARITY_THRESHOLD
) -> Optional[Dict[str, Any]]:
    """Get semantically similar cached response using embeddings comparison.
    
    Args:
        text: Input text to find similar cached responses for
        tenant_id: Tenant identifier
        similarity_threshold: Minimum cosine similarity threshold
        
    Returns:
        Most similar cached response if found above threshold, None otherwise
    """
    # Temporarily disabled until sentence_transformers dependency is fixed
    return None
    
    if not settings.CACHE_EMBEDDINGS or not EMBEDDING_MODEL:
        return None
        
    try:
        # Get embeddings for input text
        input_embeddings = EMBEDDING_MODEL.encode(text)
        
        # Get all cached responses for tenant
        tenant_keys = await redis_client.keys(f"{tenant_id}:*")
        if not tenant_keys:
            return None
            
        # Get all cached values
        cached_values = await asyncio.gather(*[
            redis_client.get(key) for key in tenant_keys
        ])
        
        # Find most similar cached response
        max_similarity = -1
        best_match = None
        
        for cached in cached_values:
            if not cached:
                continue
                
            cached_data = json.loads(cached)
            cached_embeddings = cached_data.get("embeddings")
            
            if not cached_embeddings:
                continue
                
            # Calculate cosine similarity
            similarity = np.dot(
                input_embeddings,
                np.array(cached_embeddings)
            ) / (
                np.linalg.norm(input_embeddings) *
                np.linalg.norm(cached_embeddings)
            )
            
            if similarity > max_similarity and similarity >= similarity_threshold:
                max_similarity = similarity
                best_match = cached_data["value"]
        
        if best_match:
            logger.debug(
                "Semantic cache hit",
                tenant_id=tenant_id,
                similarity=max_similarity
            )
            return best_match
            
        logger.debug(
            "Semantic cache miss",
            tenant_id=tenant_id
        )
        return None
        
    except Exception as e:
        logger.error(
            "Semantic cache lookup failed",
            tenant_id=tenant_id,
            error=str(e)
        )
        return None


async def delete_cache(key: str, tenant_id: str) -> bool:
    """Delete value from Redis with tenant isolation.
    
    Args:
        key: Cache key
        tenant_id: Tenant identifier
        
    Returns:
        True if successful, False otherwise
    """
    try:
        tenant_key = get_tenant_key(key, tenant_id)
        deleted = await redis_client.delete(tenant_key)
        
        if deleted:
            logger.debug(
                "Cache delete successful",
                key=key,
                tenant_id=tenant_id
            )
            return True
            
        logger.debug(
            "Cache key not found",
            key=key,
            tenant_id=tenant_id
        )
        return False
        
    except Exception as e:
        logger.error(
            "Cache delete failed", 
            key=key,
            tenant_id=tenant_id,
            error=str(e)
        )
        return False


async def clear_tenant_cache(tenant_id: str) -> bool:
    """Clear all cached values for a tenant.
    
    Args:
        tenant_id: Tenant identifier
        
    Returns:
        True if successful, False otherwise
    """
    try:
        tenant_keys = await redis_client.keys(f"{tenant_id}:*")
        if tenant_keys:
            await redis_client.delete(*tenant_keys)
            
        logger.info(
            "Tenant cache cleared",
            tenant_id=tenant_id,
            keys_deleted=len(tenant_keys)
        )
        return True
        
    except Exception as e:
        logger.error(
            "Clear tenant cache failed",
            tenant_id=tenant_id,
            error=str(e)
        )
        return False
