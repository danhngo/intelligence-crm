"""Core configuration module."""

import os
from typing import List, Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application config
    APP_NAME: str = "User Management Service"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str
    POSTGRES_POOL_SIZE: int = 20
    POSTGRES_POOL_OVERFLOW: int = 10
    
    # Redis settings
    REDIS_URL: str
    REDIS_POOL_SIZE: int = 20
    
    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Password settings
    MIN_PASSWORD_LENGTH: int = 8
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24
    
    # Session settings
    SESSION_COOKIE_NAME: str = "user_session"
    SESSION_EXPIRE_MINUTES: int = 60
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True


settings = Settings()
