"""User models."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    """User model."""
    
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Relationships
    roles = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users"
    )
    
    def __repr__(self) -> str:
        """String representation."""
        return f"{self.email} ({self.first_name} {self.last_name})"


class Role(Base, UUIDMixin, TimestampMixin):
    """Role model."""
    
    __tablename__ = "roles"
    
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Relationships
    users = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles"
    )
    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles"
    )
    
    def __repr__(self) -> str:
        """String representation."""
        return self.name


class Permission(Base, UUIDMixin, TimestampMixin):
    """Permission model."""
    
    __tablename__ = "permissions"
    
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Relationships
    roles = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions"
    )
    
    def __repr__(self) -> str:
        """String representation."""
        return self.name


# Association tables
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id",
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "role_id",
        String(36),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_id",
        String(36),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "permission_id",
        String(36),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True
    )
)
