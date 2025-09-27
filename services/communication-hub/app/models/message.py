"""Message and conversation models."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, Boolean, Enum as SQLEnum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class MessageType(str, Enum):
    """Message type enumeration."""
    TEXT = "text"
    HTML = "html"
    FILE = "file"
    SYSTEM = "system"
    EVENT = "event"


class Direction(str, Enum):
    """Message direction enumeration."""
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class MessageStatus(str, Enum):
    """Message status enumeration."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class Priority(str, Enum):
    """Priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class SenderType(str, Enum):
    """Sender type enumeration."""
    USER = "user"
    SYSTEM = "system"
    BOT = "bot"


class RecipientType(str, Enum):
    """Recipient type enumeration."""
    USER = "user"
    GROUP = "group"
    CHANNEL = "channel"


class ConversationStatus(str, Enum):
    """Conversation status enumeration."""
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"


class ResolutionStatus(str, Enum):
    """Resolution status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REOPENED = "reopened"


class Message(Base, UUIDMixin, TimestampMixin):
    """Message model."""

    __tablename__ = "messages"

    conversation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        index=True
    )
    channel_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        index=True
    )
    type: Mapped[MessageType] = mapped_column(SQLEnum(MessageType))
    direction: Mapped[Direction] = mapped_column(SQLEnum(Direction))
    content: Mapped[Dict[str, Any]] = mapped_column(JSON)
    sender_id: Mapped[str] = mapped_column(String(36))
    sender_type: Mapped[SenderType] = mapped_column(SQLEnum(SenderType))
    sender_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    recipient_id: Mapped[str] = mapped_column(String(36))
    recipient_type: Mapped[RecipientType] = mapped_column(SQLEnum(RecipientType))
    recipient_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    status: Mapped[MessageStatus] = mapped_column(SQLEnum(MessageStatus))
    priority: Mapped[Priority] = mapped_column(SQLEnum(Priority))
    tags: Mapped[List[str]] = mapped_column(ARRAY(String))
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float)
    sentiment_confidence: Mapped[Optional[float]] = mapped_column(Float)
    sentiment_labels: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    intent_name: Mapped[Optional[str]] = mapped_column(String(100))
    intent_confidence: Mapped[Optional[float]] = mapped_column(Float)
    intent_entities: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    extra_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    # Relationships - disabled temporarily
    # conversation: Mapped["Conversation"] = relationship(back_populates="messages")


class Conversation(Base, UUIDMixin, TimestampMixin):
    """Conversation model."""

    __tablename__ = "conversations"

    channel_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        index=True
    )
    participants: Mapped[List[str]] = mapped_column(ARRAY(String))
    status: Mapped[ConversationStatus] = mapped_column(SQLEnum(ConversationStatus))
    extra_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_response_time: Mapped[Optional[float]] = mapped_column(Float)
    resolution_status: Mapped[Optional[ResolutionStatus]] = mapped_column(
        SQLEnum(ResolutionStatus)
    )
    resolution_time: Mapped[Optional[float]] = mapped_column(Float)

    # Relationships - disabled temporarily
    # messages: Mapped[List[Message]] = relationship(
    #     back_populates="conversation",
    #     cascade="all, delete-orphan"
    # )
