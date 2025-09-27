"""Deal API endpoints."""

import uuid
from typing import Annotated, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.deal import Deal as DealModel
from app.repositories.deal import DealRepository
from app.schemas.deal import (
    Deal, DealCreate, DealList, DealUpdate, DealStageUpdate, DealPipeline
)

router = APIRouter()


@router.post("/", response_model=Deal)
async def create_deal(
    deal: DealCreate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> DealModel:
    """Create a new deal."""
    # Create deal model
    deal_data = deal.model_dump()
    db_deal = DealModel(tenant_id=tenant_id, **deal_data)
    
    # Save to database
    repo = DealRepository(db)
    return await repo.create(db_deal)


@router.get("/", response_model=DealList)
async def list_deals(
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query()] = None,
    stage: Annotated[str | None, Query()] = None,
    owner_id: Annotated[uuid.UUID | None, Query()] = None,
    contact_id: Annotated[uuid.UUID | None, Query()] = None,
    company_id: Annotated[uuid.UUID | None, Query()] = None
) -> DealList:
    """List deals with pagination and search."""
    repo = DealRepository(db)
    
    # Get deals and total count
    deals = await repo.list(
        tenant_id, skip, limit, search, stage, owner_id, contact_id, company_id
    )
    total = await repo.count(
        tenant_id, search, stage, owner_id, contact_id, company_id
    )
    
    return DealList(
        items=deals,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{deal_id}", response_model=Deal)
async def get_deal(
    deal_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> DealModel:
    """Get a specific deal by ID."""
    repo = DealRepository(db)
    deal = await repo.get_by_id(deal_id, tenant_id)
    
    if not deal:
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )
        
    return deal


@router.patch("/{deal_id}", response_model=Deal)
async def update_deal(
    deal_id: Annotated[uuid.UUID, Path()],
    deal: DealUpdate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> DealModel:
    """Update a deal."""
    repo = DealRepository(db)
    
    # Check if deal exists
    existing = await repo.get_by_id(deal_id, tenant_id)
    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )
    
    # Update deal
    updated = await repo.update(
        deal_id,
        tenant_id,
        **deal.model_dump(exclude_unset=True)
    )
    
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )
        
    return updated


@router.delete("/{deal_id}", status_code=204)
async def delete_deal(
    deal_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    """Delete a deal."""
    repo = DealRepository(db)
    
    # Try to delete the deal
    deleted = await repo.soft_delete(deal_id, tenant_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )


@router.patch("/{deal_id}/stage", response_model=Deal)
async def update_deal_stage(
    deal_id: Annotated[uuid.UUID, Path()],
    stage_update: DealStageUpdate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> DealModel:
    """Update deal stage and probability."""
    repo = DealRepository(db)
    
    # Check if deal exists
    existing = await repo.get_by_id(deal_id, tenant_id)
    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )
    
    # Update stage
    updated = await repo.update_stage(
        deal_id,
        tenant_id,
        stage_update.stage,
        stage_update.probability
    )
    
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )
        
    return updated


@router.get("/pipeline/summary")
async def get_pipeline_summary(
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
    owner_id: Annotated[uuid.UUID | None, Query()] = None
) -> list[DealPipeline]:
    """Get deal pipeline summary by stage."""
    repo = DealRepository(db)
    pipeline_data = await repo.get_pipeline_summary(tenant_id, owner_id)
    
    return [
        DealPipeline(
            stage=item["stage"],
            count=item["count"],
            total_amount=item["total_amount"],
            average_amount=item["average_amount"]
        )
        for item in pipeline_data
    ]


@router.get("/closing/this-month")
async def get_deals_closing_this_month(
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
    owner_id: Annotated[uuid.UUID | None, Query()] = None
) -> list[Deal]:
    """Get deals expected to close this month."""
    repo = DealRepository(db)
    
    # Calculate this month's date range
    now = datetime.utcnow()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if now.month == 12:
        end_of_month = start_of_month.replace(year=now.year + 1, month=1)
    else:
        end_of_month = start_of_month.replace(month=now.month + 1)
    
    deals = await repo.get_deals_by_close_date(
        tenant_id, start_of_month, end_of_month, owner_id
    )
    
    return list(deals)