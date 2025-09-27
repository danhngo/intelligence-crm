"""Email template management API endpoints."""

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, get_tenant_id
from app.core.database import get_db
from app.schemas.campaign import (
    EmailTemplate as EmailTemplateSchema,
    EmailTemplateCreate,
    EmailTemplateList,
    EmailTemplateUpdate
)
from app.services.email_template_service import EmailTemplateService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=EmailTemplateSchema)
async def create_template(
    template: EmailTemplateCreate,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new email template."""
    try:
        service = EmailTemplateService(db)
        return await service.create_template(
            template=template,
            tenant_id=tenant_id,
            created_by=current_user["id"]
        )
    except Exception as e:
        logger.error(f"Error creating email template: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=EmailTemplateList)
async def list_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """List email templates with filtering and pagination."""
    try:
        service = EmailTemplateService(db)
        return await service.list_templates(
            tenant_id=tenant_id,
            skip=skip,
            limit=limit,
            category=category,
            search=search,
            is_active=is_active
        )
    except Exception as e:
        logger.error(f"Error listing email templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{template_id}", response_model=EmailTemplateSchema)
async def get_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Get a specific email template."""
    try:
        service = EmailTemplateService(db)
        template = await service.get_template(template_id, tenant_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        return template
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting email template {template_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{template_id}", response_model=EmailTemplateSchema)
async def update_template(
    template_id: UUID,
    template_update: EmailTemplateUpdate,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Update an email template."""
    try:
        service = EmailTemplateService(db)
        template = await service.update_template(
            template_id=template_id,
            template_update=template_update,
            tenant_id=tenant_id
        )
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        return template
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating email template {template_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{template_id}")
async def delete_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Delete an email template."""
    try:
        service = EmailTemplateService(db)
        success = await service.delete_template(template_id, tenant_id)
        if not success:
            raise HTTPException(status_code=404, detail="Template not found")
        return {"message": "Template deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting email template {template_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{template_id}/preview")
async def preview_template(
    template_id: UUID,
    data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Preview template with provided data."""
    try:
        service = EmailTemplateService(db)
        preview = await service.preview_template(
            template_id=template_id,
            tenant_id=tenant_id,
            data=data
        )
        if not preview:
            raise HTTPException(status_code=404, detail="Template not found")
        return preview
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error previewing template {template_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{template_id}/duplicate", response_model=EmailTemplateSchema)
async def duplicate_template(
    template_id: UUID,
    name: str = Query(..., description="Name for the duplicated template"),
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Duplicate an existing template."""
    try:
        service = EmailTemplateService(db)
        template = await service.duplicate_template(
            template_id=template_id,
            new_name=name,
            tenant_id=tenant_id,
            created_by=current_user["id"]
        )
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        return template
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error duplicating template {template_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
