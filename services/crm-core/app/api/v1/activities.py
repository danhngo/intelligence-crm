"""Activity API endpoints."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.activity import Activity as ActivityModel
from app.repositories.activity import ActivityRepository
from app.schemas.activity import (
    Activity, ActivityCreate, ActivityList, ActivityUpdate, 
    ActivityComplete, ActivitySummary
)

router = APIRouter()


@router.post("/", response_model=Activity)
async def create_activity(
    activity: ActivityCreate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ActivityModel:
    """Create a new activity."""
    # Create activity model
    activity_data = activity.model_dump()
    db_activity = ActivityModel(tenant_id=tenant_id, **activity_data)
    
    # Save to database
    repo = ActivityRepository(db)
    return await repo.create(db_activity)


@router.get("/", response_model=ActivityList)
async def list_activities(
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query()] = None,
    type: Annotated[str | None, Query()] = None,
    status: Annotated[str | None, Query()] = None,
    owner_id: Annotated[uuid.UUID | None, Query()] = None,
    assigned_to_id: Annotated[uuid.UUID | None, Query()] = None,
    contact_id: Annotated[uuid.UUID | None, Query()] = None,
    company_id: Annotated[uuid.UUID | None, Query()] = None,
    lead_id: Annotated[uuid.UUID | None, Query()] = None,
    deal_id: Annotated[uuid.UUID | None, Query()] = None
) -> ActivityList:
    """List activities with pagination and search."""
    repo = ActivityRepository(db)
    
    # Get activities and total count
    activities = await repo.list(
        tenant_id, skip, limit, search, type, status, owner_id, 
        assigned_to_id, contact_id, company_id, lead_id, deal_id
    )
    total = await repo.count(
        tenant_id, search, type, status, owner_id,
        assigned_to_id, contact_id, company_id, lead_id, deal_id
    )
    
    return ActivityList(
        items=activities,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{activity_id}", response_model=Activity)
async def get_activity(
    activity_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ActivityModel:
    """Get a specific activity by ID."""
    repo = ActivityRepository(db)
    activity = await repo.get_by_id(activity_id, tenant_id)
    
    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )
        
    return activity


@router.patch("/{activity_id}", response_model=Activity)
async def update_activity(
    activity_id: Annotated[uuid.UUID, Path()],
    activity: ActivityUpdate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ActivityModel:
    """Update an activity."""
    repo = ActivityRepository(db)
    
    # Check if activity exists
    existing = await repo.get_by_id(activity_id, tenant_id)
    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )
    
    # Update activity
    updated = await repo.update(
        activity_id,
        tenant_id,
        **activity.model_dump(exclude_unset=True)
    )
    
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )
        
    return updated


@router.delete("/{activity_id}", status_code=204)
async def delete_activity(
    activity_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    """Delete an activity."""
    repo = ActivityRepository(db)
    
    # Try to delete the activity
    deleted = await repo.soft_delete(activity_id, tenant_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )


@router.post("/{activity_id}/complete", response_model=Activity)
async def complete_activity(
    activity_id: Annotated[uuid.UUID, Path()],
    completion_data: ActivityComplete,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ActivityModel:
    """Mark an activity as completed."""
    repo = ActivityRepository(db)
    
    # Check if activity exists
    existing = await repo.get_by_id(activity_id, tenant_id)
    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )
    
    if existing.completed:
        raise HTTPException(
            status_code=409,
            detail="Activity is already completed"
        )
    
    # Complete the activity
    completed = await repo.complete_activity(
        activity_id,
        tenant_id,
        completion_data.outcome,
        completion_data.notes
    )
    
    if not completed:
        raise HTTPException(
            status_code=500,
            detail="Failed to complete activity"
        )
        
    return completed


@router.get("/overdue/list")
async def get_overdue_activities(
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
    owner_id: Annotated[uuid.UUID | None, Query()] = None
) -> list[Activity]:
    """Get overdue activities."""
    repo = ActivityRepository(db)
    activities = await repo.get_overdue_activities(tenant_id, owner_id)
    return list(activities)


@router.get("/summary/stats", response_model=ActivitySummary)
async def get_activity_summary(
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
    owner_id: Annotated[uuid.UUID | None, Query()] = None
) -> ActivitySummary:
    """Get activity summary statistics."""
    repo = ActivityRepository(db)
    summary_data = await repo.get_activities_summary(tenant_id, owner_id)
    
    return ActivitySummary(
        total_activities=summary_data["total_activities"],
        completed_activities=summary_data["completed_activities"],
        overdue_activities=summary_data["overdue_activities"],
        today_activities=summary_data["today_activities"],
        this_week_activities=summary_data["this_week_activities"]
    )