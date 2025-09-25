"""Contact model for CRM service."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TenantModelMixin, TimestampMixin, SoftDeleteMixin


class Contact(Base, TenantModelMixin, TimestampMixin, SoftDeleteMixin):
    """Contact model representing individuals or organizations."""
    
    __tablename__ = "contacts"

    id: Mapped[uuid.UUID] = mapped_column(
        String(36), 
        primary_key=True,
        default=uuid.uuid4
    )
    
    # Basic information
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    organization: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Contact information  
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    mobile: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Address
    address_line1: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Additional fields
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    twitter: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Lead scoring
    lead_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lead_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    lead_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Tags for categorization
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Comma-separated tags
    
    # Preferences
    preferred_contact_method: Mapped[Optional[str]] = mapped_column(
        String(20), 
        nullable=True,
        default="email"
    )
    opt_out: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Metadata
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        nullable=True,
        index=True
    )
    
    def __repr__(self) -> str:
        """String representation of the contact."""
        return f"{self.first_name} {self.last_name or ''}"
