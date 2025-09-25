"""Contact API endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.contact import Contact as ContactModel
from app.repositories.contact import ContactRepository
from app.schemas.contact import (
    Contact, ContactCreate, ContactList, ContactUpdate
)

router = APIRouter()


@router.post("/", response_model=Contact)
async def create_contact(
    contact: ContactCreate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ContactModel:
    """Create a new contact."""
    # Create contact model
    contact_data = contact.model_dump()
    db_contact = ContactModel(tenant_id=tenant_id, **contact_data)
    
    # Save to database
    repo = ContactRepository(db)
    return await repo.create(db_contact)


@router.get("/", response_model=ContactList)
async def list_contacts(
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query()] = None
) -> ContactList:
    """List contacts with pagination and search."""
    repo = ContactRepository(db)
    
    # Get contacts and total count
    contacts = await repo.list(tenant_id, skip, limit, search)
    total = await repo.count(tenant_id, search)
    
    return ContactList(
        items=contacts,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{contact_id}", response_model=Contact)
async def get_contact(
    contact_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ContactModel:
    """Get a specific contact by ID."""
    repo = ContactRepository(db)
    contact = await repo.get_by_id(contact_id, tenant_id)
    
    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
        
    return contact


@router.patch("/{contact_id}", response_model=Contact)
async def update_contact(
    contact_id: Annotated[uuid.UUID, Path()],
    contact: ContactUpdate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ContactModel:
    """Update a contact."""
    repo = ContactRepository(db)
    
    # Check if contact exists
    existing = await repo.get_by_id(contact_id, tenant_id)
    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    
    # Update contact
    updated = await repo.update(
        contact_id,
        tenant_id,
        **contact.model_dump(exclude_unset=True)
    )
    
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
        
    return updated


@router.delete("/{contact_id}", status_code=204)
async def delete_contact(
    contact_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    """Delete a contact."""
    repo = ContactRepository(db)
    
    # Try to delete the contact
    deleted = await repo.soft_delete(contact_id, tenant_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
