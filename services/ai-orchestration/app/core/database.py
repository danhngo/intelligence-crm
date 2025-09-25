"""Database Connection Management

This module provides async SQLAlchemy engine setup with connection pooling
and tenant-scoped session management.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
import structlog
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)

from app.core.config import settings

logger = structlog.get_logger(__name__)

# Create async engine with connection pooling
engine = create_async_engine(
    str(settings.DATABASE_URL),
    pool_size=settings.POSTGRES_POOL_SIZE,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections after 30 minutes
    pool_pre_ping=True,  # Enable connection health checks
    echo=settings.DEBUG
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session with automatic cleanup.
    
    Yields:
        AsyncSession: Database session
    """
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception as e:
        logger.error("Database session error", error=str(e))
        await session.rollback()
        raise
    finally:
        await session.close()


@asynccontextmanager
async def get_tenant_db(tenant_id: str) -> AsyncGenerator[AsyncSession, None]:
    """Get tenant-scoped database session.
    
    Args:
        tenant_id: Tenant identifier
    
    Yields:
        AsyncSession: Database session with tenant scope
    """
    session = AsyncSessionLocal()
    
    # Set tenant ID in session info
    session.info["tenant_id"] = tenant_id
    
    try:
        # Add tenant filter to all queries
        for mapper in session.registry.mappers:
            if hasattr(mapper.class_, "__tenant_id__"):
                session.add_global_filter(
                    f"{mapper.class_.__name__}_tenant_filter",
                    lambda cls: cls.__tenant_id__ == tenant_id
                )
        
        yield session
        
    except Exception as e:
        logger.error(
            "Tenant database session error",
            tenant_id=tenant_id,
            error=str(e)
        )
        await session.rollback()
        raise
        
    finally:
        await session.close()
