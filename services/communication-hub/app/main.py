"""Communication Hub Main Application."""

import logging
import sys
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import communications, channels, messages, campaigns, templates
from app.core.config import settings
from app.core.database import engine
from app.core.redis import redis_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Communication Hub Service...")
    
    # Initialize Redis connection
    await redis_manager.initialize()
    logger.info("✅ Redis connection established")
    
    # Test database connection and create tables
    try:
        from sqlalchemy import text
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection established")
            
        # Import models to ensure they're registered
        from app.models import campaign, message
        
        # Create tables
        from app.core.database import create_tables
        await create_tables()
        logger.info("✅ Database tables created/updated")
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
    
    logger.info("🚀 Communication Hub Service started successfully!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Communication Hub Service...")
    await redis_manager.close()
    await engine.dispose()
    logger.info("✅ Communication Hub Service shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Communication Hub API",
    description="Intelligent communication orchestration and routing service",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint."""
    return {
        "service": "communication-hub",
        "version": "0.1.0",
        "status": "running",
        "description": "Communication Hub - Intelligent routing and orchestration service"
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    try:
        # Check database
        from sqlalchemy import text
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        # Check Redis
        await redis_manager.ping()
        
        return {
            "status": "healthy",
            "service": "communication-hub",
            "version": "0.1.0",
            "timestamp": __import__("time").time(),
            "components": {
                "database": "healthy",
                "redis": "healthy"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "communication-hub",
                "version": "0.1.0",
                "timestamp": __import__("time").time(),
                "error": str(e)
            }
        )


# Include API routers
app.include_router(
    communications.router,
    prefix="/api/v1/communications",
    tags=["communications"]
)

app.include_router(
    channels.router,
    prefix="/api/v1/channels",
    tags=["channels"]
)

app.include_router(
    messages.router,
    prefix="/api/v1/messages",
    tags=["messages"]
)

app.include_router(
    campaigns.router,
    prefix="/api/v1/campaigns",
    tags=["campaigns"]
)

app.include_router(
    templates.router,
    prefix="/api/v1/templates",
    tags=["templates"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
