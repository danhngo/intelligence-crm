"""Base Database Model

This module defines the base SQLAlchemy model with common fields and behaviors
for multi-tenant data isolation.
"""

import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, String, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    """Base class for all database models."""
    
    # Enable automatic table naming
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name."""
        return cls.__name__.lower()
    
    # Common columns for all models
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Tenant ID for data isolation
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Enable SQLAlchemy automatic serialization
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self) -> str:
        """String representation of model instance."""
        return f"<{self.__class__.__name__}(id={self.id})>"


# SQLAlchemy event listeners for tenant isolation
@event.listens_for(Session, "before_flush")
def enforce_tenant_isolation(session: Session, *args: Any) -> None:
    """Ensure all models have tenant_id set before saving."""
    for obj in session.new:
        if hasattr(obj, "tenant_id"):
            # Get tenant ID from session info
            tenant_id = session.info.get("tenant_id")
            if not tenant_id:
                raise ValueError("Tenant ID is required but not set in session")
            
            # Set tenant ID if not already set
            if not obj.tenant_id:
                obj.tenant_id = tenant_id
