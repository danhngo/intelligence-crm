"""Main application module."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import workflows
from app.core.config import settings
from app.core.database import close_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler."""
    yield
    # Close database connection on shutdown
    await close_db_connection()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Include API routers
app.include_router(
    workflows.router,
    prefix=f"{settings.API_V1_PREFIX}/workflow-engine",
    tags=["workflow-engine"]
)
