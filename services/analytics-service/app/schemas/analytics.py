"""Analytics API schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.analytics import EventType, MetricType


class EventCreate(BaseModel):
    """Schema for creating an analytics event."""
    
    event_type: EventType
    event_data: Dict[str, Any]
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    source_service: str = "communication-hub"


class EventResponse(BaseModel):
    """Schema for event response."""
    
    id: UUID
    event_type: EventType
    source_service: str
    event_data: Dict[str, Any]
    user_id: Optional[str] = None
    session_id: str
    tenant_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageAnalyticsCreate(BaseModel):
    """Schema for creating message analytics."""
    
    id: str
    conversation_id: str
    channel_id: str
    direction: str = Field(..., pattern="^(inbound|outbound)$")
    content: Dict[str, Any] = Field(default_factory=dict)
    sentiment: Optional[Dict[str, Any]] = None
    intent: Optional[Dict[str, Any]] = None
    response_time: Optional[float] = None


class MessageAnalyticsResponse(BaseModel):
    """Schema for message analytics response."""
    
    id: UUID
    message_id: UUID
    conversation_id: UUID
    channel_id: UUID
    direction: str
    message_length: int
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    sentiment_confidence: Optional[float] = None
    intent_name: Optional[str] = None
    intent_confidence: Optional[float] = None
    response_time: Optional[float] = None
    tenant_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationAnalyticsResponse(BaseModel):
    """Schema for conversation analytics response."""
    
    conversation_id: str
    period: Dict[str, datetime]
    message_metrics: Dict[str, Any]
    sentiment_metrics: Dict[str, Any]
    intent_metrics: Dict[str, Any]
    performance_metrics: Dict[str, Any]


class ChannelAnalyticsResponse(BaseModel):
    """Schema for channel analytics response."""
    
    channel_id: str
    period: Dict[str, datetime]
    metrics: Dict[str, Any]
    time_series: List[Dict[str, Any]] = Field(default_factory=list)


class DashboardMetricsResponse(BaseModel):
    """Schema for dashboard metrics response."""
    
    period: Dict[str, datetime]
    message_metrics: Dict[str, Any]
    conversation_metrics: Dict[str, Any]


class TimeRangeQuery(BaseModel):
    """Schema for time range queries."""
    
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class MetricQuery(BaseModel):
    """Schema for metric queries."""
    
    metric_type: Optional[MetricType] = None
    period: str = Field(default="day", pattern="^(hour|day|week|month)$")
    dimensions: Dict[str, str] = Field(default_factory=dict)


class BulkEventCreate(BaseModel):
    """Schema for creating multiple events."""
    
    events: List[EventCreate]


class AnalyticsHealthResponse(BaseModel):
    """Schema for health check response."""
    
    status: str
    timestamp: datetime
    database_connected: bool
    cache_connected: bool
    processing_queue_size: int
