"""Schemas for lead request/response models."""

import uuid
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

from pydantic import BaseModel, EmailStr, HttpUrl, Field, StringConstraints


class LeadBase(BaseModel):
    """Base schema for lead data."""
    
    first_name: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    last_name: Annotated[str, StringConstraints(max_length=100)] | None = None
    title: Annotated[str, StringConstraints(max_length=100)] | None = None
    
    email: EmailStr | None = None
    phone: Annotated[str, StringConstraints(max_length=50)] | None = None
    mobile: Annotated[str, StringConstraints(max_length=50)] | None = None
    
    company: Annotated[str, StringConstraints(max_length=200)] | None = None
    company_id: uuid.UUID | None = None
    
    address_line1: Annotated[str, StringConstraints(max_length=200)] | None = None
    address_line2: Annotated[str, StringConstraints(max_length=200)] | None = None
    city: Annotated[str, StringConstraints(max_length=100)] | None = None
    state: Annotated[str, StringConstraints(max_length=100)] | None = None
    postal_code: Annotated[str, StringConstraints(max_length=20)] | None = None
    country: Annotated[str, StringConstraints(max_length=100)] | None = None
    
    status: Annotated[str, StringConstraints(max_length=50)] = "new"
    source: Annotated[str, StringConstraints(max_length=100)] | None = None
    lead_score: Annotated[float, Field(ge=0, le=100)] | None = None
    
    budget: Annotated[float, Field(ge=0)] | None = None
    interest_level: Annotated[str, StringConstraints(max_length=20)] | None = None
    
    expected_close_date: datetime | None = None
    last_contact_date: datetime | None = None
    
    linkedin: HttpUrl | None = None
    twitter: HttpUrl | None = None
    
    description: str | None = None
    tags: Annotated[str, StringConstraints(max_length=500)] | None = None
    
    owner_id: uuid.UUID | None = None
    converted_contact_id: uuid.UUID | None = None


class LeadCreate(LeadBase):
    """Schema for creating a new lead."""
    pass


class LeadUpdate(LeadBase):
    """Schema for updating an existing lead."""
    first_name: Annotated[str, StringConstraints(min_length=1, max_length=100)] | None = None


class Lead(LeadBase):
    """Schema for lead response."""
    
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class LeadList(BaseModel):
    """Schema for paginated lead list response."""
    
    items: list[Lead]
    total: int
    skip: int
    limit: int


class LeadConvert(BaseModel):
    """Schema for converting lead to contact."""
    
    create_company: bool = False
    create_deal: bool = False
    deal_name: str | None = None
    deal_amount: float | None = None
    deal_stage: str = "prospecting"