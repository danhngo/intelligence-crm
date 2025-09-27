"""Campaign management API endpoints."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, get_tenant_id
from app.core.database import get_db
from app.models.campaign import (
    Campaign,
    CampaignMessage, 
    CampaignStatus,
    EmailTrackingEvent,
    EmailEventType
)
from app.schemas.campaign import (
    BulkActionResult,
    BulkCampaignAction,
    Campaign as CampaignSchema,
    CampaignCreate,
    CampaignList,
    CampaignStats,
    CampaignUpdate,
    EmailTrackingEventCreate,
    EmailTrackingEventList,
    TrackingPixelResponse,
    LinkClickRedirect
)
from app.services.campaign_service import CampaignService
from app.services.email_tracking_service import EmailTrackingService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=CampaignSchema)
async def create_campaign(
    campaign: CampaignCreate,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new campaign."""
    try:
        service = CampaignService(db)
        return await service.create_campaign(
            campaign=campaign,
            tenant_id=tenant_id,
            created_by=current_user["id"]
        )
    except Exception as e:
        logger.error(f"Error creating campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=CampaignList)
async def list_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[CampaignStatus] = None,
    campaign_type: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """List campaigns with filtering and pagination."""
    try:
        service = CampaignService(db)
        return await service.list_campaigns(
            tenant_id=tenant_id,
            skip=skip,
            limit=limit,
            status=status,
            campaign_type=campaign_type,
            search=search
        )
    except Exception as e:
        logger.error(f"Error listing campaigns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{campaign_id}", response_model=CampaignSchema)
async def get_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Get a specific campaign."""
    try:
        service = CampaignService(db)
        campaign = await service.get_campaign(campaign_id, tenant_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting campaign {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{campaign_id}", response_model=CampaignSchema)
async def update_campaign(
    campaign_id: UUID,
    campaign_update: CampaignUpdate,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Update a campaign."""
    try:
        service = CampaignService(db)
        campaign = await service.update_campaign(
            campaign_id=campaign_id,
            campaign_update=campaign_update,
            tenant_id=tenant_id
        )
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating campaign {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Delete a campaign."""
    try:
        service = CampaignService(db)
        success = await service.delete_campaign(campaign_id, tenant_id)
        if not success:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return {"message": "Campaign deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting campaign {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{campaign_id}/start", response_model=CampaignSchema)
async def start_campaign(
    campaign_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Start a campaign."""
    try:
        service = CampaignService(db)
        campaign = await service.start_campaign(
            campaign_id=campaign_id,
            tenant_id=tenant_id,
            background_tasks=background_tasks
        )
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting campaign {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{campaign_id}/pause", response_model=CampaignSchema)
async def pause_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Pause a campaign."""
    try:
        service = CampaignService(db)
        campaign = await service.pause_campaign(campaign_id, tenant_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error pausing campaign {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{campaign_id}/stop", response_model=CampaignSchema)
async def stop_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Stop a campaign."""
    try:
        service = CampaignService(db)
        campaign = await service.stop_campaign(campaign_id, tenant_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error stopping campaign {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{campaign_id}/stats", response_model=CampaignStats)
async def get_campaign_stats(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Get campaign statistics."""
    try:
        service = CampaignService(db)
        stats = await service.get_campaign_stats(campaign_id, tenant_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting campaign stats {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{campaign_id}/events", response_model=EmailTrackingEventList)
async def get_campaign_events(
    campaign_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    event_type: Optional[EmailEventType] = None,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Get campaign tracking events."""
    try:
        tracking_service = EmailTrackingService(db)
        return await tracking_service.get_campaign_events(
            campaign_id=campaign_id,
            tenant_id=tenant_id,
            skip=skip,
            limit=limit,
            event_type=event_type
        )
    except Exception as e:
        logger.error(f"Error getting campaign events {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk-action", response_model=BulkActionResult)
async def bulk_campaign_action(
    action: BulkCampaignAction,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    tenant_id: UUID = Depends(get_tenant_id)
):
    """Perform bulk action on campaigns."""
    try:
        service = CampaignService(db)
        return await service.bulk_action(
            action=action,
            tenant_id=tenant_id,
            background_tasks=background_tasks
        )
    except Exception as e:
        logger.error(f"Error performing bulk action: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Email Tracking Endpoints
@router.get("/tracking/open/{tracking_id}", response_model=TrackingPixelResponse)
async def track_email_open(
    tracking_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Track email open event via tracking pixel."""
    try:
        tracking_service = EmailTrackingService(db)
        
        # Extract client information
        user_agent = request.headers.get("user-agent")
        forwarded_for = request.headers.get("x-forwarded-for")
        real_ip = request.headers.get("x-real-ip")
        client_ip = forwarded_for or real_ip or request.client.host
        
        event = EmailTrackingEventCreate(
            event_type=EmailEventType.OPENED,
            tracking_id=tracking_id,
            recipient_email="",  # Will be resolved from tracking_id
            user_agent=user_agent,
            ip_address=client_ip
        )
        
        result = await tracking_service.track_event(event)
        
        # Return 1x1 transparent pixel
        pixel_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x04\x01\x00\x3B'
        
        return Response(
            content=pixel_data,
            media_type="image/gif",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    except Exception as e:
        logger.error(f"Error tracking email open {tracking_id}: {e}")
        # Still return pixel to avoid broken images
        pixel_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x04\x01\x00\x3B'
        return Response(content=pixel_data, media_type="image/gif")


@router.get("/tracking/click/{link_id}")
async def track_link_click(
    link_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Track link click and redirect to original URL."""
    try:
        tracking_service = EmailTrackingService(db)
        
        # Extract client information
        user_agent = request.headers.get("user-agent")
        forwarded_for = request.headers.get("x-forwarded-for")
        real_ip = request.headers.get("x-real-ip")
        client_ip = forwarded_for or real_ip or request.client.host
        
        # Get original URL and track click
        result = await tracking_service.track_click(
            link_id=link_id,
            user_agent=user_agent,
            ip_address=client_ip
        )
        
        if result and result.get("redirect_url"):
            return Response(
                status_code=302,
                headers={"Location": result["redirect_url"]}
            )
        else:
            raise HTTPException(status_code=404, detail="Link not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tracking link click {link_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tracking/events", response_model=Dict[str, Any])
async def create_tracking_event(
    event: EmailTrackingEventCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a tracking event manually (for webhooks, etc.)."""
    try:
        tracking_service = EmailTrackingService(db)
        result = await tracking_service.track_event(event)
        return {"success": True, "event_id": result.id}
    except Exception as e:
        logger.error(f"Error creating tracking event: {e}")
        raise HTTPException(status_code=500, detail=str(e))
