"""Deal model for CRM service."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TenantModelMixin, TimestampMixin, SoftDeleteMixin


class Deal(Base, TenantModelMixin, TimestampMixin, SoftDeleteMixin):
    """Deal model representing sales opportunities."""
    
    __tablename__ = "deals"

    id: Mapped[uuid.UUID] = mapped_column(
        String(36), 
        primary_key=True,
        default=uuid.uuid4
    )
    
    # Basic information
    name: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Financial information
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD")  # ISO 4217 currency code
    
    # Deal progression
    stage: Mapped[str] = mapped_column(String(50), default="prospecting")  # prospecting, qualification, proposal, negotiation, closed-won, closed-lost
    probability: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 0-100%
    
    # Timeline
    expected_close_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    actual_close_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Relationships
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
    
    # Deal source
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # inbound, outbound, referral, etc.
    
    # Deal type and category
    deal_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # new_business, upsell, renewal
    product_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Competition and risk
    competitors: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Comma-separated
    risk_factors: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Additional fields
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Comma-separated tags
    
    # Metadata
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        String(36),
        nullable=True,
        index=True
    )
    
    # Deal team
    team_members: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Comma-separated user IDs
    
    # Forecasting
    forecast_category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # commit, best_case, pipeline, omitted
    
    def __repr__(self) -> str:
        """String representation of the deal."""
        return f"<Deal {self.name} - {self.stage} - ${self.amount or 0}>"