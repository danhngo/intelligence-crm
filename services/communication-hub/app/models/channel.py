"""Channel models."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from sqlalchemy import JSON, Boolean, DateTime, Enum as SQLEnum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.message import Message, Conversation

from app.models.base import Base, TimestampMixin, UUIDMixin


class ChannelType(str, Enum):
    """Channel type enumeration."""
    EMAIL = "email"
    SMS = "sms"
    CHAT = "chat"
    SOCIAL = "social"
    VOICE = "voice"


class ProviderType(str, Enum):
    """Provider type enumeration."""
    SMTP = "smtp"
    TWILIO = "twilio"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    WHATSAPP = "whatsapp"
    CUSTOM = "custom"


class HealthStatus(str, Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class Channel(Base, UUIDMixin, TimestampMixin):
    """Channel model."""

    __tablename__ = "channels"

    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[ChannelType] = mapped_column(SQLEnum(ChannelType))
    provider: Mapped[ProviderType] = mapped_column(SQLEnum(ProviderType))
    credentials: Mapped[Dict[str, str]] = mapped_column(JSON)
    settings: Mapped[Dict[str, any]] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    health_status: Mapped[HealthStatus] = mapped_column(
        SQLEnum(HealthStatus),
        default=HealthStatus.HEALTHY
    )
    last_health_check: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    error_rate: Mapped[float] = mapped_column(Float, default=0.0)
    avg_response_time: Mapped[float] = mapped_column(Float, default=0.0)
    metadata: Mapped[Dict[str, any]] = mapped_column(JSON, default=dict)

    # Relationships
    messages: Mapped[List["Message"]] = relationship(
        back_populates="channel",
        cascade="all, delete-orphan"
    )
    conversations: Mapped[List["Conversation"]] = relationship(
        back_populates="channel",
        cascade="all, delete-orphan"
    )
