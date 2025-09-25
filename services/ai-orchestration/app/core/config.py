"""Configuration Management

This module uses Pydantic's settings management for configuration with environment variable 
support and validation. It handles all service configuration including database URLs,
LLM provider keys, Redis settings, and security parameters.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, validator, AnyHttpUrl, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    """Base service configuration settings."""
    
    # Application Settings
    PROJECT_NAME: str = "AI/ML Orchestration Service"
    VERSION: str = "0.1.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    API_V1_PREFIX: str = "/api/v1"
    
    # Server Settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    WORKERS: int = Field(default=4, env="WORKERS")
    ALLOWED_HOSTS: List[str] = Field(default=["*"])
    ALLOWED_ORIGINS: List[str] = Field(default=["*"])
    
    # Security Settings
    SECRET_KEY: str = Field(default="", env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Settings
    POSTGRES_HOST: str = Field(default="localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: str = Field(default="5432", env="POSTGRES_PORT")
    POSTGRES_USER: str = Field(default="postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(default="ai_orchestration", env="POSTGRES_DB")
    POSTGRES_POOL_SIZE: int = Field(default=20, env="POSTGRES_POOL_SIZE")
    DATABASE_URL: Optional[PostgresDsn] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Construct database URL if not provided directly."""
        if isinstance(v, str):
            return v
        
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=int(values.get("POSTGRES_PORT")),
            path=f"/{values.get('POSTGRES_DB')}"
        ).unicode_string()

    # Redis Settings
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_PASSWORD: str = Field(default="", env="REDIS_PASSWORD")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    REDIS_URL: Optional[RedisDsn] = None

    @validator("REDIS_URL", pre=True)
    def assemble_redis_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Construct Redis URL if not provided directly."""
        if isinstance(v, str):
            return v
        
        password = f":{values.get('REDIS_PASSWORD')}@" if values.get("REDIS_PASSWORD") else "@"
        return f"redis://{password}{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}/{values.get('REDIS_DB')}"

    # LLM Provider Settings
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    OPENAI_ORGANIZATION: str = Field(default="", env="OPENAI_ORGANIZATION")
    OPENAI_DEFAULT_MODEL: str = "gpt-4"
    OPENAI_TIMEOUT: int = 30
    
    GOOGLE_API_KEY: str = Field(default="", env="GOOGLE_API_KEY")
    GOOGLE_PROJECT_ID: str = Field(default="", env="GOOGLE_PROJECT_ID")
    GOOGLE_DEFAULT_MODEL: str = "gemini-pro"
    
    ANTHROPIC_API_KEY: str = Field(default="", env="ANTHROPIC_API_KEY")
    ANTHROPIC_DEFAULT_MODEL: str = "claude-2"

    # Token and Cost Management
    MAX_TOKENS_PER_REQUEST: int = 4096
    TOKEN_BUDGET_PER_TENANT: Dict[str, int] = Field(default={})
    COST_PER_1K_TOKENS: Dict[str, float] = Field(
        default={
            "gpt-4": 0.03,
            "gpt-3.5-turbo": 0.002,
            "gemini-pro": 0.0005,
            "claude-2": 0.01
        }
    )

    # Caching Settings
    CACHE_TTL: int = 3600  # Default 1 hour
    SEMANTIC_CACHE_SIMILARITY_THRESHOLD: float = 0.95
    CACHE_EMBEDDINGS: bool = True
    
    # Vector Database Settings
    PINECONE_API_KEY: str = Field(default="", env="PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: str = Field(default="", env="PINECONE_ENVIRONMENT")
    PINECONE_INDEX: str = Field(default="crm-embeddings", env="PINECONE_INDEX")
    
    # Monitoring Settings
    ENABLE_TELEMETRY: bool = True
    SENTRY_DSN: str = Field(default="", env="SENTRY_DSN")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Resource Limits
    MAX_CONCURRENT_WORKFLOWS: int = 100
    RATE_LIMIT_PER_MINUTE: int = 60
    WORKFLOW_TIMEOUT_SECONDS: int = 300  # 5 minutes
    
    class Config:
        """Pydantic model configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings instance
settings = Settings()
