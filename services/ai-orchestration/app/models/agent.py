"""Agent State Models

This module defines the database models for LangGraph agent state management,
inter-agent communication, and workflow coordination.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

from sqlalchemy import Column, DateTime, String, JSON, ForeignKey, Enum as SQLAEnum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base


class AgentType(str, Enum):
    """Types of AI agents in the system."""
    LEAD_ANALYZER = "lead_analyzer"
    CONTENT_GENERATOR = "content_generator"
    DECISION_MAKER = "decision_maker"
    COORDINATOR = "coordinator"


class AgentStatus(str, Enum):
    """Status of an agent's execution."""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentAction(Base):
    """Individual action taken by an agent."""
    
    # Action details
    action_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    # Execution timing
    started_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime(timezone=True))
    duration = Column(Integer)  # milliseconds
    
    # Action data
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON)
    
    # Success/failure tracking
    success = Column(SQLAEnum(AgentStatus), nullable=False)
    error = Column(JSON)
    
    # Token usage
    tokens_used = Column(Integer, default=0)
    cost = Column(Integer, default=0)  # microcents
    
    # Link to parent agent state
    agent_state_id = Column(
        UUID(as_uuid=True),
        ForeignKey("agentstate.id", ondelete="CASCADE"),
        nullable=False
    )
    agent_state = relationship("AgentState", back_populates="execution_history")


class AgentState(Base):
    """State tracking for individual agents in multi-agent workflows."""
    
    # Agent identification
    agent_type = Column(SQLAEnum(AgentType), nullable=False)
    name = Column(String, nullable=False)
    status = Column(SQLAEnum(AgentStatus), nullable=False, default=AgentStatus.IDLE)
    
    # Workflow context
    workflow_id = Column(
        UUID(as_uuid=True),
        ForeignKey("workflowcontext.id"),
        nullable=False
    )
    current_step = Column(String)
    step_started_at = Column(DateTime(timezone=True))
    
    # Agent memory and state
    local_memory = Column(JSON, nullable=False, default=dict)
    shared_memory = Column(JSON, nullable=False, default=dict)
    
    # Execution state
    current_observation = Column(JSON)
    next_action = Column(JSON)
    action_queue = Column(JSON, default=list)
    
    # Dependencies and coordination
    depends_on = Column(JSON, default=list)  # List of agent IDs this agent depends on
    blocks = Column(JSON, default=list)  # List of agent IDs blocked by this agent
    
    # Performance metrics
    total_actions = Column(Integer, default=0)
    successful_actions = Column(Integer, default=0)
    failed_actions = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Integer, default=0)  # microcents
    
    # Action history
    execution_history = relationship(
        "AgentAction",
        back_populates="agent_state",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="AgentAction.started_at"
    )
    
    def add_action(
        self,
        action_type: str,
        description: str,
        input_data: Dict[str, Any]
    ) -> AgentAction:
        """Record a new action taken by this agent.
        
        Args:
            action_type: Type of action being taken
            description: Human-readable description
            input_data: Input data for the action
            
        Returns:
            Created AgentAction instance
        """
        action = AgentAction(
            agent_state=self,
            action_type=action_type,
            description=description,
            input_data=input_data,
            success=AgentStatus.WORKING
        )
        self.execution_history.append(action)
        self.total_actions += 1
        return action
    
    def complete_action(
        self,
        action: AgentAction,
        output_data: Dict[str, Any],
        tokens_used: int = 0,
        cost: int = 0,
        error: Optional[Dict[str, Any]] = None
    ) -> None:
        """Complete a previously started action.
        
        Args:
            action: AgentAction instance to complete
            output_data: Output/results from the action
            tokens_used: Number of tokens used
            cost: Cost in microcents
            error: Optional error information
        """
        action.completed_at = datetime.utcnow()
        action.duration = int((action.completed_at - action.started_at).total_seconds() * 1000)
        action.output_data = output_data
        action.tokens_used = tokens_used
        action.cost = cost
        
        if error:
            action.success = AgentStatus.FAILED
            action.error = error
            self.failed_actions += 1
        else:
            action.success = AgentStatus.COMPLETED
            self.successful_actions += 1
        
        self.total_tokens += tokens_used
        self.total_cost += cost
    
    def update_memory(
        self,
        local_updates: Optional[Dict[str, Any]] = None,
        shared_updates: Optional[Dict[str, Any]] = None
    ) -> None:
        """Update agent memory state.
        
        Args:
            local_updates: Updates to local memory
            shared_updates: Updates to shared memory
        """
        if local_updates:
            self.local_memory.update(local_updates)
        
        if shared_updates:
            self.shared_memory.update(shared_updates)
    
    def set_next_action(
        self,
        action: Dict[str, Any],
        observation: Optional[Dict[str, Any]] = None
    ) -> None:
        """Set the next action for this agent.
        
        Args:
            action: Next action to take
            observation: Optional current observation
        """
        self.next_action = action
        if observation:
            self.current_observation = observation
    
    def queue_action(self, action: Dict[str, Any]) -> None:
        """Add an action to the agent's queue.
        
        Args:
            action: Action to queue
        """
        if not isinstance(self.action_queue, list):
            self.action_queue = []
        self.action_queue.append(action)
    
    def get_next_queued_action(self) -> Optional[Dict[str, Any]]:
        """Get next action from queue.
        
        Returns:
            Next queued action if available, None otherwise
        """
        if not self.action_queue:
            return None
        return self.action_queue.pop(0)
