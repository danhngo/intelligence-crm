"""Repository for company operations."""

import uuid
from typing import Optional, Sequence

from sqlalchemy import select, update, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company


class CompanyRepository:
    """Repository for company operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session."""
        self.session = session
    
    async def create(self, company: Company) -> Company:
        """Create a new company."""
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company
    
    async def get_by_id(
        self, 
        company_id: uuid.UUID, 
        tenant_id: uuid.UUID
    ) -> Optional[Company]:
        """Get company by ID and tenant ID."""
        query = select(Company).where(
            and_(
                Company.id == company_id,
                Company.tenant_id == tenant_id,
                Company.is_deleted == False
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_name(
        self, 
        name: str, 
        tenant_id: uuid.UUID
    ) -> Optional[Company]:
        """Get company by name and tenant ID."""
        query = select(Company).where(
            and_(
                Company.name == name,
                Company.tenant_id == tenant_id,
                Company.is_deleted == False
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
        industry: Optional[str] = None,
        status: Optional[str] = None
    ) -> Sequence[Company]:
        """List companies with pagination and optional filters."""
        query = select(Company).where(
            and_(
                Company.tenant_id == tenant_id,
                Company.is_deleted == False
            )
        )
        
        if search:
            search_filter = or_(
                Company.name.ilike(f"%{search}%"),
                Company.legal_name.ilike(f"%{search}%"),
                Company.industry.ilike(f"%{search}%"),
                Company.email.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        if industry:
            query = query.where(Company.industry == industry)
            
        if status:
            query = query.where(Company.status == status)
            
        query = query.offset(skip).limit(limit).order_by(Company.name)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update(
        self, 
        company_id: uuid.UUID,
        tenant_id: uuid.UUID,
        **kwargs
    ) -> Optional[Company]:
        """Update company by ID and tenant ID."""
        query = update(Company).where(
            and_(
                Company.id == company_id,
                Company.tenant_id == tenant_id,
                Company.is_deleted == False
            )
        ).values(**kwargs)
        
        await self.session.execute(query)
        await self.session.commit()
        
        return await self.get_by_id(company_id, tenant_id)
    
    async def soft_delete(
        self, 
        company_id: uuid.UUID,
        tenant_id: uuid.UUID
    ) -> bool:
        """Soft delete company by ID and tenant ID."""
        company = await self.get_by_id(company_id, tenant_id)
        if not company:
            return False
            
        company.is_deleted = True
        await self.session.commit()
        return True
    
    async def count(
        self,
        tenant_id: uuid.UUID,
        search: Optional[str] = None,
        industry: Optional[str] = None,
        status: Optional[str] = None
    ) -> int:
        """Count total number of companies with filters."""
        query = select(func.count(Company.id)).where(
            and_(
                Company.tenant_id == tenant_id,
                Company.is_deleted == False
            )
        )
        
        if search:
            search_filter = or_(
                Company.name.ilike(f"%{search}%"),
                Company.legal_name.ilike(f"%{search}%"),
                Company.industry.ilike(f"%{search}%"),
                Company.email.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        if industry:
            query = query.where(Company.industry == industry)
            
        if status:
            query = query.where(Company.status == status)
            
        result = await self.session.execute(query)
        return result.scalar() or 0
    
    async def get_industries(self, tenant_id: uuid.UUID) -> Sequence[str]:
        """Get list of unique industries."""
        query = select(Company.industry.distinct()).where(
            and_(
                Company.tenant_id == tenant_id,
                Company.is_deleted == False,
                Company.industry.isnot(None)
            )
        ).order_by(Company.industry)
        
        result = await self.session.execute(query)
        return [industry for industry in result.scalars().all() if industry]