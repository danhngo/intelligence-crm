"""Schemas for deal request/response models."""

import uuid
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

from pydantic import BaseModel, Field, StringConstraints


class DealBase(BaseModel):
    """Base schema for deal data."""
    
    name: Annotated[str, StringConstraints(min_length=1, max_length=200)]
    description: str | None = None
    
    amount: Annotated[float, Field(ge=0)] | None = None
    currency: Annotated[str, StringConstraints(min_length=3, max_length=3)] = "USD"
    
    stage: Annotated[str, StringConstraints(max_length=50)] = "prospecting"
    probability: Annotated[float, Field(ge=0, le=100)] | None = None
    
    expected_close_date: datetime | None = None
    actual_close_date: datetime | None = None
    
    contact_id: uuid.UUID | None = None
    company_id: uuid.UUID | None = None
    lead_id: uuid.UUID | None = None
    
    source: Annotated[str, StringConstraints(max_length=100)] | None = None
    deal_type: Annotated[str, StringConstraints(max_length=50)] | None = None
    product_category: Annotated[str, StringConstraints(max_length=100)] | None = None
    
    competitors: Annotated[str, StringConstraints(max_length=500)] | None = None
    risk_factors: str | None = None
    
    tags: Annotated[str, StringConstraints(max_length=500)] | None = None
    owner_id: uuid.UUID | None = None
    team_members: Annotated[str, StringConstraints(max_length=500)] | None = None
    forecast_category: Annotated[str, StringConstraints(max_length=20)] | None = None


class DealCreate(DealBase):
    """Schema for creating a new deal."""
    pass


class DealUpdate(DealBase):
    """Schema for updating an existing deal."""
    name: Annotated[str, StringConstraints(min_length=1, max_length=200)] | None = None


class Deal(DealBase):
    """Schema for deal response."""
    
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class DealList(BaseModel):
    """Schema for paginated deal list response."""
    
    items: list[Deal]
    total: int
    skip: int
    limit: int


class DealStageUpdate(BaseModel):
    """Schema for updating deal stage."""
    
    stage: Annotated[str, StringConstraints(max_length=50)]
    probability: Annotated[float, Field(ge=0, le=100)] | None = None
    notes: str | None = None


class DealPipeline(BaseModel):
    """Schema for deal pipeline summary."""
    
    stage: str
    count: int
    total_amount: float
    average_amount: float