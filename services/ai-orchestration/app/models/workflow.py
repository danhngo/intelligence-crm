"""Workflow Models

This module defines the database models for LangChain workflow state tracking,
conversation memory management, and execution monitoring.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

from sqlalchemy import Column, DateTime, Integer, String, JSON, ForeignKey, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base


class WorkflowStatus(str, Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class WorkflowType(str, Enum):
    """Types of AI workflows."""
    LEAD_SCORING = "lead_scoring"
    CUSTOMER_INSIGHT = "customer_insight"
    CONTENT_GENERATION = "content_generation"
    DECISION_MAKING = "decision_making"


class ConversationTurn(Base):
    """Individual turn in a workflow conversation."""
    
    # Role who generated this message
    role = Column(String, nullable=False)
    
    # Message content
    content = Column(String, nullable=False)
    
    # Token usage metrics
    input_tokens = Column(Integer, nullable=False, default=0)
    output_tokens = Column(Integer, nullable=False, default=0)
    
    # Metadata about the turn (e.g., model used, confidence)
    metadata = Column(JSON, nullable=False, default=dict)
    
    # Link to parent workflow
    workflow_id = Column(
        UUID(as_uuid=True),
        ForeignKey("workflowcontext.id", ondelete="CASCADE"),
        nullable=False
    )
    workflow = relationship("WorkflowContext", back_populates="conversation_turns")


class ExecutionStep(Base):
    """Individual step in workflow execution."""
    
    # Step identifier and type
    step_name = Column(String, nullable=False)
    step_type = Column(String, nullable=False)
    
    # Execution timing
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True))
    duration = Column(Integer)  # milliseconds
    
    # Step inputs and outputs
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON)
    
    # Error details if failed
    error = Column(JSON)
    
    # Token usage for this step
    tokens_used = Column(Integer, default=0)
    
    # Link to parent workflow
    workflow_id = Column(
        UUID(as_uuid=True),
        ForeignKey("workflowcontext.id", ondelete="CASCADE"),
        nullable=False
    )
    workflow = relationship("WorkflowContext", back_populates="execution_steps")


class WorkflowContext(Base):
    """Main workflow context tracking model."""
    
    # Workflow identification
    workflow_type = Column(SQLAEnum(WorkflowType), nullable=False)
    status = Column(SQLAEnum(WorkflowStatus), nullable=False, default=WorkflowStatus.PENDING)
    
    # Execution timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration = Column(Integer)  # milliseconds
    
    # Workflow data
    input_data = Column(JSON, nullable=False, default=dict)
    output_data = Column(JSON)
    metadata = Column(JSON, nullable=False, default=dict)
    
    # Error tracking
    error = Column(JSON)
    retry_count = Column(Integer, default=0)
    last_error_at = Column(DateTime(timezone=True))
    
    # Usage metrics
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Integer, default=0)  # Cost in microcents (1/1,000,000 of a cent)
    
    # External entity links
    customer_id = Column(UUID(as_uuid=True), index=True)
    user_id = Column(UUID(as_uuid=True), index=True)
    
    # Conversation memory and execution tracking
    conversation_turns = relationship(
        "ConversationTurn",
        back_populates="workflow",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    execution_steps = relationship(
        "ExecutionStep",
        back_populates="workflow",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    def add_conversation_turn(
        self,
        role: str,
        content: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ConversationTurn:
        """Add a new conversation turn to this workflow.
        
        Args:
            role: Role who generated the message (human/ai/system)
            content: Message content
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens used
            metadata: Optional metadata about the turn
            
        Returns:
            Created ConversationTurn instance
        """
        turn = ConversationTurn(
            workflow=self,
            role=role,
            content=content,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            metadata=metadata or {}
        )
        self.conversation_turns.append(turn)
        self.total_tokens += input_tokens + output_tokens
        return turn
    
    def add_execution_step(
        self,
        step_name: str,
        step_type: str,
        input_data: Dict[str, Any],
        started_at: Optional[datetime] = None
    ) -> ExecutionStep:
        """Add a new execution step to this workflow.
        
        Args:
            step_name: Name of the execution step
            step_type: Type of step (e.g., llm_call, tool_use)
            input_data: Input data for the step
            started_at: Optional start time (defaults to now)
            
        Returns:
            Created ExecutionStep instance
        """
        step = ExecutionStep(
            workflow=self,
            step_name=step_name,
            step_type=step_type,
            input_data=input_data,
            started_at=started_at or datetime.utcnow()
        )
        self.execution_steps.append(step)
        return step
    
    def complete_execution_step(
        self,
        step: ExecutionStep,
        output_data: Dict[str, Any],
        tokens_used: int = 0,
        error: Optional[Dict[str, Any]] = None
    ) -> None:
        """Complete an execution step with results.
        
        Args:
            step: ExecutionStep instance to complete
            output_data: Output data from the step
            tokens_used: Number of tokens used in this step
            error: Optional error information if step failed
        """
        step.completed_at = datetime.utcnow()
        step.duration = int((step.completed_at - step.started_at).total_seconds() * 1000)
        step.output_data = output_data
        step.tokens_used = tokens_used
        step.error = error
        
        # Update workflow totals
        self.total_tokens += tokens_used
        
        # Update workflow status on error
        if error:
            self.error = error
            self.status = WorkflowStatus.FAILED
            self.last_error_at = step.completed_at
            self.retry_count += 1
    
    def complete_workflow(
        self,
        output_data: Dict[str, Any],
        status: WorkflowStatus = WorkflowStatus.COMPLETED
    ) -> None:
        """Complete the workflow with final results.
        
        Args:
            output_data: Final workflow output data
            status: Final workflow status
        """
        self.completed_at = datetime.utcnow()
        self.duration = int((self.completed_at - self.started_at).total_seconds() * 1000)
        self.output_data = output_data
        self.status = status
