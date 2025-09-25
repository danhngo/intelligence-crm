"""Repository for contact operations."""

import uuid
from typing import Optional, Sequence

from sqlalchemy import select, update, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import Contact


class ContactRepository:
    """Repository for contact operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session."""
        self.session = session
    
    async def create(self, contact: Contact) -> Contact:
        """Create a new contact."""
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact
    
    async def get_by_id(
        self, 
        contact_id: uuid.UUID, 
        tenant_id: uuid.UUID
    ) -> Optional[Contact]:
        """Get contact by ID and tenant ID."""
        query = select(Contact).where(
            and_(
                Contact.id == contact_id,
                Contact.tenant_id == tenant_id,
                Contact.is_deleted == False
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_email(
        self, 
        email: str, 
        tenant_id: uuid.UUID
    ) -> Optional[Contact]:
        """Get contact by email and tenant ID."""
        query = select(Contact).where(
            and_(
                Contact.email == email,
                Contact.tenant_id == tenant_id,
                Contact.is_deleted == False
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def list(
        self,
        tenant_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> Sequence[Contact]:
        """List contacts with pagination and optional search."""
        query = select(Contact).where(
            and_(
                Contact.tenant_id == tenant_id,
                Contact.is_deleted == False
            )
        )
        
        if search:
            search_filter = or_(
                Contact.first_name.ilike(f"%{search}%"),
                Contact.last_name.ilike(f"%{search}%"),
                Contact.email.ilike(f"%{search}%"),
                Contact.organization.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
            
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update(
        self, 
        contact_id: uuid.UUID,
        tenant_id: uuid.UUID,
        **kwargs
    ) -> Optional[Contact]:
        """Update contact by ID and tenant ID."""
        query = update(Contact).where(
            and_(
                Contact.id == contact_id,
                Contact.tenant_id == tenant_id,
                Contact.is_deleted == False
            )
        ).values(**kwargs)
        
        await self.session.execute(query)
        await self.session.commit()
        
        return await self.get_by_id(contact_id, tenant_id)
    
    async def soft_delete(
        self, 
        contact_id: uuid.UUID,
        tenant_id: uuid.UUID
    ) -> bool:
        """Soft delete contact by ID and tenant ID."""
        contact = await self.get_by_id(contact_id, tenant_id)
        if not contact:
            return False
            
        contact.is_deleted = True
        await self.session.commit()
        return True
    
    async def count(
        self,
        tenant_id: uuid.UUID,
        search: Optional[str] = None
    ) -> int:
        """Count total number of contacts."""
        query = select(Contact).where(
            and_(
                Contact.tenant_id == tenant_id,
                Contact.is_deleted == False
            )
        )
        
        if search:
            search_filter = or_(
                Contact.first_name.ilike(f"%{search}%"),
                Contact.last_name.ilike(f"%{search}%"),
                Contact.email.ilike(f"%{search}%"),
                Contact.organization.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
            
        result = await self.session.execute(query)
        return len(result.scalars().all())
