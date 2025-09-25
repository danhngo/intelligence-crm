"""Customer Insights Models

This module defines the database models for AI-generated customer insights,
recommendations, and customer journey analysis.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

from sqlalchemy import Column, DateTime, String, JSON, ForeignKey, Enum as SQLAEnum, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from app.models.base import Base


class InsightType(str, Enum):
    """Types of customer insights."""
    BEHAVIOR_PATTERN = "behavior_pattern"
    PURCHASE_INTENT = "purchase_intent"
    CHURN_RISK = "churn_risk"
    UPSELL_OPPORTUNITY = "upsell_opportunity"
    SATISFACTION_LEVEL = "satisfaction_level"
    SENTIMENT_CHANGE = "sentiment_change"


class InsightPriority(str, Enum):
    """Priority levels for insights and recommendations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class InsightStatus(str, Enum):
    """Status of an insight."""
    ACTIVE = "active"
    ACTIONED = "actioned"
    DISMISSED = "dismissed"
    EXPIRED = "expired"


class Recommendation(Base):
    """Actionable recommendation derived from an insight."""
    
    # Recommendation details
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(SQLAEnum(InsightPriority), nullable=False)
    
    # Action planning
    suggested_actions = Column(ARRAY(String), nullable=False)
    estimated_impact = Column(String, nullable=False)
    effort_level = Column(String, nullable=False)
    
    # Implementation tracking
    is_implemented = Column(Boolean, nullable=False, default=False)
    implemented_at = Column(DateTime(timezone=True))
    implementation_notes = Column(String)
    
    # Results tracking
    actual_impact = Column(JSON)
    impact_metrics = Column(JSON)
    
    # Link to parent insight
    insight_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customerinsight.id", ondelete="CASCADE"),
        nullable=False
    )
    insight = relationship("CustomerInsight", back_populates="recommendations")
    
    def implement(
        self,
        notes: Optional[str] = None,
        impact_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Mark recommendation as implemented.
        
        Args:
            notes: Optional implementation notes
            impact_data: Optional impact measurement data
        """
        self.is_implemented = True
        self.implemented_at = datetime.utcnow()
        if notes:
            self.implementation_notes = notes
        if impact_data:
            self.actual_impact = impact_data


class CustomerInsight(Base):
    """AI-generated customer insight with recommendations."""
    
    # Customer identification
    customer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Insight details
    insight_type = Column(SQLAEnum(InsightType), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    # Confidence and impact
    confidence = Column(Float, nullable=False)  # 0.0-1.0
    priority = Column(SQLAEnum(InsightPriority), nullable=False)
    impact_score = Column(Integer, nullable=False)  # 1-10
    
    # Status tracking
    status = Column(SQLAEnum(InsightStatus), nullable=False, default=InsightStatus.ACTIVE)
    generated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    actioned_at = Column(DateTime(timezone=True))
    
    # Supporting data
    data_sources = Column(JSON, nullable=False)
    supporting_evidence = Column(JSON, nullable=False)
    
    # Historical context
    previous_insights = Column(ARRAY(UUID(as_uuid=True)))
    related_insights = Column(ARRAY(UUID(as_uuid=True)))
    
    # Actionable recommendations
    recommendations = relationship(
        "Recommendation",
        back_populates="insight",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # Workflow reference
    workflow_id = Column(
        UUID(as_uuid=True),
        ForeignKey("workflowcontext.id"),
        nullable=False
    )
    
    def add_recommendation(
        self,
        title: str,
        description: str,
        priority: InsightPriority,
        suggested_actions: List[str],
        estimated_impact: str,
        effort_level: str
    ) -> Recommendation:
        """Add a new recommendation for this insight.
        
        Args:
            title: Recommendation title
            description: Detailed description
            priority: Priority level
            suggested_actions: List of suggested actions
            estimated_impact: Estimated business impact
            effort_level: Required effort level
            
        Returns:
            Created Recommendation instance
        """
        rec = Recommendation(
            insight=self,
            title=title,
            description=description,
            priority=priority,
            suggested_actions=suggested_actions,
            estimated_impact=estimated_impact,
            effort_level=effort_level
        )
        self.recommendations.append(rec)
        return rec
    
    def mark_actioned(self) -> None:
        """Mark insight as actioned."""
        self.status = InsightStatus.ACTIONED
        self.actioned_at = datetime.utcnow()
    
    def mark_expired(self) -> None:
        """Mark insight as expired."""
        self.status = InsightStatus.EXPIRED
    
    def dismiss(self) -> None:
        """Dismiss this insight."""
        self.status = InsightStatus.DISMISSED
        
    def is_active(self) -> bool:
        """Check if insight is still active."""
        return (
            self.status == InsightStatus.ACTIVE
            and datetime.utcnow() < self.expires_at
        )
    
    def get_pending_recommendations(self) -> List[Recommendation]:
        """Get list of pending (not implemented) recommendations.
        
        Returns:
            List of pending Recommendation instances
        """
        return [r for r in self.recommendations if not r.is_implemented]
    
    def get_implemented_recommendations(self) -> List[Recommendation]:
        """Get list of implemented recommendations.
        
        Returns:
            List of implemented Recommendation instances
        """
        return [r for r in self.recommendations if r.is_implemented]
