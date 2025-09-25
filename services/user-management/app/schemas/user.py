"""API schemas."""

import uuid
from datetime import datetime
from typing import List, Optional
from typing_extensions import Annotated

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# User schemas
class UserBase(BaseModel):
    """Base user schema."""
    
    email: EmailStr
    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str, Field(min_length=1, max_length=100)]
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a user."""
    
    password: Annotated[str, Field(min_length=8)]


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    
    email: Optional[EmailStr] = None
    first_name: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    last_name: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    password: Optional[Annotated[str, Field(min_length=8)]] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """Schema for user in database."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    is_superuser: bool
    email_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class User(UserInDB):
    """Schema for user response."""
    
    roles: List["Role"] = []


# Role schemas
class RoleBase(BaseModel):
    """Base role schema."""
    
    name: Annotated[str, Field(min_length=1, max_length=100)]
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Schema for creating a role."""
    
    permissions: List[uuid.UUID] = []


class RoleUpdate(BaseModel):
    """Schema for updating a role."""
    
    name: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    description: Optional[str] = None
    permissions: Optional[List[uuid.UUID]] = None


class RoleInDB(RoleBase):
    """Schema for role in database."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class Role(RoleInDB):
    """Schema for role response."""
    
    permissions: List["Permission"] = []


# Permission schemas
class PermissionBase(BaseModel):
    """Base permission schema."""
    
    name: Annotated[str, Field(min_length=1, max_length=100)]
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    """Schema for creating a permission."""
    pass


class PermissionUpdate(BaseModel):
    """Schema for updating a permission."""
    
    name: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    description: Optional[str] = None


class Permission(PermissionBase):
    """Schema for permission response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# Auth schemas
class Token(BaseModel):
    """Schema for token response."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for token payload."""
    
    sub: str
    exp: datetime


class LoginRequest(BaseModel):
    """Schema for login request."""
    
    email: EmailStr
    password: str
