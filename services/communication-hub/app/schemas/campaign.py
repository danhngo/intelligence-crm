"""Campaign and email tracking schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.campaign import CampaignType, CampaignStatus, EmailEventType


# Campaign Schemas
class CampaignBase(BaseModel):
    """Base campaign schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    type: CampaignType
    scheduled_at: Optional[datetime] = None
    target_segments: List[str] = Field(default_factory=list)
    contact_list_ids: List[str] = Field(default_factory=list)
    template_id: Optional[UUID] = None
    subject_line: Optional[str] = Field(None, max_length=255)
    sender_name: Optional[str] = Field(None, max_length=100)
    sender_email: Optional[EmailStr] = None
    tracking_enabled: bool = True
    click_tracking_enabled: bool = True
    open_tracking_enabled: bool = True
    unsubscribe_enabled: bool = True
    config: Dict[str, Any] = Field(default_factory=dict)
    extra_data: Dict[str, Any] = Field(default_factory=dict)


class CampaignCreate(CampaignBase):
    """Create campaign schema."""
    pass


class CampaignUpdate(BaseModel):
    """Update campaign schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[CampaignStatus] = None
    scheduled_at: Optional[datetime] = None
    target_segments: Optional[List[str]] = None
    contact_list_ids: Optional[List[str]] = None
    template_id: Optional[UUID] = None
    subject_line: Optional[str] = Field(None, max_length=255)
    sender_name: Optional[str] = Field(None, max_length=100)
    sender_email: Optional[EmailStr] = None
    tracking_enabled: Optional[bool] = None
    click_tracking_enabled: Optional[bool] = None
    open_tracking_enabled: Optional[bool] = None
    unsubscribe_enabled: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None
    extra_data: Optional[Dict[str, Any]] = None


class Campaign(CampaignBase):
    """Campaign response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    status: CampaignStatus
    tenant_id: UUID
    created_by: UUID
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_recipients: int = 0
    sent_count: int = 0
    delivered_count: int = 0
    opened_count: int = 0
    clicked_count: int = 0
    bounced_count: int = 0
    complained_count: int = 0
    unsubscribed_count: int = 0
    created_at: datetime
    updated_at: datetime


class CampaignStats(BaseModel):
    """Campaign statistics schema."""
    total_recipients: int
    sent_count: int
    delivered_count: int
    opened_count: int
    clicked_count: int
    bounced_count: int
    complained_count: int
    unsubscribed_count: int
    
    # Calculated rates
    delivery_rate: float = Field(..., description="Delivered / Sent")
    open_rate: float = Field(..., description="Opens / Delivered")
    click_rate: float = Field(..., description="Clicks / Delivered")
    click_to_open_rate: float = Field(..., description="Clicks / Opens")
    bounce_rate: float = Field(..., description="Bounces / Sent")
    complaint_rate: float = Field(..., description="Complaints / Delivered")
    unsubscribe_rate: float = Field(..., description="Unsubscribes / Delivered")


# Campaign Message Schemas
class CampaignMessageBase(BaseModel):
    """Base campaign message schema."""
    recipient_email: EmailStr
    recipient_contact_id: Optional[UUID] = None
    subject_line: str = Field(..., max_length=255)
    html_content: Optional[str] = None
    text_content: Optional[str] = None
    personalization_data: Dict[str, Any] = Field(default_factory=dict)


class CampaignMessageCreate(CampaignMessageBase):
    """Create campaign message schema."""
    campaign_id: UUID


class CampaignMessage(CampaignMessageBase):
    """Campaign message response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    campaign_id: UUID
    message_id: Optional[UUID] = None
    tracking_id: str
    status: str
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    created_at: datetime
    updated_at: datetime


# Email Tracking Schemas
class EmailTrackingEventCreate(BaseModel):
    """Create email tracking event schema."""
    event_type: EmailEventType
    tracking_id: str
    recipient_email: EmailStr
    url: Optional[str] = None
    link_id: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    country: Optional[str] = Field(None, max_length=2)
    region: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    device_type: Optional[str] = Field(None, max_length=50)
    client_name: Optional[str] = Field(None, max_length=100)
    client_version: Optional[str] = Field(None, max_length=50)
    extra_data: Dict[str, Any] = Field(default_factory=dict)


class EmailTrackingEvent(EmailTrackingEventCreate):
    """Email tracking event response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    campaign_id: Optional[UUID] = None
    campaign_message_id: Optional[UUID] = None
    message_id: Optional[UUID] = None
    event_timestamp: datetime
    created_at: datetime
    updated_at: datetime


# Email Template Schemas
class EmailTemplateBase(BaseModel):
    """Base email template schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    subject_template: str = Field(..., max_length=255)
    html_template: Optional[str] = None
    text_template: Optional[str] = None
    variables: List[str] = Field(default_factory=list)
    sample_data: Dict[str, Any] = Field(default_factory=dict)
    category: Optional[str] = Field(None, max_length=100)
    tags: List[str] = Field(default_factory=list)
    extra_data: Dict[str, Any] = Field(default_factory=dict)


class EmailTemplateCreate(EmailTemplateBase):
    """Create email template schema."""
    pass


class EmailTemplateUpdate(BaseModel):
    """Update email template schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    subject_template: Optional[str] = Field(None, max_length=255)
    html_template: Optional[str] = None
    text_template: Optional[str] = None
    variables: Optional[List[str]] = None
    sample_data: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    extra_data: Optional[Dict[str, Any]] = None


class EmailTemplate(EmailTemplateBase):
    """Email template response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    tenant_id: UUID
    created_by: UUID
    is_active: bool = True
    usage_count: int = 0
    last_used_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


# Contact Segment Schemas
class ContactSegmentBase(BaseModel):
    """Base contact segment schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    criteria: Dict[str, Any] = Field(..., description="Segment filter criteria")
    is_dynamic: bool = True
    is_active: bool = True
    extra_data: Dict[str, Any] = Field(default_factory=dict)


class ContactSegmentCreate(ContactSegmentBase):
    """Create contact segment schema."""
    pass


class ContactSegmentUpdate(BaseModel):
    """Update contact segment schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    criteria: Optional[Dict[str, Any]] = None
    is_dynamic: Optional[bool] = None
    is_active: Optional[bool] = None
    extra_data: Optional[Dict[str, Any]] = None


class ContactSegment(ContactSegmentBase):
    """Contact segment response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    tenant_id: UUID
    created_by: UUID
    contact_count: int = 0
    last_calculated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


# List Schemas
class CampaignList(BaseModel):
    """Campaign list response schema."""
    items: List[Campaign]
    total: int
    skip: int
    limit: int


class CampaignMessageList(BaseModel):
    """Campaign message list response schema."""
    items: List[CampaignMessage]
    total: int
    skip: int
    limit: int


class EmailTrackingEventList(BaseModel):
    """Email tracking event list response schema."""
    items: List[EmailTrackingEvent]
    total: int
    skip: int
    limit: int


class EmailTemplateList(BaseModel):
    """Email template list response schema."""
    items: List[EmailTemplate]
    total: int
    skip: int
    limit: int


class ContactSegmentList(BaseModel):
    """Contact segment list response schema."""
    items: List[ContactSegment]
    total: int
    skip: int
    limit: int


# Bulk Operations Schemas
class BulkCampaignAction(BaseModel):
    """Bulk campaign action schema."""
    action: str = Field(..., pattern="^(start|pause|stop|delete)$")
    campaign_ids: List[UUID] = Field(..., min_items=1)


class BulkActionResult(BaseModel):
    """Bulk action result schema."""
    success_count: int
    failed_count: int
    errors: List[Dict[str, Any]] = Field(default_factory=list)


# Real-time Tracking Schemas
class TrackingPixelResponse(BaseModel):
    """Tracking pixel response schema."""
    success: bool
    tracking_id: str
    timestamp: datetime


class LinkClickRedirect(BaseModel):
    """Link click redirect schema."""
    success: bool
    tracking_id: str
    redirect_url: str
    timestamp: datetime
