"""Repository for deal operations."""

import uuid
from typing import Optional, Sequence, Dict, Any
from datetime import datetime

from sqlalchemy import select, update, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.deal import Deal


class DealRepository:
    """Repository for deal operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session."""
        self.session = session
    
    async def create(self, deal: Deal) -> Deal:
        """Create a new deal."""
        self.session.add(deal)
        await self.session.commit()
        await self.session.refresh(deal)
        return deal
    
    async def get_by_id(
        self, 
        deal_id: uuid.UUID, 
        tenant_id: uuid.UUID
    ) -> Optional[Deal]:
        """Get deal by ID and tenant ID."""
        query = select(Deal).where(
            and_(
                Deal.id == deal_id,
                Deal.tenant_id == tenant_id,
                Deal.is_deleted == False
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
        stage: Optional[str] = None,
        owner_id: Optional[uuid.UUID] = None,
        contact_id: Optional[uuid.UUID] = None,
        company_id: Optional[uuid.UUID] = None
    ) -> Sequence[Deal]:
        """List deals with pagination and optional filters."""
        query = select(Deal).where(
            and_(
                Deal.tenant_id == tenant_id,
                Deal.is_deleted == False
            )
        )
        
        if search:
            search_filter = or_(
                Deal.name.ilike(f"%{search}%"),
                Deal.description.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        if stage:
            query = query.where(Deal.stage == stage)
            
        if owner_id:
            query = query.where(Deal.owner_id == owner_id)
            
        if contact_id:
            query = query.where(Deal.contact_id == contact_id)
            
        if company_id:
            query = query.where(Deal.company_id == company_id)
            
        query = query.offset(skip).limit(limit).order_by(Deal.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update(
        self, 
        deal_id: uuid.UUID,
        tenant_id: uuid.UUID,
        **kwargs
    ) -> Optional[Deal]:
        """Update deal by ID and tenant ID."""
        query = update(Deal).where(
            and_(
                Deal.id == deal_id,
                Deal.tenant_id == tenant_id,
                Deal.is_deleted == False
            )
        ).values(**kwargs)
        
        await self.session.execute(query)
        await self.session.commit()
        
        return await self.get_by_id(deal_id, tenant_id)
    
    async def soft_delete(
        self, 
        deal_id: uuid.UUID,
        tenant_id: uuid.UUID
    ) -> bool:
        """Soft delete deal by ID and tenant ID."""
        deal = await self.get_by_id(deal_id, tenant_id)
        if not deal:
            return False
            
        deal.is_deleted = True
        await self.session.commit()
        return True
    
    async def count(
        self,
        tenant_id: uuid.UUID,
        search: Optional[str] = None,
        stage: Optional[str] = None,
        owner_id: Optional[uuid.UUID] = None,
        contact_id: Optional[uuid.UUID] = None,
        company_id: Optional[uuid.UUID] = None
    ) -> int:
        """Count total number of deals with filters."""
        query = select(func.count(Deal.id)).where(
            and_(
                Deal.tenant_id == tenant_id,
                Deal.is_deleted == False
            )
        )
        
        if search:
            search_filter = or_(
                Deal.name.ilike(f"%{search}%"),
                Deal.description.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        if stage:
            query = query.where(Deal.stage == stage)
            
        if owner_id:
            query = query.where(Deal.owner_id == owner_id)
            
        if contact_id:
            query = query.where(Deal.contact_id == contact_id)
            
        if company_id:
            query = query.where(Deal.company_id == company_id)
            
        result = await self.session.execute(query)
        return result.scalar() or 0
    
    async def get_pipeline_summary(
        self,
        tenant_id: uuid.UUID,
        owner_id: Optional[uuid.UUID] = None
    ) -> Sequence[Dict[str, Any]]:
        """Get deal pipeline summary by stage."""
        query = select(
            Deal.stage,
            func.count(Deal.id).label("count"),
            func.coalesce(func.sum(Deal.amount), 0).label("total_amount"),
            func.coalesce(func.avg(Deal.amount), 0).label("average_amount")
        ).where(
            and_(
                Deal.tenant_id == tenant_id,
                Deal.is_deleted == False
            )
        ).group_by(Deal.stage)
        
        if owner_id:
            query = query.where(Deal.owner_id == owner_id)
            
        result = await self.session.execute(query)
        return [
            {
                "stage": row.stage,
                "count": row.count,
                "total_amount": float(row.total_amount),
                "average_amount": float(row.average_amount)
            }
            for row in result.all()
        ]
    
    async def get_deals_by_close_date(
        self,
        tenant_id: uuid.UUID,
        start_date: datetime,
        end_date: datetime,
        owner_id: Optional[uuid.UUID] = None
    ) -> Sequence[Deal]:
        """Get deals by expected close date range."""
        query = select(Deal).where(
            and_(
                Deal.tenant_id == tenant_id,
                Deal.is_deleted == False,
                Deal.expected_close_date.between(start_date, end_date)
            )
        )
        
        if owner_id:
            query = query.where(Deal.owner_id == owner_id)
            
        query = query.order_by(Deal.expected_close_date)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update_stage(
        self,
        deal_id: uuid.UUID,
        tenant_id: uuid.UUID,
        stage: str,
        probability: Optional[float] = None
    ) -> Optional[Deal]:
        """Update deal stage and probability."""
        update_data = {"stage": stage}
        if probability is not None:
            update_data["probability"] = probability
            
        # If closing won, set actual close date
        if stage == "closed-won":
            update_data["actual_close_date"] = datetime.utcnow()
            
        return await self.update(deal_id, tenant_id, **update_data)