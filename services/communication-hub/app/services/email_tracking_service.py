"""Email tracking service for real-time event handling."""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import EmailTrackingEvent, EmailEventType, CampaignMessage
from app.schemas.campaign import (
    EmailTrackingEventCreate,
    EmailTrackingEventList
)

logger = logging.getLogger(__name__)


class EmailTrackingService:
    """Service for handling email tracking events."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def track_event(self, event: EmailTrackingEventCreate) -> EmailTrackingEvent:
        """Track an email event."""
        # Resolve campaign and message info from tracking_id
        campaign_message = await self._get_campaign_message_by_tracking_id(event.tracking_id)
        
        # Create tracking event
        db_event = EmailTrackingEvent(
            **event.model_dump(),
            campaign_id=campaign_message.campaign_id if campaign_message else None,
            campaign_message_id=campaign_message.id if campaign_message else None,
            recipient_email=campaign_message.recipient_email if campaign_message else event.recipient_email,
            event_timestamp=datetime.utcnow()
        )
        
        # Enrich with geo/device data
        if event.ip_address:
            geo_data = await self._get_geo_data(event.ip_address)
            db_event.country = geo_data.get("country")
            db_event.region = geo_data.get("region") 
            db_event.city = geo_data.get("city")
        
        if event.user_agent:
            device_data = self._parse_user_agent(event.user_agent)
            db_event.device_type = device_data.get("device_type")
            db_event.client_name = device_data.get("client_name")
            db_event.client_version = device_data.get("client_version")
        
        self.db.add(db_event)
        await self.db.commit()
        await self.db.refresh(db_event)
        
        # Update campaign statistics
        if campaign_message:
            await self._update_campaign_stats(campaign_message.campaign_id, event.event_type)
        
        logger.info(f"Tracked {event.event_type} event for {event.recipient_email}")
        return db_event

    async def track_click(
        self,
        link_id: str,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Track link click and return redirect URL."""
        # Get link info from link_id (implement link mapping)
        link_info = await self._get_link_info(link_id)
        if not link_info:
            return None
        
        # Create click event
        event = EmailTrackingEventCreate(
            event_type=EmailEventType.CLICKED,
            tracking_id=link_info["tracking_id"],
            recipient_email=link_info["recipient_email"],
            url=link_info["original_url"],
            link_id=link_id,
            user_agent=user_agent,
            ip_address=ip_address
        )
        
        await self.track_event(event)
        
        return {
            "redirect_url": link_info["original_url"],
            "tracking_id": link_info["tracking_id"]
        }

    async def get_campaign_events(
        self,
        campaign_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 20,
        event_type: Optional[EmailEventType] = None
    ) -> EmailTrackingEventList:
        """Get tracking events for a campaign."""
        query = select(EmailTrackingEvent).where(
            EmailTrackingEvent.campaign_id == campaign_id
        )
        
        if event_type:
            query = query.where(EmailTrackingEvent.event_type == event_type)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(EmailTrackingEvent.event_timestamp.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        events = result.scalars().all()
        
        return EmailTrackingEventList(
            items=events,
            total=total,
            skip=skip,
            limit=limit
        )

    async def get_recipient_events(
        self,
        recipient_email: str,
        tenant_id: UUID,
        days_back: int = 30
    ) -> List[EmailTrackingEvent]:
        """Get all events for a specific recipient."""
        since = datetime.utcnow() - timedelta(days=days_back)
        
        query = select(EmailTrackingEvent).where(
            EmailTrackingEvent.recipient_email == recipient_email,
            EmailTrackingEvent.event_timestamp >= since
        ).order_by(EmailTrackingEvent.event_timestamp.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_event_analytics(
        self,
        campaign_id: Optional[UUID] = None,
        tenant_id: Optional[UUID] = None,
        days_back: int = 7
    ) -> Dict[str, Any]:
        """Get analytics data for events."""
        since = datetime.utcnow() - timedelta(days=days_back)
        
        query = select(EmailTrackingEvent).where(
            EmailTrackingEvent.event_timestamp >= since
        )
        
        if campaign_id:
            query = query.where(EmailTrackingEvent.campaign_id == campaign_id)
        
        result = await self.db.execute(query)
        events = result.scalars().all()
        
        # Aggregate statistics
        stats = {
            "total_events": len(events),
            "by_type": {},
            "by_day": {},
            "by_device": {},
            "by_country": {},
            "unique_recipients": set()
        }
        
        for event in events:
            # By type
            event_type = event.event_type.value
            stats["by_type"][event_type] = stats["by_type"].get(event_type, 0) + 1
            
            # By day
            day = event.event_timestamp.date().isoformat()
            stats["by_day"][day] = stats["by_day"].get(day, 0) + 1
            
            # By device
            if event.device_type:
                stats["by_device"][event.device_type] = stats["by_device"].get(event.device_type, 0) + 1
            
            # By country
            if event.country:
                stats["by_country"][event.country] = stats["by_country"].get(event.country, 0) + 1
            
            # Unique recipients
            stats["unique_recipients"].add(event.recipient_email)
        
        stats["unique_recipients"] = len(stats["unique_recipients"])
        return stats

    async def _get_campaign_message_by_tracking_id(self, tracking_id: str) -> Optional[CampaignMessage]:
        """Get campaign message by tracking ID."""
        query = select(CampaignMessage).where(
            CampaignMessage.tracking_id == tracking_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _get_link_info(self, link_id: str) -> Optional[Dict[str, Any]]:
        """Get link information for click tracking."""
        # TODO: Implement link mapping storage
        # This would store mappings of link_id -> {original_url, tracking_id, etc.}
        # For now, return None
        return None

    async def _update_campaign_stats(self, campaign_id: UUID, event_type: EmailEventType):
        """Update campaign statistics based on event type."""
        from app.models.campaign import Campaign
        
        # Get campaign
        query = select(Campaign).where(Campaign.id == campaign_id)
        result = await self.db.execute(query)
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            return
        
        # Update appropriate counter
        if event_type == EmailEventType.DELIVERED:
            campaign.delivered_count += 1
        elif event_type == EmailEventType.OPENED:
            campaign.opened_count += 1
        elif event_type == EmailEventType.CLICKED:
            campaign.clicked_count += 1
        elif event_type == EmailEventType.BOUNCED:
            campaign.bounced_count += 1
        elif event_type == EmailEventType.COMPLAINED:
            campaign.complained_count += 1
        elif event_type == EmailEventType.UNSUBSCRIBED:
            campaign.unsubscribed_count += 1
        
        await self.db.commit()

    async def _get_geo_data(self, ip_address: str) -> Dict[str, Any]:
        """Get geographical data from IP address."""
        # TODO: Integrate with IP geolocation service (MaxMind, IPStack, etc.)
        # For now, return empty dict
        return {}

    def _parse_user_agent(self, user_agent: str) -> Dict[str, Any]:
        """Parse user agent string for device/client info."""
        # TODO: Implement user agent parsing (use user-agents library)
        # For now, return basic classification
        user_agent_lower = user_agent.lower()
        
        result = {}
        
        # Device type detection
        if any(mobile in user_agent_lower for mobile in ['mobile', 'android', 'iphone']):
            result["device_type"] = "mobile"
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            result["device_type"] = "tablet"
        else:
            result["device_type"] = "desktop"
        
        # Email client detection
        if 'outlook' in user_agent_lower:
            result["client_name"] = "Outlook"
        elif 'gmail' in user_agent_lower:
            result["client_name"] = "Gmail"
        elif 'apple mail' in user_agent_lower:
            result["client_name"] = "Apple Mail"
        elif 'thunderbird' in user_agent_lower:
            result["client_name"] = "Thunderbird"
        else:
            result["client_name"] = "Unknown"
        
        return result
