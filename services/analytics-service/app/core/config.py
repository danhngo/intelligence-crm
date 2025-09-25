"""Core configuration for the analytics service."""

from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Service configuration settings."""
    
    # Service configuration
    SERVICE_NAME: str = "analytics-service"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    PORT: int = 8000
    
    # Database settings
    DATABASE_URL: str
    POSTGRES_POOL_SIZE: int = 20
    POSTGRES_POOL_OVERFLOW: int = 10
    POSTGRES_POOL_TIMEOUT: int = 30
    
    # Redis settings for caching
    REDIS_URL: str
    REDIS_POOL_SIZE: int = 20
    REDIS_TIMEOUT: int = 5
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External services
    CRM_SERVICE_URL: str = "http://crm:8000"
    COMMUNICATION_HUB_URL: str = "http://communication-hub:8000"
    WORKFLOW_ENGINE_URL: str = "http://workflow-engine:8001"
    USER_MANAGEMENT_URL: str = "http://user-management:8002"
    
    # Analytics configuration
    ANALYTICS_BATCH_SIZE: int = 100
    ANALYTICS_PROCESSING_INTERVAL: int = 60  # seconds
    METRICS_RETENTION_DAYS: int = 90
    
    # CORS settings
    ALLOWED_HOSTS: List[str] = ["*"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
