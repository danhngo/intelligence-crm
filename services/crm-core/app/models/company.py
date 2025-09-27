"""Company model for CRM service."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TenantModelMixin, TimestampMixin, SoftDeleteMixin


class Company(Base, TenantModelMixin, TimestampMixin, SoftDeleteMixin):
    """Company model representing organizations and businesses."""
    
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(
        String(36), 
        primary_key=True,
        default=uuid.uuid4
    )
    
    # Basic information
    name: Mapped[str] = mapped_column(String(200), index=True)
    legal_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    company_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # Corporation, LLC, etc.
    
    # Contact information
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Address
    address_line1: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Business details
    employee_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    annual_revenue: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    founded_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Social profiles
    linkedin: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    twitter: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    facebook: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # CRM fields
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Comma-separated tags
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # active, inactive, prospect
    
    # Lead scoring
    company_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Metadata
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        nullable=True,
        index=True
    )
    
    # Parent company relationship
    parent_company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        ForeignKey("companies.id"),
        nullable=True
    )
    
    def __repr__(self) -> str:
        """String representation of the company."""
        return f"<Company {self.name}>"