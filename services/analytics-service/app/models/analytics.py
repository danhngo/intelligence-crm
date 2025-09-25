"""Analytics data models."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class EventType(str, Enum):
    """Types of events being tracked."""
    MESSAGE_SENT = "message_sent"
    MESSAGE_RECEIVED = "message_received"
    CONVERSATION_STARTED = "conversation_started"
    CONVERSATION_ENDED = "conversation_ended"
    CHANNEL_CONNECTED = "channel_connected"
    CHANNEL_DISCONNECTED = "channel_disconnected"
    USER_ACTION = "user_action"
    SYSTEM_ACTION = "system_action"


class MetricType(str, Enum):
    """Types of metrics being tracked."""
    CONVERSATION = "conversation"
    MESSAGE = "message"
    CHANNEL = "channel"
    SENTIMENT = "sentiment"
    INTENT = "intent"
    RESPONSE_TIME = "response_time"
    USER_ENGAGEMENT = "user_engagement"


class Event(Base, UUIDMixin, TimestampMixin):
    """Event tracking model."""
    
    __tablename__ = "events"

    event_type: Mapped[EventType] = mapped_column(SQLEnum(EventType), nullable=False)
    source_service: Mapped[str] = mapped_column(String(50), nullable=False)
    event_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    user_id: Mapped[Optional[str]] = mapped_column(String(36))
    session_id: Mapped[str] = mapped_column(String(36), nullable=False)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    
    # Additional metadata
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)


class MessageAnalytics(Base, UUIDMixin, TimestampMixin):
    """Analytics for message-level metrics."""
    
    __tablename__ = "message_analytics"

    message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    channel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Message metrics
    direction: Mapped[str] = mapped_column(String(10), nullable=False)  # 'inbound' or 'outbound'
    message_length: Mapped[int] = mapped_column(Integer, default=0)
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float)
    sentiment_label: Mapped[Optional[str]] = mapped_column(String(20))
    sentiment_confidence: Mapped[Optional[float]] = mapped_column(Float)
    intent_name: Mapped[Optional[str]] = mapped_column(String(100))
    intent_confidence: Mapped[Optional[float]] = mapped_column(Float)
    response_time: Mapped[Optional[float]] = mapped_column(Float)  # seconds
    
    # Metadata
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    period_hour: Mapped[str] = mapped_column(String(13), nullable=False, index=True)  # YYYY-MM-DD-HH
    period_day: Mapped[str] = mapped_column(String(10), nullable=False, index=True)   # YYYY-MM-DD


class ConversationAnalytics(Base, UUIDMixin, TimestampMixin):
    """Analytics for conversation-level metrics."""
    
    __tablename__ = "conversation_analytics"

    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    channel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Conversation metrics
    total_messages: Mapped[int] = mapped_column(Integer, default=0)
    inbound_messages: Mapped[int] = mapped_column(Integer, default=0)
    outbound_messages: Mapped[int] = mapped_column(Integer, default=0)
    avg_response_time: Mapped[Optional[float]] = mapped_column(Float)
    max_response_time: Mapped[Optional[float]] = mapped_column(Float)
    min_response_time: Mapped[Optional[float]] = mapped_column(Float)
    
    # Sentiment analysis
    avg_sentiment_score: Mapped[Optional[float]] = mapped_column(Float)
    sentiment_distribution: Mapped[Dict[str, int]] = mapped_column(JSON, default=dict)
    
    # Intent analysis
    top_intents: Mapped[Dict[str, int]] = mapped_column(JSON, default=dict)
    intent_changes: Mapped[int] = mapped_column(Integer, default=0)
    
    # Resolution metrics
    duration_minutes: Mapped[Optional[float]] = mapped_column(Float)
    resolution_status: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Metadata
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    period_day: Mapped[str] = mapped_column(String(10), nullable=False, index=True)


class ChannelAnalytics(Base, UUIDMixin, TimestampMixin):
    """Analytics for channel-level metrics."""
    
    __tablename__ = "channel_analytics"

    channel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    channel_type: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Channel metrics
    active_conversations: Mapped[int] = mapped_column(Integer, default=0)
    new_conversations: Mapped[int] = mapped_column(Integer, default=0)
    closed_conversations: Mapped[int] = mapped_column(Integer, default=0)
    messages_processed: Mapped[int] = mapped_column(Integer, default=0)
    
    # Performance metrics
    avg_response_time: Mapped[Optional[float]] = mapped_column(Float)
    success_rate: Mapped[float] = mapped_column(Float, default=0.0)
    error_count: Mapped[int] = mapped_column(Integer, default=0)
    uptime_percentage: Mapped[float] = mapped_column(Float, default=100.0)
    
    # Quality metrics
    avg_conversation_rating: Mapped[Optional[float]] = mapped_column(Float)
    customer_satisfaction_score: Mapped[Optional[float]] = mapped_column(Float)
    
    # Metadata
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    period_hour: Mapped[str] = mapped_column(String(13), nullable=False, index=True)
    period_day: Mapped[str] = mapped_column(String(10), nullable=False, index=True)


class UserEngagementAnalytics(Base, UUIDMixin, TimestampMixin):
    """Analytics for user engagement metrics."""
    
    __tablename__ = "user_engagement_analytics"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(36), nullable=False)
    
    # Engagement metrics
    total_sessions: Mapped[int] = mapped_column(Integer, default=0)
    total_messages: Mapped[int] = mapped_column(Integer, default=0)
    avg_session_duration: Mapped[Optional[float]] = mapped_column(Float)
    last_activity: Mapped[datetime] = mapped_column(nullable=False)
    
    # Behavior metrics
    channels_used: Mapped[List[str]] = mapped_column(ARRAY(String))
    most_active_channel: Mapped[Optional[str]] = mapped_column(String(20))
    preferred_communication_time: Mapped[Optional[str]] = mapped_column(String(5))  # HH:MM
    
    # Metadata
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    period_day: Mapped[str] = mapped_column(String(10), nullable=False, index=True)


class MetricSnapshot(Base, UUIDMixin, TimestampMixin):
    """Snapshot of aggregated metrics for fast retrieval."""
    
    __tablename__ = "metric_snapshots"

    metric_type: Mapped[MetricType] = mapped_column(SQLEnum(MetricType), nullable=False)
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    dimensions: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    # Time dimensions
    period_type: Mapped[str] = mapped_column(String(10), nullable=False)  # 'hour', 'day', 'week', 'month'
    period_value: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Metadata
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
