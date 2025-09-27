"""Repository for lead operations."""

import uuid
from typing import Optional, Sequence
from datetime import datetime

from sqlalchemy import select, update, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead
from app.models.contact import Contact


class LeadRepository:
    """Repository for lead operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session."""
        self.session = session
    
    async def create(self, lead: Lead) -> Lead:
        """Create a new lead."""
        self.session.add(lead)
        await self.session.commit()
        await self.session.refresh(lead)
        return lead
    
    async def get_by_id(
        self, 
        lead_id: uuid.UUID, 
        tenant_id: uuid.UUID
    ) -> Optional[Lead]:
        """Get lead by ID and tenant ID."""
        query = select(Lead).where(
            and_(
                Lead.id == lead_id,
                Lead.tenant_id == tenant_id,
                Lead.is_deleted == False
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_email(
        self, 
        email: str, 
        tenant_id: uuid.UUID
    ) -> Optional[Lead]:
        """Get lead by email and tenant ID."""
        query = select(Lead).where(
            and_(
                Lead.email == email,
                Lead.tenant_id == tenant_id,
                Lead.is_deleted == False
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def list(
        self,
        tenant_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None,
        owner_id: Optional[uuid.UUID] = None
    ) -> Sequence[Lead]:
        """List leads with pagination and optional filters."""
        query = select(Lead).where(
            and_(
                Lead.tenant_id == tenant_id,
                Lead.is_deleted == False
            )
        )
        
        if search:
            search_filter = or_(
                Lead.first_name.ilike(f"%{search}%"),
                Lead.last_name.ilike(f"%{search}%"),
                Lead.email.ilike(f"%{search}%"),
                Lead.company.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        if status:
            query = query.where(Lead.status == status)
            
        if source:
            query = query.where(Lead.source == source)
            
        if owner_id:
            query = query.where(Lead.owner_id == owner_id)
            
        query = query.offset(skip).limit(limit).order_by(Lead.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update(
        self, 
        lead_id: uuid.UUID,
        tenant_id: uuid.UUID,
        **kwargs
    ) -> Optional[Lead]:
        """Update lead by ID and tenant ID."""
        query = update(Lead).where(
            and_(
                Lead.id == lead_id,
                Lead.tenant_id == tenant_id,
                Lead.is_deleted == False
            )
        ).values(**kwargs)
        
        await self.session.execute(query)
        await self.session.commit()
        
        return await self.get_by_id(lead_id, tenant_id)
    
    async def soft_delete(
        self, 
        lead_id: uuid.UUID,
        tenant_id: uuid.UUID
    ) -> bool:
        """Soft delete lead by ID and tenant ID."""
        lead = await self.get_by_id(lead_id, tenant_id)
        if not lead:
            return False
            
        lead.is_deleted = True
        await self.session.commit()
        return True
    
    async def count(
        self,
        tenant_id: uuid.UUID,
        search: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None,
        owner_id: Optional[uuid.UUID] = None
    ) -> int:
        """Count total number of leads with filters."""
        query = select(func.count(Lead.id)).where(
            and_(
                Lead.tenant_id == tenant_id,
                Lead.is_deleted == False
            )
        )
        
        if search:
            search_filter = or_(
                Lead.first_name.ilike(f"%{search}%"),
                Lead.last_name.ilike(f"%{search}%"),
                Lead.email.ilike(f"%{search}%"),
                Lead.company.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        if status:
            query = query.where(Lead.status == status)
            
        if source:
            query = query.where(Lead.source == source)
            
        if owner_id:
            query = query.where(Lead.owner_id == owner_id)
            
        result = await self.session.execute(query)
        return result.scalar() or 0
    
    async def convert_to_contact(
        self,
        lead_id: uuid.UUID,
        tenant_id: uuid.UUID
    ) -> Optional[Contact]:
        """Convert lead to contact."""
        lead = await self.get_by_id(lead_id, tenant_id)
        if not lead or lead.converted_contact_id:
            return None
        
        # Create contact from lead data
        contact = Contact(
            tenant_id=tenant_id,
            first_name=lead.first_name,
            last_name=lead.last_name,
            organization=lead.company,
            title=lead.title,
            email=lead.email,
            phone=lead.phone,
            mobile=lead.mobile,
            address_line1=lead.address_line1,
            address_line2=lead.address_line2,
            city=lead.city,
            state=lead.state,
            postal_code=lead.postal_code,
            country=lead.country,
            description=lead.description,
            linkedin=lead.linkedin,
            twitter=lead.twitter,
            lead_score=lead.lead_score,
            lead_status="converted",
            lead_source=lead.source,
            tags=lead.tags,
            owner_id=lead.owner_id
        )
        
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        
        # Update lead with converted contact ID and status
        lead.converted_contact_id = contact.id
        lead.status = "converted"
        await self.session.commit()
        
        return contact
    
    async def get_lead_sources(self, tenant_id: uuid.UUID) -> Sequence[str]:
        """Get list of unique lead sources."""
        query = select(Lead.source.distinct()).where(
            and_(
                Lead.tenant_id == tenant_id,
                Lead.is_deleted == False,
                Lead.source.isnot(None)
            )
        ).order_by(Lead.source)
        
        result = await self.session.execute(query)
        return [source for source in result.scalars().all() if source]