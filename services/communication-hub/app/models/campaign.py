"""Campaign and email tracking models."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, Boolean, DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, INET, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class CampaignType(str, Enum):
    """Campaign type enumeration."""
    EMAIL = "email"
    SMS = "sms" 
    WHATSAPP = "whatsapp"
    MULTI_CHANNEL = "multi_channel"


class CampaignStatus(str, Enum):
    """Campaign status enumeration."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class EmailEventType(str, Enum):
    """Email event type enumeration."""
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened" 
    CLICKED = "clicked"
    BOUNCED = "bounced"
    COMPLAINED = "complained"
    UNSUBSCRIBED = "unsubscribed"


class Campaign(Base, UUIDMixin, TimestampMixin):
    """Campaign model for multi-channel campaigns."""

    __tablename__ = "campaigns"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    type: Mapped[CampaignType] = mapped_column(SQLEnum(CampaignType))
    status: Mapped[CampaignStatus] = mapped_column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT)
    
    # Tenant isolation
    tenant_id: Mapped[uuid.UUID] = mapped_column(index=True)
    created_by: Mapped[uuid.UUID] = mapped_column()
    
    # Scheduling
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Targeting
    target_segments: Mapped[List[str]] = mapped_column(ARRAY(String))  # Contact segment IDs
    contact_list_ids: Mapped[List[str]] = mapped_column(ARRAY(String))  # Static contact lists
    
    # Content
    template_id: Mapped[Optional[uuid.UUID]] = mapped_column()
    subject_line: Mapped[Optional[str]] = mapped_column(String(255))
    sender_name: Mapped[Optional[str]] = mapped_column(String(100))
    sender_email: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Settings
    tracking_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    click_tracking_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    open_tracking_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    unsubscribe_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Statistics (computed fields)
    total_recipients: Mapped[int] = mapped_column(Integer, default=0)
    sent_count: Mapped[int] = mapped_column(Integer, default=0)
    delivered_count: Mapped[int] = mapped_column(Integer, default=0)
    opened_count: Mapped[int] = mapped_column(Integer, default=0)
    clicked_count: Mapped[int] = mapped_column(Integer, default=0)
    bounced_count: Mapped[int] = mapped_column(Integer, default=0)
    complained_count: Mapped[int] = mapped_column(Integer, default=0)
    unsubscribed_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Configuration
    config: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    extra_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    # Relationships
    campaign_messages: Mapped[List["CampaignMessage"]] = relationship(
        back_populates="campaign", cascade="all, delete-orphan"
    )
    email_events: Mapped[List["EmailTrackingEvent"]] = relationship(
        back_populates="campaign", cascade="all, delete-orphan"
    )


class CampaignMessage(Base, UUIDMixin, TimestampMixin):
    """Individual message sent as part of a campaign."""

    __tablename__ = "campaign_messages"

    campaign_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    message_id: Mapped[Optional[uuid.UUID]] = mapped_column()
    
    # Recipient info
    recipient_email: Mapped[str] = mapped_column(String(255), index=True)
    recipient_contact_id: Mapped[Optional[uuid.UUID]] = mapped_column()
    
    # Content (personalized)
    subject_line: Mapped[str] = mapped_column(String(255))
    html_content: Mapped[Optional[str]] = mapped_column(Text)
    text_content: Mapped[Optional[str]] = mapped_column(Text)
    
    # Tracking IDs
    tracking_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, sent, delivered, failed
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Error tracking
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Personalization data
    personalization_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    # Relationships
    campaign: Mapped[Campaign] = relationship(back_populates="campaign_messages")
    # Note: Message relationship will be added when Message model is properly imported


class EmailTrackingEvent(Base, UUIDMixin, TimestampMixin):
    """Email tracking events (opens, clicks, bounces, etc.)."""

    __tablename__ = "email_tracking_events"

    campaign_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    campaign_message_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("campaign_messages.id", ondelete="CASCADE"), index=True
    )
    message_id: Mapped[Optional[uuid.UUID]] = mapped_column()
    
    # Event details
    event_type: Mapped[EmailEventType] = mapped_column(SQLEnum(EmailEventType), index=True)
    tracking_id: Mapped[str] = mapped_column(String(255), index=True)
    recipient_email: Mapped[str] = mapped_column(String(255), index=True)
    
    # Timestamp
    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    
    # Event-specific data
    url: Mapped[Optional[str]] = mapped_column(Text)  # For click events
    link_id: Mapped[Optional[str]] = mapped_column(String(255))  # Internal link identifier
    
    # Client information
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    ip_address: Mapped[Optional[str]] = mapped_column(INET)
    country: Mapped[Optional[str]] = mapped_column(String(2))
    region: Mapped[Optional[str]] = mapped_column(String(100))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Device/client info
    device_type: Mapped[Optional[str]] = mapped_column(String(50))  # desktop, mobile, tablet
    client_name: Mapped[Optional[str]] = mapped_column(String(100))  # Gmail, Outlook, etc.
    client_version: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Additional metadata
    extra_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    # Relationships
    campaign: Mapped[Optional[Campaign]] = relationship(back_populates="email_events")
    campaign_message: Mapped[Optional[CampaignMessage]] = relationship()


class EmailTemplate(Base, UUIDMixin, TimestampMixin):
    """Email template model for campaigns."""

    __tablename__ = "email_templates"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Tenant isolation
    tenant_id: Mapped[uuid.UUID] = mapped_column(index=True)
    created_by: Mapped[uuid.UUID] = mapped_column()
    
    # Template content
    subject_template: Mapped[str] = mapped_column(String(255))
    html_template: Mapped[Optional[str]] = mapped_column(Text)
    text_template: Mapped[Optional[str]] = mapped_column(Text)
    
    # Template variables and personalization
    variables: Mapped[List[str]] = mapped_column(ARRAY(String))  # Available template variables
    sample_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)  # Sample data for preview
    
    # Template settings
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    tags: Mapped[List[str]] = mapped_column(ARRAY(String))
    
    # Usage tracking
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Metadata
    extra_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)


class ContactSegment(Base, UUIDMixin, TimestampMixin):
    """Contact segment for campaign targeting."""

    __tablename__ = "contact_segments"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Tenant isolation
    tenant_id: Mapped[uuid.UUID] = mapped_column(index=True)
    created_by: Mapped[uuid.UUID] = mapped_column()
    
    # Segment criteria (stored as SQL-like filters)
    criteria: Mapped[Dict[str, Any]] = mapped_column(JSON)  # Filter conditions
    
    # Segment statistics
    contact_count: Mapped[int] = mapped_column(Integer, default=0)
    last_calculated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Settings
    is_dynamic: Mapped[bool] = mapped_column(Boolean, default=True)  # Auto-update vs. static
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Metadata
    extra_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
