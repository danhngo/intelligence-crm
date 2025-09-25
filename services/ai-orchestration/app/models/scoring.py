"""Lead Scoring Models

This module defines the database models for AI-powered lead scoring, including
score components, explanations, and model performance tracking.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, Enum as SQLAEnum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base


class ScoreCategory(str, Enum):
    """Categories for lead scoring components."""
    ENGAGEMENT = "engagement"
    DEMOGRAPHICS = "demographics"
    BEHAVIOR = "behavior"
    INTENT = "intent"
    QUALIFICATION = "qualification"


class LeadScoreResult(Base):
    """Lead scoring results with explanations and tracking."""
    
    # Lead identification
    lead_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Score details
    score = Column(Integer, nullable=False)  # 0-100
    confidence = Column(Float, nullable=False)  # 0.0-1.0
    
    # Timing and expiration
    calculated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_expired = Column(Boolean, nullable=False, default=False)
    
    # Model information
    model_version = Column(String, nullable=False)
    model_parameters = Column(JSON, nullable=False)
    
    # Data sources used
    data_sources = Column(JSON, nullable=False)
    data_freshness = Column(JSON, nullable=False)
    
    # Score components and explanations
    score_components = relationship(
        "ScoreComponent",
        back_populates="lead_score",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # Workflow reference for audit trail
    workflow_id = Column(
        UUID(as_uuid=True),
        ForeignKey("workflowcontext.id"),
        nullable=False
    )
    
    # Performance tracking
    conversion_occurred = Column(Boolean)
    conversion_type = Column(String)
    conversion_value = Column(Float)
    conversion_date = Column(DateTime(timezone=True))
    
    def add_component(
        self,
        category: ScoreCategory,
        score: float,
        weight: float,
        explanation: str,
        evidence: Dict[str, Any]
    ) -> "ScoreComponent":
        """Add a new scoring component.
        
        Args:
            category: Score component category
            score: Component score value
            weight: Component weight in total score
            explanation: Human-readable explanation
            evidence: Supporting evidence/data
            
        Returns:
            Created ScoreComponent instance
        """
        component = ScoreComponent(
            lead_score=self,
            category=category,
            score=score,
            weight=weight,
            explanation=explanation,
            evidence=evidence
        )
        self.score_components.append(component)
        return component
    
    def record_conversion(
        self,
        conversion_type: str,
        conversion_value: float,
        conversion_date: Optional[datetime] = None
    ) -> None:
        """Record a conversion event for this lead.
        
        Args:
            conversion_type: Type of conversion
            conversion_value: Value of the conversion
            conversion_date: When conversion occurred (default now)
        """
        self.conversion_occurred = True
        self.conversion_type = conversion_type
        self.conversion_value = conversion_value
        self.conversion_date = conversion_date or datetime.utcnow()
    
    def mark_expired(self) -> None:
        """Mark this score as expired."""
        self.is_expired = True


class ScoreComponent(Base):
    """Individual component of a lead score."""
    
    # Score details
    category = Column(SQLAEnum(ScoreCategory), nullable=False)
    score = Column(Float, nullable=False)  # Raw component score
    weight = Column(Float, nullable=False)  # Weight in total score
    
    # Explanation
    explanation = Column(String, nullable=False)
    evidence = Column(JSON, nullable=False)
    
    # Link to parent score
    lead_score_id = Column(
        UUID(as_uuid=True),
        ForeignKey("leadscoreresult.id", ondelete="CASCADE"),
        nullable=False
    )
    lead_score = relationship("LeadScoreResult", back_populates="score_components")
    
    @property
    def weighted_score(self) -> float:
        """Calculate the weighted contribution to total score."""
        return self.score * self.weight
