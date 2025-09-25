"""Main application module."""

import time
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import contacts
from app.core.config import settings
from app.core.database import close_db_connection, engine


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

# Add trusted host middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Root endpoint
@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint."""
    return {
        "service": "crm-core",
        "version": "0.1.0",
        "status": "running",
        "description": "CRM Core - Customer relationship management service"
    }


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    try:
        # Check database connection
        from sqlalchemy import text
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "service": "crm-core",
            "version": "0.1.0",
            "timestamp": time.time(),
            "components": {
                "database": "healthy"
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "crm-core",
                "version": "0.1.0",
                "timestamp": time.time(),
                "error": str(e)
            }
        )


# Include API routers
app.include_router(
    contacts.router,
    prefix=f"{settings.API_V1_PREFIX}/contacts",
    tags=["contacts"]
)
