"""Schemas for company request/response models."""

import uuid
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

from pydantic import BaseModel, EmailStr, HttpUrl, Field, StringConstraints


class CompanyBase(BaseModel):
    """Base schema for company data."""
    
    name: Annotated[str, StringConstraints(min_length=1, max_length=200)]
    legal_name: Annotated[str, StringConstraints(max_length=200)] | None = None
    industry: Annotated[str, StringConstraints(max_length=100)] | None = None
    company_type: Annotated[str, StringConstraints(max_length=50)] | None = None
    
    website: HttpUrl | None = None
    email: EmailStr | None = None
    phone: Annotated[str, StringConstraints(max_length=50)] | None = None
    
    address_line1: Annotated[str, StringConstraints(max_length=200)] | None = None
    address_line2: Annotated[str, StringConstraints(max_length=200)] | None = None
    city: Annotated[str, StringConstraints(max_length=100)] | None = None
    state: Annotated[str, StringConstraints(max_length=100)] | None = None
    postal_code: Annotated[str, StringConstraints(max_length=20)] | None = None
    country: Annotated[str, StringConstraints(max_length=100)] | None = None
    
    employee_count: Annotated[int, Field(ge=0)] | None = None
    annual_revenue: Annotated[float, Field(ge=0)] | None = None
    founded_year: Annotated[int, Field(ge=1800, le=2100)] | None = None
    
    linkedin: HttpUrl | None = None
    twitter: HttpUrl | None = None
    facebook: HttpUrl | None = None
    
    description: str | None = None
    tags: Annotated[str, StringConstraints(max_length=500)] | None = None
    status: Annotated[str, StringConstraints(max_length=50)] | None = None
    
    company_score: Annotated[float, Field(ge=0, le=100)] | None = None
    owner_id: uuid.UUID | None = None
    parent_company_id: uuid.UUID | None = None


class CompanyCreate(CompanyBase):
    """Schema for creating a new company."""
    pass


class CompanyUpdate(CompanyBase):
    """Schema for updating an existing company."""
    name: Annotated[str, StringConstraints(min_length=1, max_length=200)] | None = None


class Company(CompanyBase):
    """Schema for company response."""
    
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class CompanyList(BaseModel):
    """Schema for paginated company list response."""
    
    items: list[Company]
    total: int
    skip: int
    limit: int