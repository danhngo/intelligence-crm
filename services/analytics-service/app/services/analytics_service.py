"""Analytics service implementation."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.orm import selectinload

from app.models.analytics import (
    Event,
    MessageAnalytics,
    ConversationAnalytics,
    ChannelAnalytics,
    UserEngagementAnalytics,
    MetricSnapshot,
    EventType,
    MetricType
)
from app.core.cache import AsyncRedisCache
from app.core.config import get_settings

settings = get_settings()


class AnalyticsService:
    """Service for processing and aggregating analytics data."""
    
    def __init__(self, db: AsyncSession, cache: AsyncRedisCache):
        self.db = db
        self.cache = cache

    async def track_event(
        self,
        event_type: EventType,
        event_data: Dict[str, Any],
        tenant_id: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        source_service: str = "communication-hub"
    ) -> Event:
        """Track an analytics event."""
        
        event = Event(
            event_type=event_type,
            source_service=source_service,
            event_data=event_data,
            user_id=user_id,
            session_id=session_id or f"session_{datetime.utcnow().timestamp()}",
            tenant_id=tenant_id
        )
        
        self.db.add(event)
        await self.db.commit()
        
        # Cache event for real-time processing
        await self._cache_event(event)
        
        return event

    async def process_message_analytics(
        self,
        message_data: Dict[str, Any],
        tenant_id: str
    ) -> MessageAnalytics:
        """Process analytics for a message."""
        
        current_time = datetime.utcnow()
        period_hour = current_time.strftime("%Y-%m-%d-%H")
        period_day = current_time.strftime("%Y-%m-%d")
        
        analytics = MessageAnalytics(
            message_id=message_data["id"],
            conversation_id=message_data["conversation_id"],
            channel_id=message_data["channel_id"],
            direction=message_data.get("direction", "inbound"),
            message_length=len(message_data.get("content", {}).get("text", "")),
            sentiment_score=message_data.get("sentiment", {}).get("score"),
            sentiment_label=message_data.get("sentiment", {}).get("label"),
            sentiment_confidence=message_data.get("sentiment", {}).get("confidence"),
            intent_name=message_data.get("intent", {}).get("name"),
            intent_confidence=message_data.get("intent", {}).get("confidence"),
            response_time=message_data.get("response_time"),
            tenant_id=tenant_id,
            period_hour=period_hour,
            period_day=period_day
        )
        
        self.db.add(analytics)
        await self.db.commit()
        
        # Update real-time metrics in cache
        await self._update_real_time_metrics(analytics, tenant_id)
        
        return analytics

    async def get_conversation_analytics(
        self,
        conversation_id: str,
        tenant_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get analytics for a conversation."""
        
        # Set default time range if not provided
        if not end_time:
            end_time = datetime.utcnow()
        if not start_time:
            start_time = end_time - timedelta(days=7)
        
        # Query message analytics
        query = select(MessageAnalytics).where(
            and_(
                MessageAnalytics.conversation_id == conversation_id,
                MessageAnalytics.tenant_id == tenant_id,
                MessageAnalytics.created_at.between(start_time, end_time)
            )
        )
        
        result = await self.db.execute(query)
        messages = result.scalars().all()
        
        # Calculate aggregated metrics
        total_messages = len(messages)
        inbound_messages = len([m for m in messages if m.direction == "inbound"])
        outbound_messages = len([m for m in messages if m.direction == "outbound"])
        
        sentiment_scores = [m.sentiment_score for m in messages if m.sentiment_score is not None]
        response_times = [m.response_time for m in messages if m.response_time is not None]
        
        # Calculate sentiment distribution
        sentiment_distribution = {}
        for message in messages:
            if message.sentiment_label:
                sentiment_distribution[message.sentiment_label] = sentiment_distribution.get(message.sentiment_label, 0) + 1
        
        # Calculate intent distribution
        intent_distribution = {}
        for message in messages:
            if message.intent_name:
                intent_distribution[message.intent_name] = intent_distribution.get(message.intent_name, 0) + 1
        
        return {
            "conversation_id": conversation_id,
            "period": {
                "start": start_time,
                "end": end_time
            },
            "message_metrics": {
                "total_messages": total_messages,
                "inbound_messages": inbound_messages,
                "outbound_messages": outbound_messages,
                "avg_message_length": sum(m.message_length for m in messages) / total_messages if total_messages > 0 else 0
            },
            "sentiment_metrics": {
                "avg_sentiment": sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0,
                "sentiment_distribution": sentiment_distribution
            },
            "intent_metrics": {
                "intent_distribution": intent_distribution,
                "intent_changes": len(set(m.intent_name for m in messages if m.intent_name))
            },
            "performance_metrics": {
                "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
                "max_response_time": max(response_times) if response_times else 0,
                "min_response_time": min(response_times) if response_times else 0
            }
        }

    async def get_channel_analytics(
        self,
        channel_id: str,
        tenant_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, Any]:
        """Get analytics for a channel."""
        
        # Query channel analytics
        query = select(ChannelAnalytics).where(
            and_(
                ChannelAnalytics.channel_id == channel_id,
                ChannelAnalytics.tenant_id == tenant_id,
                ChannelAnalytics.created_at.between(start_time, end_time)
            )
        ).order_by(desc(ChannelAnalytics.created_at))
        
        result = await self.db.execute(query)
        channel_metrics = result.scalars().all()
        
        if not channel_metrics:
            return {
                "channel_id": channel_id,
                "period": {"start": start_time, "end": end_time},
                "metrics": {}
            }
        
        # Aggregate metrics
        total_conversations = sum(m.active_conversations for m in channel_metrics)
        total_messages = sum(m.messages_processed for m in channel_metrics)
        avg_response_time = sum(m.avg_response_time for m in channel_metrics if m.avg_response_time) / len([m for m in channel_metrics if m.avg_response_time])
        
        return {
            "channel_id": channel_id,
            "period": {"start": start_time, "end": end_time},
            "metrics": {
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "avg_response_time": avg_response_time,
                "success_rate": sum(m.success_rate for m in channel_metrics) / len(channel_metrics),
                "uptime_percentage": sum(m.uptime_percentage for m in channel_metrics) / len(channel_metrics)
            },
            "time_series": [
                {
                    "timestamp": m.created_at,
                    "active_conversations": m.active_conversations,
                    "messages_processed": m.messages_processed,
                    "response_time": m.avg_response_time,
                    "success_rate": m.success_rate
                }
                for m in channel_metrics
            ]
        }

    async def get_dashboard_metrics(
        self,
        tenant_id: str,
        period: str = "day"  # 'hour', 'day', 'week', 'month'
    ) -> Dict[str, Any]:
        """Get dashboard metrics for a tenant."""
        
        # Calculate time range based on period
        end_time = datetime.utcnow()
        if period == "hour":
            start_time = end_time - timedelta(hours=24)
        elif period == "day":
            start_time = end_time - timedelta(days=7)
        elif period == "week":
            start_time = end_time - timedelta(weeks=4)
        else:  # month
            start_time = end_time - timedelta(days=90)
        
        # Get cached metrics first
        cache_key = f"dashboard:{tenant_id}:{period}"
        cached_metrics = await self.cache.get(cache_key)
        
        if cached_metrics:
            return json.loads(cached_metrics)
        
        # Calculate metrics from database
        metrics = await self._calculate_dashboard_metrics(tenant_id, start_time, end_time)
        
        # Cache for 5 minutes
        await self.cache.set(cache_key, metrics, ttl=300)
        
        return metrics

    async def _cache_event(self, event: Event):
        """Cache event for real-time processing."""
        cache_key = f"events:{event.tenant_id}"
        event_data = {
            "id": str(event.id),
            "type": event.event_type,
            "timestamp": event.created_at.isoformat(),
            "data": event.event_data
        }
        
        # Add to recent events list (keep last 100)
        await self.cache.lpush(cache_key, json.dumps(event_data))
        await self.cache.ltrim(cache_key, 0, 99)

    async def _update_real_time_metrics(self, analytics: MessageAnalytics, tenant_id: str):
        """Update real-time metrics in cache."""
        current_hour = analytics.period_hour
        cache_key = f"metrics:{tenant_id}:{current_hour}"
        
        # Update counters
        await self.cache.hincrby(cache_key, "message_count", 1)
        await self.cache.hincrby(cache_key, f"{analytics.direction}_messages", 1)
        
        if analytics.sentiment_score is not None:
            await self.cache.hincrbyfloat(cache_key, "total_sentiment", analytics.sentiment_score)
            await self.cache.hincrby(cache_key, "sentiment_count", 1)
        
        if analytics.response_time is not None:
            await self.cache.hincrbyfloat(cache_key, "total_response_time", analytics.response_time)
            await self.cache.hincrby(cache_key, "response_time_count", 1)
        
        # Set TTL for 25 hours
        await self.cache.expire(cache_key, 25 * 3600)

    async def _calculate_dashboard_metrics(
        self,
        tenant_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, Any]:
        """Calculate dashboard metrics from database."""
        
        # Message analytics aggregation
        message_query = select(
            func.count(MessageAnalytics.id).label("total_messages"),
            func.sum(func.case((MessageAnalytics.direction == "inbound", 1), else_=0)).label("inbound_messages"),
            func.sum(func.case((MessageAnalytics.direction == "outbound", 1), else_=0)).label("outbound_messages"),
            func.avg(MessageAnalytics.sentiment_score).label("avg_sentiment"),
            func.avg(MessageAnalytics.response_time).label("avg_response_time")
        ).where(
            and_(
                MessageAnalytics.tenant_id == tenant_id,
                MessageAnalytics.created_at.between(start_time, end_time)
            )
        )
        
        result = await self.db.execute(message_query)
        message_stats = result.first()
        
        # Conversation analytics aggregation
        conversation_query = select(
            func.count(ConversationAnalytics.id).label("total_conversations"),
            func.avg(ConversationAnalytics.duration_minutes).label("avg_duration"),
            func.sum(func.case((ConversationAnalytics.resolution_status == "resolved", 1), else_=0)).label("resolved_conversations")
        ).where(
            and_(
                ConversationAnalytics.tenant_id == tenant_id,
                ConversationAnalytics.created_at.between(start_time, end_time)
            )
        )
        
        result = await self.db.execute(conversation_query)
        conversation_stats = result.first()
        
        return {
            "period": {"start": start_time, "end": end_time},
            "message_metrics": {
                "total": message_stats.total_messages or 0,
                "inbound": message_stats.inbound_messages or 0,
                "outbound": message_stats.outbound_messages or 0,
                "avg_sentiment": float(message_stats.avg_sentiment or 0),
                "avg_response_time": float(message_stats.avg_response_time or 0)
            },
            "conversation_metrics": {
                "total": conversation_stats.total_conversations or 0,
                "resolved": conversation_stats.resolved_conversations or 0,
                "avg_duration": float(conversation_stats.avg_duration or 0),
                "resolution_rate": (conversation_stats.resolved_conversations or 0) / max(conversation_stats.total_conversations or 1, 1) * 100
            }
        }
