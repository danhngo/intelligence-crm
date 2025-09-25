"""Configuration management for the CRM Core Service."""

from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.
    
    Loads configuration from environment variables and .env file
    """
    
    # Application config
    APP_NAME: str = "CRM Core Service"
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
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    
    # Rate limiting
    RATE_LIMIT_PER_SECOND: int = 10
    
    # Contact validation
    MIN_CONTACT_SCORE: float = 0.0
    MAX_CONTACT_SCORE: float = 100.0
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra environment variables
    )

    
settings = Settings()
