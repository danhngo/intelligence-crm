"""Analytics API routes."""

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import AsyncRedisCache, get_cache
from app.core.database import get_db
from app.models.analytics import EventType
from app.schemas.analytics import (
    BulkEventCreate,
    ChannelAnalyticsResponse,
    ConversationAnalyticsResponse,
    DashboardMetricsResponse,
    EventCreate,
    EventResponse,
    MessageAnalyticsCreate,
    MessageAnalyticsResponse,
    TimeRangeQuery,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.post("/events", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    tenant_id: str = Query(..., description="Tenant ID"),
    db: AsyncSession = Depends(get_db),
    cache: AsyncRedisCache = Depends(get_cache)
):
    """Create a new analytics event."""
    analytics_service = AnalyticsService(db, cache)
    
    result = await analytics_service.track_event(
        event_type=event.event_type,
        event_data=event.event_data,
        tenant_id=tenant_id,
        user_id=event.user_id,
        session_id=event.session_id,
        source_service=event.source_service
    )
    
    return EventResponse.from_orm(result)


@router.post("/events/bulk", response_model=List[EventResponse])
async def create_bulk_events(
    bulk_events: BulkEventCreate,
    tenant_id: str = Query(..., description="Tenant ID"),
    db: AsyncSession = Depends(get_db),
    cache: AsyncRedisCache = Depends(get_cache)
):
    """Create multiple analytics events."""
    analytics_service = AnalyticsService(db, cache)
    
    results = []
    for event in bulk_events.events:
        result = await analytics_service.track_event(
            event_type=event.event_type,
            event_data=event.event_data,
            tenant_id=tenant_id,
            user_id=event.user_id,
            session_id=event.session_id,
            source_service=event.source_service
        )
        results.append(EventResponse.from_orm(result))
    
    return results


@router.post("/messages/analytics", response_model=MessageAnalyticsResponse)
async def process_message_analytics(
    message_data: MessageAnalyticsCreate,
    tenant_id: str = Query(..., description="Tenant ID"),
    db: AsyncSession = Depends(get_db),
    cache: AsyncRedisCache = Depends(get_cache)
):
    """Process analytics for a message."""
    analytics_service = AnalyticsService(db, cache)
    
    result = await analytics_service.process_message_analytics(
        message_data.dict(),
        tenant_id
    )
    
    return MessageAnalyticsResponse.from_orm(result)


@router.get("/conversations/{conversation_id}/analytics", response_model=ConversationAnalyticsResponse)
async def get_conversation_analytics(
    conversation_id: str,
    tenant_id: str = Query(..., description="Tenant ID"),
    start_time: Optional[datetime] = Query(None, description="Start time"),
    end_time: Optional[datetime] = Query(None, description="End time"),
    db: AsyncSession = Depends(get_db),
    cache: AsyncRedisCache = Depends(get_cache)
):
    """Get analytics for a specific conversation."""
    analytics_service = AnalyticsService(db, cache)
    
    # Set default time range if not provided
    if not end_time:
        end_time = datetime.utcnow()
    if not start_time:
        start_time = end_time - timedelta(days=7)
    
    result = await analytics_service.get_conversation_analytics(
        conversation_id=conversation_id,
        tenant_id=tenant_id,
        start_time=start_time,
        end_time=end_time
    )
    
    return ConversationAnalyticsResponse(**result)


@router.get("/channels/{channel_id}/analytics", response_model=ChannelAnalyticsResponse)
async def get_channel_analytics(
    channel_id: str,
    tenant_id: str = Query(..., description="Tenant ID"),
    start_time: datetime = Query(..., description="Start time"),
    end_time: datetime = Query(..., description="End time"),
    db: AsyncSession = Depends(get_db),
    cache: AsyncRedisCache = Depends(get_cache)
):
    """Get analytics for a specific channel."""
    analytics_service = AnalyticsService(db, cache)
    
    result = await analytics_service.get_channel_analytics(
        channel_id=channel_id,
        tenant_id=tenant_id,
        start_time=start_time,
        end_time=end_time
    )
    
    return ChannelAnalyticsResponse(**result)


@router.get("/dashboard", response_model=DashboardMetricsResponse)
async def get_dashboard_metrics(
    tenant_id: str = Query(..., description="Tenant ID"),
    period: str = Query("day", regex="^(hour|day|week|month)$", description="Time period"),
    db: AsyncSession = Depends(get_db),
    cache: AsyncRedisCache = Depends(get_cache)
):
    """Get dashboard metrics for a tenant."""
    analytics_service = AnalyticsService(db, cache)
    
    result = await analytics_service.get_dashboard_metrics(
        tenant_id=tenant_id,
        period=period
    )
    
    return DashboardMetricsResponse(**result)


@router.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db),
    cache: AsyncRedisCache = Depends(get_cache)
):
    """Health check endpoint."""
    
    # Check database connection
    try:
        await db.execute("SELECT 1")
        db_connected = True
    except Exception:
        db_connected = False
    
    # Check cache connection
    try:
        await cache.set("health_check", "ok", ttl=10)
        cache_connected = True
    except Exception:
        cache_connected = False
    
    status = "healthy" if db_connected and cache_connected else "unhealthy"
    
    return {
        "status": status,
        "timestamp": datetime.utcnow(),
        "database_connected": db_connected,
        "cache_connected": cache_connected,
        "processing_queue_size": 0  # Placeholder for queue monitoring
    }
