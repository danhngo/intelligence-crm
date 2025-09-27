"""Activity model for CRM service."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TenantModelMixin, TimestampMixin, SoftDeleteMixin


class Activity(Base, TenantModelMixin, TimestampMixin, SoftDeleteMixin):
    """Activity model representing interactions and tasks."""
    
    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(
        String(36), 
        primary_key=True,
        default=uuid.uuid4
    )
    
    # Basic information
    subject: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Activity type and status
    type: Mapped[str] = mapped_column(String(50))  # call, email, meeting, task, note, etc.
    status: Mapped[str] = mapped_column(String(50), default="open")  # open, completed, cancelled, in_progress
    priority: Mapped[str] = mapped_column(String(20), default="normal")  # low, normal, high, urgent
    
    # Timing
    due_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    start_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(nullable=True)
    
    # Completion tracking
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Relationships - polymorphic associations
    contact_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        ForeignKey("contacts.id"),
        nullable=True
    )
    
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        ForeignKey("companies.id"),
        nullable=True
    )
    
    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        ForeignKey("leads.id"),
        nullable=True
    )
    
    deal_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        ForeignKey("deals.id"),
        nullable=True
    )
    
    # Activity ownership
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        nullable=True,
        index=True
    )
    
    assigned_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        nullable=True,
        index=True
    )
    
    # Meeting/Call specific fields
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    meeting_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    attendees: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)  # JSON or comma-separated emails
    
    # Email specific fields
    email_from: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email_to: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)  # Comma-separated emails
    email_cc: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    email_bcc: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    
    # Task specific fields
    reminder_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    reminder_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Outcome and follow-up
    outcome: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # successful, no_answer, busy, etc.
    follow_up_required: Mapped[bool] = mapped_column(Boolean, default=False)
    follow_up_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Additional fields
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Comma-separated tags
    
    def __repr__(self) -> str:
        """String representation of the activity."""
        return f"<Activity {self.type}: {self.subject} - {self.status}>"