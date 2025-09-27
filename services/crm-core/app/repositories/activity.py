"""Repository for activity operations."""

import uuid
from typing import Optional, Sequence, Dict, Any
from datetime import datetime, timedelta

from sqlalchemy import select, update, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity


class ActivityRepository:
    """Repository for activity operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session."""
        self.session = session
    
    async def create(self, activity: Activity) -> Activity:
        """Create a new activity."""
        self.session.add(activity)
        await self.session.commit()
        await self.session.refresh(activity)
        return activity
    
    async def get_by_id(
        self, 
        activity_id: uuid.UUID, 
        tenant_id: uuid.UUID
    ) -> Optional[Activity]:
        """Get activity by ID and tenant ID."""
        query = select(Activity).where(
            and_(
                Activity.id == activity_id,
                Activity.tenant_id == tenant_id,
                Activity.is_deleted == False
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
        type_filter: Optional[str] = None,
        status: Optional[str] = None,
        owner_id: Optional[uuid.UUID] = None,
        assigned_to_id: Optional[uuid.UUID] = None,
        contact_id: Optional[uuid.UUID] = None,
        company_id: Optional[uuid.UUID] = None,
        lead_id: Optional[uuid.UUID] = None,
        deal_id: Optional[uuid.UUID] = None
    ) -> Sequence[Activity]:
        """List activities with pagination and optional filters."""
        query = select(Activity).where(
            and_(
                Activity.tenant_id == tenant_id,
                Activity.is_deleted == False
            )
        )
        
        if search:
            search_filter = or_(
                Activity.subject.ilike(f"%{search}%"),
                Activity.description.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        if type_filter:
            query = query.where(Activity.type == type_filter)
            
        if status:
            query = query.where(Activity.status == status)
            
        if owner_id:
            query = query.where(Activity.owner_id == owner_id)
            
        if assigned_to_id:
            query = query.where(Activity.assigned_to_id == assigned_to_id)
            
        if contact_id:
            query = query.where(Activity.contact_id == contact_id)
            
        if company_id:
            query = query.where(Activity.company_id == company_id)
            
        if lead_id:
            query = query.where(Activity.lead_id == lead_id)
            
        if deal_id:
            query = query.where(Activity.deal_id == deal_id)
            
        query = query.offset(skip).limit(limit).order_by(Activity.due_date.desc().nullslast(), Activity.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update(
        self, 
        activity_id: uuid.UUID,
        tenant_id: uuid.UUID,
        **kwargs
    ) -> Optional[Activity]:
        """Update activity by ID and tenant ID."""
        query = update(Activity).where(
            and_(
                Activity.id == activity_id,
                Activity.tenant_id == tenant_id,
                Activity.is_deleted == False
            )
        ).values(**kwargs)
        
        await self.session.execute(query)
        await self.session.commit()
        
        return await self.get_by_id(activity_id, tenant_id)
    
    async def soft_delete(
        self, 
        activity_id: uuid.UUID,
        tenant_id: uuid.UUID
    ) -> bool:
        """Soft delete activity by ID and tenant ID."""
        activity = await self.get_by_id(activity_id, tenant_id)
        if not activity:
            return False
            
        activity.is_deleted = True
        await self.session.commit()
        return True
    
    async def count(
        self,
        tenant_id: uuid.UUID,
        search: Optional[str] = None,
        type_filter: Optional[str] = None,
        status: Optional[str] = None,
        owner_id: Optional[uuid.UUID] = None,
        assigned_to_id: Optional[uuid.UUID] = None,
        contact_id: Optional[uuid.UUID] = None,
        company_id: Optional[uuid.UUID] = None,
        lead_id: Optional[uuid.UUID] = None,
        deal_id: Optional[uuid.UUID] = None
    ) -> int:
        """Count total number of activities with filters."""
        query = select(func.count(Activity.id)).where(
            and_(
                Activity.tenant_id == tenant_id,
                Activity.is_deleted == False
            )
        )
        
        if search:
            search_filter = or_(
                Activity.subject.ilike(f"%{search}%"),
                Activity.description.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        if type_filter:
            query = query.where(Activity.type == type_filter)
            
        if status:
            query = query.where(Activity.status == status)
            
        if owner_id:
            query = query.where(Activity.owner_id == owner_id)
            
        if assigned_to_id:
            query = query.where(Activity.assigned_to_id == assigned_to_id)
            
        if contact_id:
            query = query.where(Activity.contact_id == contact_id)
            
        if company_id:
            query = query.where(Activity.company_id == company_id)
            
        if lead_id:
            query = query.where(Activity.lead_id == lead_id)
            
        if deal_id:
            query = query.where(Activity.deal_id == deal_id)
            
        result = await self.session.execute(query)
        return result.scalar() or 0
    
    async def complete_activity(
        self,
        activity_id: uuid.UUID,
        tenant_id: uuid.UUID,
        outcome: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Optional[Activity]:
        """Mark activity as completed."""
        update_data = {
            "completed": True,
            "completed_at": datetime.utcnow(),
            "status": "completed"
        }
        
        if outcome:
            update_data["outcome"] = outcome
            
        if notes:
            # Append notes to description
            activity = await self.get_by_id(activity_id, tenant_id)
            if activity and activity.description:
                update_data["description"] = f"{activity.description}\n\nCompletion Notes: {notes}"
            else:
                update_data["description"] = f"Completion Notes: {notes}"
        
        return await self.update(activity_id, tenant_id, **update_data)
    
    async def get_overdue_activities(
        self,
        tenant_id: uuid.UUID,
        owner_id: Optional[uuid.UUID] = None
    ) -> Sequence[Activity]:
        """Get overdue activities."""
        now = datetime.utcnow()
        query = select(Activity).where(
            and_(
                Activity.tenant_id == tenant_id,
                Activity.is_deleted == False,
                Activity.completed == False,
                Activity.due_date < now
            )
        )
        
        if owner_id:
            query = query.where(
                or_(
                    Activity.owner_id == owner_id,
                    Activity.assigned_to_id == owner_id
                )
            )
            
        query = query.order_by(Activity.due_date)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_activities_summary(
        self,
        tenant_id: uuid.UUID,
        owner_id: Optional[uuid.UUID] = None
    ) -> Dict[str, int]:
        """Get activity summary statistics."""
        base_filter = and_(
            Activity.tenant_id == tenant_id,
            Activity.is_deleted == False
        )
        
        if owner_id:
            owner_filter = or_(
                Activity.owner_id == owner_id,
                Activity.assigned_to_id == owner_id
            )
            base_filter = and_(base_filter, owner_filter)
        
        # Total activities
        total_query = select(func.count(Activity.id)).where(base_filter)
        total_result = await self.session.execute(total_query)
        total_activities = total_result.scalar() or 0
        
        # Completed activities
        completed_query = select(func.count(Activity.id)).where(
            and_(base_filter, Activity.completed == True)
        )
        completed_result = await self.session.execute(completed_query)
        completed_activities = completed_result.scalar() or 0
        
        # Overdue activities
        now = datetime.utcnow()
        overdue_query = select(func.count(Activity.id)).where(
            and_(
                base_filter,
                Activity.completed == False,
                Activity.due_date < now
            )
        )
        overdue_result = await self.session.execute(overdue_query)
        overdue_activities = overdue_result.scalar() or 0
        
        # Today's activities
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        today_query = select(func.count(Activity.id)).where(
            and_(
                base_filter,
                Activity.due_date.between(today_start, today_end)
            )
        )
        today_result = await self.session.execute(today_query)
        today_activities = today_result.scalar() or 0
        
        # This week's activities
        week_start = today_start - timedelta(days=today_start.weekday())
        week_end = week_start + timedelta(days=7)
        week_query = select(func.count(Activity.id)).where(
            and_(
                base_filter,
                Activity.due_date.between(week_start, week_end)
            )
        )
        week_result = await self.session.execute(week_query)
        this_week_activities = week_result.scalar() or 0
        
        return {
            "total_activities": total_activities,
            "completed_activities": completed_activities,
            "overdue_activities": overdue_activities,
            "today_activities": today_activities,
            "this_week_activities": this_week_activities
        }