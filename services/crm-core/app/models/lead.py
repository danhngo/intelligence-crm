"""Lead model for CRM service."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TenantModelMixin, TimestampMixin, SoftDeleteMixin


class Lead(Base, TenantModelMixin, TimestampMixin, SoftDeleteMixin):
    """Lead model representing potential customers."""
    
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(
        String(36), 
        primary_key=True,
        default=uuid.uuid4
    )
    
    # Basic information
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Contact information
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    mobile: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Company information
    company: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        ForeignKey("companies.id"),
        nullable=True
    )
    
    # Address
    address_line1: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Lead qualification
    status: Mapped[str] = mapped_column(String(50), default="new")  # new, qualified, nurturing, converted, lost
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # website, referral, campaign, etc.
    lead_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Interest and budget
    budget: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    interest_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # hot, warm, cold
    
    # Timeline
    expected_close_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_contact_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Social profiles
    linkedin: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    twitter: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Additional fields
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Comma-separated tags
    
    # Metadata
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        nullable=True,
        index=True
    )
    
    # Conversion tracking
    converted_contact_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        ForeignKey("contacts.id"),
        nullable=True
    )
    
    def __repr__(self) -> str:
        """String representation of the lead."""
        return f"<Lead {self.first_name} {self.last_name or ''} - {self.status}>"