"""Schemas for activity request/response models."""

import uuid
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

from pydantic import BaseModel, Field, StringConstraints, EmailStr


class ActivityBase(BaseModel):
    """Base schema for activity data."""
    
    subject: Annotated[str, StringConstraints(min_length=1, max_length=200)]
    description: str | None = None
    
    type: Annotated[str, StringConstraints(max_length=50)]  # call, email, meeting, task, note
    status: Annotated[str, StringConstraints(max_length=50)] = "open"
    priority: Annotated[str, StringConstraints(max_length=20)] = "normal"
    
    due_date: datetime | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_minutes: Annotated[int, Field(ge=0)] | None = None
    
    completed: bool = False
    completed_at: datetime | None = None
    
    # Relationships
    contact_id: uuid.UUID | None = None
    company_id: uuid.UUID | None = None
    lead_id: uuid.UUID | None = None
    deal_id: uuid.UUID | None = None
    
    owner_id: uuid.UUID | None = None
    assigned_to_id: uuid.UUID | None = None
    
    # Meeting/Call fields
    location: Annotated[str, StringConstraints(max_length=200)] | None = None
    meeting_url: Annotated[str, StringConstraints(max_length=500)] | None = None
    attendees: str | None = None
    
    # Email fields
    email_from: EmailStr | None = None
    email_to: str | None = None
    email_cc: str | None = None
    email_bcc: str | None = None
    
    # Task fields
    reminder_date: datetime | None = None
    reminder_sent: bool = False
    
    # Outcome fields
    outcome: Annotated[str, StringConstraints(max_length=100)] | None = None
    follow_up_required: bool = False
    follow_up_date: datetime | None = None
    
    tags: Annotated[str, StringConstraints(max_length=500)] | None = None


class ActivityCreate(ActivityBase):
    """Schema for creating a new activity."""
    pass


class ActivityUpdate(ActivityBase):
    """Schema for updating an existing activity."""
    subject: Annotated[str, StringConstraints(min_length=1, max_length=200)] | None = None
    type: Annotated[str, StringConstraints(max_length=50)] | None = None


class Activity(ActivityBase):
    """Schema for activity response."""
    
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ActivityList(BaseModel):
    """Schema for paginated activity list response."""
    
    items: list[Activity]
    total: int
    skip: int
    limit: int


class ActivityComplete(BaseModel):
    """Schema for completing an activity."""
    
    outcome: Annotated[str, StringConstraints(max_length=100)] | None = None
    notes: str | None = None
    follow_up_required: bool = False
    follow_up_date: datetime | None = None


class ActivitySummary(BaseModel):
    """Schema for activity summary/statistics."""
    
    total_activities: int
    completed_activities: int
    overdue_activities: int
    today_activities: int
    this_week_activities: int