"""Core configuration settings."""

from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # App settings
    APP_NAME: str = "Communication Hub"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@communication-db:5432/communication_hub"
    
    # Redis settings
    REDIS_URL: str = "redis://communication-redis:6379/0"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # External service URLs
    CRM_CORE_URL: str = "http://crm-core:8000"
    USER_MANAGEMENT_URL: str = "http://user-management:8002"
    AI_ORCHESTRATION_URL: str = "http://ai-orchestration:8005"
    
    # Communication providers
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    SENDGRID_API_KEY: Optional[str] = None
    SLACK_BOT_TOKEN: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "communication-hub-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
