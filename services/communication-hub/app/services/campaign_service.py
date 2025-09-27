"""Campaign service for business logic."""

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign, CampaignMessage, CampaignStatus, EmailTrackingEvent
from app.schemas.campaign import (
    BulkActionResult,
    BulkCampaignAction,
    CampaignCreate,
    CampaignList,
    CampaignStats,
    CampaignUpdate
)
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class CampaignService:
    """Service class for campaign management."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.email_service = EmailService()

    async def create_campaign(
        self,
        campaign: CampaignCreate,
        tenant_id: UUID,
        created_by: UUID
    ) -> Campaign:
        """Create a new campaign."""
        db_campaign = Campaign(
            **campaign.model_dump(),
            tenant_id=tenant_id,
            created_by=created_by,
            status=CampaignStatus.DRAFT
        )
        
        self.db.add(db_campaign)
        await self.db.commit()
        await self.db.refresh(db_campaign)
        
        logger.info(f"Created campaign {db_campaign.id} for tenant {tenant_id}")
        return db_campaign

    async def list_campaigns(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 20,
        status: Optional[CampaignStatus] = None,
        campaign_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> CampaignList:
        """List campaigns with filtering."""
        query = select(Campaign).where(Campaign.tenant_id == tenant_id)
        
        # Apply filters
        if status:
            query = query.where(Campaign.status == status)
        if campaign_type:
            query = query.where(Campaign.type == campaign_type)
        if search:
            query = query.where(
                Campaign.name.ilike(f"%{search}%") |
                Campaign.description.ilike(f"%{search}%")
            )
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(Campaign.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        campaigns = result.scalars().all()
        
        return CampaignList(
            items=campaigns,
            total=total,
            skip=skip,
            limit=limit
        )

    async def get_campaign(self, campaign_id: UUID, tenant_id: UUID) -> Optional[Campaign]:
        """Get a specific campaign."""
        query = select(Campaign).where(
            Campaign.id == campaign_id,
            Campaign.tenant_id == tenant_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_campaign(
        self,
        campaign_id: UUID,
        campaign_update: CampaignUpdate,
        tenant_id: UUID
    ) -> Optional[Campaign]:
        """Update a campaign."""
        # Get existing campaign
        campaign = await self.get_campaign(campaign_id, tenant_id)
        if not campaign:
            return None
        
        # Update fields
        update_data = campaign_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(campaign, field, value)
        
        await self.db.commit()
        await self.db.refresh(campaign)
        
        logger.info(f"Updated campaign {campaign_id}")
        return campaign

    async def delete_campaign(self, campaign_id: UUID, tenant_id: UUID) -> bool:
        """Delete a campaign."""
        campaign = await self.get_campaign(campaign_id, tenant_id)
        if not campaign:
            return False
        
        await self.db.delete(campaign)
        await self.db.commit()
        
        logger.info(f"Deleted campaign {campaign_id}")
        return True

    async def start_campaign(
        self,
        campaign_id: UUID,
        tenant_id: UUID,
        background_tasks: BackgroundTasks
    ) -> Optional[Campaign]:
        """Start a campaign."""
        campaign = await self.get_campaign(campaign_id, tenant_id)
        if not campaign:
            return None
        
        if campaign.status not in [CampaignStatus.DRAFT, CampaignStatus.PAUSED]:
            raise ValueError(f"Cannot start campaign in {campaign.status} status")
        
        # Update status
        campaign.status = CampaignStatus.RUNNING
        campaign.started_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(campaign)
        
        # Queue campaign execution
        background_tasks.add_task(self._execute_campaign, campaign_id)
        
        logger.info(f"Started campaign {campaign_id}")
        return campaign

    async def pause_campaign(self, campaign_id: UUID, tenant_id: UUID) -> Optional[Campaign]:
        """Pause a campaign."""
        campaign = await self.get_campaign(campaign_id, tenant_id)
        if not campaign:
            return None
        
        if campaign.status != CampaignStatus.RUNNING:
            raise ValueError(f"Cannot pause campaign in {campaign.status} status")
        
        campaign.status = CampaignStatus.PAUSED
        await self.db.commit()
        await self.db.refresh(campaign)
        
        logger.info(f"Paused campaign {campaign_id}")
        return campaign

    async def stop_campaign(self, campaign_id: UUID, tenant_id: UUID) -> Optional[Campaign]:
        """Stop a campaign."""
        campaign = await self.get_campaign(campaign_id, tenant_id)
        if not campaign:
            return None
        
        campaign.status = CampaignStatus.COMPLETED
        campaign.completed_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(campaign)
        
        logger.info(f"Stopped campaign {campaign_id}")
        return campaign

    async def get_campaign_stats(self, campaign_id: UUID, tenant_id: UUID) -> Optional[CampaignStats]:
        """Get campaign statistics."""
        campaign = await self.get_campaign(campaign_id, tenant_id)
        if not campaign:
            return None
        
        # Calculate rates safely
        def safe_rate(numerator: int, denominator: int) -> float:
            return (numerator / denominator * 100) if denominator > 0 else 0.0
        
        return CampaignStats(
            total_recipients=campaign.total_recipients,
            sent_count=campaign.sent_count,
            delivered_count=campaign.delivered_count,
            opened_count=campaign.opened_count,
            clicked_count=campaign.clicked_count,
            bounced_count=campaign.bounced_count,
            complained_count=campaign.complained_count,
            unsubscribed_count=campaign.unsubscribed_count,
            delivery_rate=safe_rate(campaign.delivered_count, campaign.sent_count),
            open_rate=safe_rate(campaign.opened_count, campaign.delivered_count),
            click_rate=safe_rate(campaign.clicked_count, campaign.delivered_count),
            click_to_open_rate=safe_rate(campaign.clicked_count, campaign.opened_count),
            bounce_rate=safe_rate(campaign.bounced_count, campaign.sent_count),
            complaint_rate=safe_rate(campaign.complained_count, campaign.delivered_count),
            unsubscribe_rate=safe_rate(campaign.unsubscribed_count, campaign.delivered_count),
        )

    async def bulk_action(
        self,
        action: BulkCampaignAction,
        tenant_id: UUID,
        background_tasks: BackgroundTasks
    ) -> BulkActionResult:
        """Perform bulk action on campaigns."""
        success_count = 0
        failed_count = 0
        errors = []
        
        for campaign_id in action.campaign_ids:
            try:
                if action.action == "start":
                    await self.start_campaign(campaign_id, tenant_id, background_tasks)
                elif action.action == "pause":
                    await self.pause_campaign(campaign_id, tenant_id)
                elif action.action == "stop":
                    await self.stop_campaign(campaign_id, tenant_id)
                elif action.action == "delete":
                    await self.delete_campaign(campaign_id, tenant_id)
                
                success_count += 1
                
            except Exception as e:
                failed_count += 1
                errors.append({
                    "campaign_id": str(campaign_id),
                    "error": str(e)
                })
                logger.error(f"Bulk action {action.action} failed for campaign {campaign_id}: {e}")
        
        return BulkActionResult(
            success_count=success_count,
            failed_count=failed_count,
            errors=errors
        )

    async def _execute_campaign(self, campaign_id: UUID):
        """Execute campaign in background."""
        try:
            logger.info(f"Executing campaign {campaign_id}")
            
            # Get campaign details
            campaign = await self.get_campaign(campaign_id, None)  # Skip tenant check in background
            if not campaign:
                logger.error(f"Campaign {campaign_id} not found for execution")
                return
            
            # Get target contacts
            contacts = await self._get_campaign_contacts(campaign)
            
            # Update recipient count
            campaign.total_recipients = len(contacts)
            await self.db.commit()
            
            # Process contacts in batches
            batch_size = 100
            for i in range(0, len(contacts), batch_size):
                batch = contacts[i:i + batch_size]
                await self._process_contact_batch(campaign, batch)
                
                # Check if campaign is still running
                await self.db.refresh(campaign)
                if campaign.status != CampaignStatus.RUNNING:
                    logger.info(f"Campaign {campaign_id} stopped during execution")
                    break
                
                # Small delay between batches
                await asyncio.sleep(1)
            
            # Mark campaign as completed if it finished normally
            if campaign.status == CampaignStatus.RUNNING:
                campaign.status = CampaignStatus.COMPLETED
                campaign.completed_at = datetime.utcnow()
                await self.db.commit()
            
            logger.info(f"Campaign {campaign_id} execution completed")
            
        except Exception as e:
            logger.error(f"Error executing campaign {campaign_id}: {e}")
            # Mark campaign as failed
            try:
                campaign = await self.get_campaign(campaign_id, None)
                if campaign:
                    campaign.status = CampaignStatus.COMPLETED  # or add FAILED status
                    await self.db.commit()
            except Exception as commit_error:
                logger.error(f"Error updating campaign status: {commit_error}")

    async def _get_campaign_contacts(self, campaign: Campaign) -> List[Dict[str, Any]]:
        """Get target contacts for campaign."""
        # TODO: Implement contact fetching based on segments and lists
        # This would integrate with the CRM Core service to get contacts
        # For now, return empty list
        return []

    async def _process_contact_batch(self, campaign: Campaign, contacts: List[Dict[str, Any]]):
        """Process a batch of contacts for campaign."""
        for contact in contacts:
            try:
                # Create campaign message record
                tracking_id = str(uuid.uuid4())
                
                campaign_message = CampaignMessage(
                    campaign_id=campaign.id,
                    recipient_email=contact["email"],
                    recipient_contact_id=contact.get("id"),
                    subject_line=campaign.subject_line or "Default Subject",
                    tracking_id=tracking_id,
                    personalization_data=contact
                )
                
                self.db.add(campaign_message)
                await self.db.flush()
                
                # Send email (implement actual sending)
                await self.email_service.send_campaign_email(campaign_message)
                
                # Update campaign statistics
                campaign.sent_count += 1
                
            except Exception as e:
                logger.error(f"Error processing contact {contact.get('email')}: {e}")
                campaign_message.status = "failed"
                campaign_message.error_message = str(e)
        
        await self.db.commit()
