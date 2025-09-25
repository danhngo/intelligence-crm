"""Configuration management for the Workflow Engine Service."""

from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # Application config
    APP_NAME: str = "Workflow Engine Service"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str
    POSTGRES_POOL_SIZE: int = 20
    POSTGRES_POOL_OVERFLOW: int = 10
    
    # Redis settings
    REDIS_URL: str
    REDIS_POOL_SIZE: int = 20
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    
    # Workflow Engine settings
    MAX_WORKFLOW_STEPS: int = 50
    MAX_PARALLEL_EXECUTIONS: int = 10
    EXECUTION_TIMEOUT_SECONDS: int = 3600  # 1 hour
    MAX_RETRY_ATTEMPTS: int = 3
    RETRY_DELAY_SECONDS: int = 60
    
    # Service integrations
    CRM_SERVICE_URL: str = "http://crm-core:8000"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    
settings = Settings()
