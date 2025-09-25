"""Database configuration and dependencies."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.POSTGRES_POOL_SIZE,
    max_overflow=settings.POSTGRES_POOL_OVERFLOW,
    pool_timeout=settings.POSTGRES_POOL_TIMEOUT,
    poolclass=NullPool if "sqlite" in settings.DATABASE_URL else None,
    echo=settings.DEBUG,
)

# Create session maker
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """Get database session context manager."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
