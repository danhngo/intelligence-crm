"""Channel schemas."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.models.channel import (
    ChannelStatus,
    ChannelType,
    IntegrationType,
    MessageFormat,
)


class ChannelConfig(BaseModel):
    """Channel configuration schema."""
    
    credentials: Dict[str, Any] = Field(default_factory=dict)
    settings: Dict[str, Any] = Field(default_factory=dict)
    rate_limits: Optional[Dict[str, Any]] = None
    retry_policy: Optional[Dict[str, Any]] = None
    message_templates: Optional[Dict[str, Any]] = None


class ChannelBase(BaseModel):
    """Base channel schema."""
    
    name: str
    type: ChannelType
    integration_type: IntegrationType
    supported_formats: List[MessageFormat] = Field(default_factory=list)
    config: ChannelConfig
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChannelCreate(ChannelBase):
    """Schema for creating a channel."""
    pass


class ChannelUpdate(BaseModel):
    """Schema for updating a channel."""
    
    name: Optional[str] = None
    config: Optional[ChannelConfig] = None
    metadata: Optional[Dict[str, Any]] = None


class Channel(ChannelBase):
    """Schema for channel response."""
    
    id: uuid.UUID
    status: ChannelStatus
    message_count: int
    error_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class ChannelStats(BaseModel):
    """Channel statistics schema."""
    
    message_count: int
    error_count: int
    avg_latency: float
    success_rate: float
    metrics: Dict[str, Any] = Field(default_factory=dict)
