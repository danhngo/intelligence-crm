"""Lead API endpoints."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.lead import Lead as LeadModel
from app.repositories.lead import LeadRepository
from app.schemas.lead import (
    Lead, LeadCreate, LeadList, LeadUpdate, LeadConvert
)
from app.schemas.contact import Contact

router = APIRouter()


@router.post("/", response_model=Lead)
async def create_lead(
    lead: LeadCreate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LeadModel:
    """Create a new lead."""
    # Check if lead with same email already exists (if email provided)
    repo = LeadRepository(db)
    if lead.email:
        existing = await repo.get_by_email(lead.email, tenant_id)
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Lead with this email already exists"
            )
    
    # Create lead model
    lead_data = lead.model_dump()
    db_lead = LeadModel(tenant_id=tenant_id, **lead_data)
    
    # Save to database
    return await repo.create(db_lead)


@router.get("/", response_model=LeadList)
async def list_leads(
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query()] = None,
    status: Annotated[str | None, Query()] = None,
    source: Annotated[str | None, Query()] = None,
    owner_id: Annotated[uuid.UUID | None, Query()] = None
) -> LeadList:
    """List leads with pagination and search."""
    repo = LeadRepository(db)
    
    # Get leads and total count
    leads = await repo.list(
        tenant_id, skip, limit, search, status, source, owner_id
    )
    total = await repo.count(tenant_id, search, status, source, owner_id)
    
    return LeadList(
        items=leads,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{lead_id}", response_model=Lead)
async def get_lead(
    lead_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LeadModel:
    """Get a specific lead by ID."""
    repo = LeadRepository(db)
    lead = await repo.get_by_id(lead_id, tenant_id)
    
    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )
        
    return lead


@router.patch("/{lead_id}", response_model=Lead)
async def update_lead(
    lead_id: Annotated[uuid.UUID, Path()],
    lead: LeadUpdate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LeadModel:
    """Update a lead."""
    repo = LeadRepository(db)
    
    # Check if lead exists
    existing = await repo.get_by_id(lead_id, tenant_id)
    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )
    
    # Check if updating email would conflict
    if lead.email and lead.email != existing.email:
        email_conflict = await repo.get_by_email(lead.email, tenant_id)
        if email_conflict and email_conflict.id != lead_id:
            raise HTTPException(
                status_code=409,
                detail="Lead with this email already exists"
            )
    
    # Update lead
    updated = await repo.update(
        lead_id,
        tenant_id,
        **lead.model_dump(exclude_unset=True)
    )
    
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )
        
    return updated


@router.delete("/{lead_id}", status_code=204)
async def delete_lead(
    lead_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    """Delete a lead."""
    repo = LeadRepository(db)
    
    # Try to delete the lead
    deleted = await repo.soft_delete(lead_id, tenant_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )


@router.post("/{lead_id}/convert", response_model=Contact)
async def convert_lead(
    lead_id: Annotated[uuid.UUID, Path()],
    convert_data: LeadConvert,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> Contact:
    """Convert a lead to a contact."""
    repo = LeadRepository(db)
    
    # Check if lead exists and hasn't been converted yet
    lead = await repo.get_by_id(lead_id, tenant_id)
    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )
    
    if lead.converted_contact_id:
        raise HTTPException(
            status_code=409,
            detail="Lead has already been converted"
        )
    
    # Convert lead to contact
    contact = await repo.convert_to_contact(lead_id, tenant_id)
    if not contact:
        raise HTTPException(
            status_code=500,
            detail="Failed to convert lead"
        )
    
    # TODO: Implement company and deal creation if requested
    # This would involve creating CompanyRepository and DealRepository instances
    # and creating the respective records
    
    return contact


@router.get("/meta/sources")
async def get_lead_sources(
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> list[str]:
    """Get list of unique lead sources."""
    repo = LeadRepository(db)
    sources = await repo.get_lead_sources(tenant_id)
    return list(sources)