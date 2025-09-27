"""Schemas for request/response models."""

import uuid
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

from pydantic import (
    BaseModel, EmailStr, HttpUrl, 
    Field, BeforeValidator, StringConstraints
)

from app.core.config import settings


class ContactBase(BaseModel):
    """Base schema for contact data."""
    
    first_name: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    last_name: Annotated[str, StringConstraints(max_length=100)] | None = None
    organization: Annotated[str, StringConstraints(max_length=200)] | None = None
    title: Annotated[str, StringConstraints(max_length=100)] | None = None
    
    email: EmailStr | None = None
    phone: Annotated[str, StringConstraints(max_length=50)] | None = None
    mobile: Annotated[str, StringConstraints(max_length=50)] | None = None
    
    address_line1: Annotated[str, StringConstraints(max_length=200)] | None = None
    address_line2: Annotated[str, StringConstraints(max_length=200)] | None = None
    city: Annotated[str, StringConstraints(max_length=100)] | None = None
    state: Annotated[str, StringConstraints(max_length=100)] | None = None
    postal_code: Annotated[str, StringConstraints(max_length=20)] | None = None
    country: Annotated[str, StringConstraints(max_length=100)] | None = None
    
    description: Annotated[str, StringConstraints(max_length=1000)] | None = None
    website: HttpUrl | None = None
    linkedin: HttpUrl | None = None
    twitter: HttpUrl | None = None
    
    lead_score: Annotated[float, Field(ge=settings.MIN_CONTACT_SCORE, le=settings.MAX_CONTACT_SCORE)] | None = None
    lead_status: Annotated[str, StringConstraints(max_length=50)] | None = None
    lead_source: Annotated[str, StringConstraints(max_length=100)] | None = None
    
    tags: Annotated[str, StringConstraints(max_length=500)] | None = None
    
    preferred_contact_method: Annotated[str, StringConstraints(max_length=20)] | None = None
    opt_out: bool = False
    
    owner_id: uuid.UUID | None = None


class ContactCreate(ContactBase):
    """Schema for creating a new contact."""
    pass


class ContactUpdate(ContactBase):
    """Schema for updating an existing contact."""
    pass


class Contact(ContactBase):
    """Schema for contact response."""
    
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ContactList(BaseModel):
    """Schema for paginated contact list response."""
    
    items: list[Contact]
    total: int
    skip: int
    limit: int
