"""Company API endpoints."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.company import Company as CompanyModel
from app.repositories.company import CompanyRepository
from app.schemas.company import (
    Company, CompanyCreate, CompanyList, CompanyUpdate
)

router = APIRouter()


@router.post("/", response_model=Company)
async def create_company(
    company: CompanyCreate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> CompanyModel:
    """Create a new company."""
    # Check if company with same name already exists
    repo = CompanyRepository(db)
    existing = await repo.get_by_name(company.name, tenant_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Company with this name already exists"
        )
    
    # Create company model
    company_data = company.model_dump()
    db_company = CompanyModel(tenant_id=tenant_id, **company_data)
    
    # Save to database
    return await repo.create(db_company)


@router.get("/", response_model=CompanyList)
async def list_companies(
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query()] = None,
    industry: Annotated[str | None, Query()] = None,
    status: Annotated[str | None, Query()] = None
) -> CompanyList:
    """List companies with pagination and search."""
    repo = CompanyRepository(db)
    
    # Get companies and total count
    companies = await repo.list(
        tenant_id, skip, limit, search, industry, status
    )
    total = await repo.count(tenant_id, search, industry, status)
    
    return CompanyList(
        items=companies,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{company_id}", response_model=Company)
async def get_company(
    company_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> CompanyModel:
    """Get a specific company by ID."""
    repo = CompanyRepository(db)
    company = await repo.get_by_id(company_id, tenant_id)
    
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )
        
    return company


@router.patch("/{company_id}", response_model=Company)
async def update_company(
    company_id: Annotated[uuid.UUID, Path()],
    company: CompanyUpdate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> CompanyModel:
    """Update a company."""
    repo = CompanyRepository(db)
    
    # Check if company exists
    existing = await repo.get_by_id(company_id, tenant_id)
    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )
    
    # Check if updating name would conflict
    if company.name and company.name != existing.name:
        name_conflict = await repo.get_by_name(company.name, tenant_id)
        if name_conflict and name_conflict.id != company_id:
            raise HTTPException(
                status_code=409,
                detail="Company with this name already exists"
            )
    
    # Update company
    updated = await repo.update(
        company_id,
        tenant_id,
        **company.model_dump(exclude_unset=True)
    )
    
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )
        
    return updated


@router.delete("/{company_id}", status_code=204)
async def delete_company(
    company_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    """Delete a company."""
    repo = CompanyRepository(db)
    
    # Try to delete the company
    deleted = await repo.soft_delete(company_id, tenant_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )


@router.get("/meta/industries")
async def get_industries(
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> list[str]:
    """Get list of unique industries."""
    repo = CompanyRepository(db)
    industries = await repo.get_industries(tenant_id)
    return list(industries)