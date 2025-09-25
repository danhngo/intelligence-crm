"""Main FastAPI Application for AI/ML Orchestration Service

This module initializes the FastAPI application with middleware, error handling,
health endpoints, and routing for AI orchestration capabilities.
"""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import structlog
import uvicorn

from app.core.config import settings
from app.core.database import engine
from app.core.cache import redis_client

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting AI/ML Orchestration Service")
    
    # Test database connection
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        logger.info("Database connection established")
    except Exception as e:
        logger.error("Database connection failed", error=str(e))
        raise
    
    # Test Redis connection
    try:
        await redis_client.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.error("Redis connection failed", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI/ML Orchestration Service")
    await engine.dispose()
    await redis_client.close()


# Initialize FastAPI application
app = FastAPI(
    title="AI/ML Orchestration Service",
    description="Intelligent automation engine for CRM platform AI capabilities",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)


# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log all HTTP requests with performance metrics."""
    start_time = time.time()
    
    # Extract tenant context if available
    tenant_id = request.headers.get("X-Tenant-ID", "unknown")
    
    logger.info(
        "Request started",
        method=request.method,
        url=str(request.url),
        tenant_id=tenant_id,
        client_ip=request.client.host if request.client else None
    )
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            "Request completed",
            method=request.method,
            url=str(request.url),
            tenant_id=tenant_id,
            status_code=response.status_code,
            process_time=round(process_time, 4)
        )
        
        # Add performance header
        response.headers["X-Process-Time"] = str(process_time)
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        
        logger.error(
            "Request failed",
            method=request.method,
            url=str(request.url),
            tenant_id=tenant_id,
            process_time=round(process_time, 4),
            error=str(e),
            exc_info=True
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": "An unexpected error occurred",
                "request_id": str(time.time())
            }
        )


# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "ai-ml-orchestration",
        "version": "0.1.0",
        "timestamp": time.time()
    }


@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """Readiness probe for Kubernetes deployment."""
    checks = {}
    all_healthy = True
    
    # Check database
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
        all_healthy = False
    
    # Check Redis
    try:
        await redis_client.ping()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"
        all_healthy = False
    
    status_code = 200 if all_healthy else 503
    return Response(
        content=str({
            "status": "ready" if all_healthy else "not_ready",
            "checks": checks,
            "timestamp": time.time()
        }),
        status_code=status_code,
        media_type="application/json"
    )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with service information."""
    return {
        "service": "AI/ML Orchestration Service",
        "description": "Intelligent automation engine for CRM platform AI capabilities",
        "version": "0.1.0",
        "status": "running",
        "docs_url": "/docs" if settings.DEBUG else "disabled in production"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(
        "Unhandled exception",
        method=request.method,
        url=str(request.url),
        error=str(exc),
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred",
            "request_id": str(time.time())
        }
    )


# Development server
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
