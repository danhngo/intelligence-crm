"""AI Context Repository

This module implements the data access layer for AI workflow contexts with tenant
isolation, conversation memory management, and context pruning capabilities.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from uuid import UUID

import structlog
from sqlalchemy import select, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.workflow import (
    WorkflowContext, 
    WorkflowStatus,
    WorkflowType,
    ConversationTurn,
    ExecutionStep
)
from app.core.config import settings

logger = structlog.get_logger(__name__)


class AIContextRepository:
    """Repository for managing AI workflow contexts and conversation memory."""

    def __init__(self, session: AsyncSession):
        """Initialize repository.
        
        Args:
            session: SQLAlchemy async session
        """
        self._session = session
        self._tenant_id = session.info.get("tenant_id")
        if not self._tenant_id:
            raise ValueError("Tenant ID is required for AI context operations")

    async def create_workflow(
        self,
        workflow_type: WorkflowType,
        input_data: Dict[str, Any],
        customer_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> WorkflowContext:
        """Create a new workflow context.
        
        Args:
            workflow_type: Type of workflow to create
            input_data: Initial input data
            customer_id: Optional customer ID
            user_id: Optional user ID
            metadata: Optional workflow metadata
            
        Returns:
            Created WorkflowContext instance
        """
        workflow = WorkflowContext(
            tenant_id=self._tenant_id,
            workflow_type=workflow_type,
            customer_id=customer_id,
            user_id=user_id,
            input_data=input_data,
            metadata=metadata or {},
            status=WorkflowStatus.PENDING,
            started_at=datetime.utcnow()
        )
        
        self._session.add(workflow)
        await self._session.flush()
        
        logger.info(
            "Created workflow context",
            workflow_id=workflow.id,
            workflow_type=workflow_type,
            tenant_id=self._tenant_id
        )
        
        return workflow

    async def get_workflow(
        self,
        workflow_id: UUID,
        include_conversation: bool = True,
        include_steps: bool = True
    ) -> Optional[WorkflowContext]:
        """Get workflow context by ID.
        
        Args:
            workflow_id: Workflow context ID
            include_conversation: Whether to load conversation turns
            include_steps: Whether to load execution steps
            
        Returns:
            WorkflowContext if found, None otherwise
        """
        query = select(WorkflowContext).where(
            WorkflowContext.id == workflow_id,
            WorkflowContext.tenant_id == self._tenant_id
        )
        
        if not include_conversation:
            query = query.options(selectinload(WorkflowContext.conversation_turns))
        if not include_steps:
            query = query.options(selectinload(WorkflowContext.execution_steps))
            
        result = await self._session.execute(query)
        workflow = result.scalar_one_or_none()
        
        if workflow:
            logger.debug(
                "Retrieved workflow context",
                workflow_id=workflow_id,
                tenant_id=self._tenant_id
            )
        else:
            logger.debug(
                "Workflow context not found",
                workflow_id=workflow_id,
                tenant_id=self._tenant_id
            )
            
        return workflow

    async def get_active_workflows(
        self,
        workflow_type: Optional[WorkflowType] = None,
        customer_id: Optional[UUID] = None,
        limit: int = 100
    ) -> List[WorkflowContext]:
        """Get active (non-completed) workflows.
        
        Args:
            workflow_type: Optional workflow type filter
            customer_id: Optional customer ID filter
            limit: Maximum number of workflows to return
            
        Returns:
            List of active WorkflowContext instances
        """
        query = select(WorkflowContext).where(
            WorkflowContext.tenant_id == self._tenant_id,
            WorkflowContext.status.in_([
                WorkflowStatus.PENDING,
                WorkflowStatus.RUNNING,
                WorkflowStatus.PAUSED
            ])
        )
        
        if workflow_type:
            query = query.where(WorkflowContext.workflow_type == workflow_type)
        if customer_id:
            query = query.where(WorkflowContext.customer_id == customer_id)
            
        query = query.order_by(desc(WorkflowContext.started_at)).limit(limit)
        
        result = await self._session.execute(query)
        workflows = result.scalars().all()
        
        logger.debug(
            "Retrieved active workflows",
            count=len(workflows),
            workflow_type=workflow_type,
            tenant_id=self._tenant_id
        )
        
        return workflows

    async def update_workflow_status(
        self,
        workflow_id: UUID,
        status: WorkflowStatus,
        output_data: Optional[Dict[str, Any]] = None,
        error: Optional[Dict[str, Any]] = None
    ) -> Optional[WorkflowContext]:
        """Update workflow status and completion data.
        
        Args:
            workflow_id: Workflow context ID
            status: New workflow status
            output_data: Optional output data if completed
            error: Optional error data if failed
            
        Returns:
            Updated WorkflowContext if found, None otherwise
        """
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None
            
        workflow.status = status
        if status == WorkflowStatus.COMPLETED:
            workflow.output_data = output_data
            workflow.completed_at = datetime.utcnow()
            workflow.duration = int(
                (workflow.completed_at - workflow.started_at).total_seconds() * 1000
            )
        elif status == WorkflowStatus.FAILED:
            workflow.error = error
            workflow.completed_at = datetime.utcnow()
            workflow.duration = int(
                (workflow.completed_at - workflow.started_at).total_seconds() * 1000
            )
            
        await self._session.flush()
        
        logger.info(
            "Updated workflow status",
            workflow_id=workflow_id,
            status=status,
            tenant_id=self._tenant_id
        )
        
        return workflow

    async def add_conversation_turn(
        self,
        workflow_id: UUID,
        role: str,
        content: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Tuple[WorkflowContext, ConversationTurn]]:
        """Add a conversation turn to workflow context.
        
        Args:
            workflow_id: Workflow context ID
            role: Role who generated the message
            content: Message content
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens used
            metadata: Optional message metadata
            
        Returns:
            Tuple of (WorkflowContext, ConversationTurn) if successful, None otherwise
        """
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None
            
        turn = workflow.add_conversation_turn(
            role=role,
            content=content,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            metadata=metadata
        )
        
        # Update workflow token usage
        workflow.total_tokens += input_tokens + output_tokens
        await self._session.flush()
        
        logger.debug(
            "Added conversation turn",
            workflow_id=workflow_id,
            role=role,
            tenant_id=self._tenant_id
        )
        
        return workflow, turn

    async def get_conversation_context(
        self,
        workflow_id: UUID,
        max_turns: Optional[int] = None,
        max_tokens: Optional[int] = None
    ) -> List[ConversationTurn]:
        """Get conversation context with optional limits.
        
        Args:
            workflow_id: Workflow context ID
            max_turns: Maximum number of turns to return
            max_tokens: Maximum total tokens in returned context
            
        Returns:
            List of ConversationTurn instances
        """
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return []
            
        turns = workflow.conversation_turns
        
        if max_turns:
            turns = turns[-max_turns:]
            
        if max_tokens:
            total_tokens = 0
            filtered_turns = []
            
            for turn in reversed(turns):
                turn_tokens = turn.input_tokens + turn.output_tokens
                if total_tokens + turn_tokens > max_tokens:
                    break
                    
                filtered_turns.insert(0, turn)
                total_tokens += turn_tokens
                
            turns = filtered_turns
            
        logger.debug(
            "Retrieved conversation context",
            workflow_id=workflow_id,
            turn_count=len(turns),
            tenant_id=self._tenant_id
        )
        
        return turns

    async def add_execution_step(
        self,
        workflow_id: UUID,
        step_name: str,
        step_type: str,
        input_data: Dict[str, Any]
    ) -> Optional[Tuple[WorkflowContext, ExecutionStep]]:
        """Add execution step to workflow context.
        
        Args:
            workflow_id: Workflow context ID
            step_name: Name of execution step
            step_type: Type of step
            input_data: Step input data
            
        Returns:
            Tuple of (WorkflowContext, ExecutionStep) if successful, None otherwise
        """
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None
            
        step = workflow.add_execution_step(
            step_name=step_name,
            step_type=step_type,
            input_data=input_data
        )
        
        await self._session.flush()
        
        logger.debug(
            "Added execution step",
            workflow_id=workflow_id,
            step_name=step_name,
            tenant_id=self._tenant_id
        )
        
        return workflow, step

    async def complete_execution_step(
        self,
        workflow_id: UUID,
        step_id: UUID,
        output_data: Dict[str, Any],
        tokens_used: int = 0,
        error: Optional[Dict[str, Any]] = None
    ) -> Optional[Tuple[WorkflowContext, ExecutionStep]]:
        """Complete an execution step.
        
        Args:
            workflow_id: Workflow context ID
            step_id: Execution step ID
            output_data: Step output data
            tokens_used: Number of tokens used
            error: Optional error information
            
        Returns:
            Tuple of (WorkflowContext, ExecutionStep) if successful, None otherwise
        """
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None
            
        step = next((s for s in workflow.execution_steps if s.id == step_id), None)
        if not step:
            return None
            
        workflow.complete_execution_step(
            step=step,
            output_data=output_data,
            tokens_used=tokens_used,
            error=error
        )
        
        await self._session.flush()
        
        logger.debug(
            "Completed execution step",
            workflow_id=workflow_id,
            step_id=step_id,
            tenant_id=self._tenant_id,
            error=bool(error)
        )
        
        return workflow, step

    async def prune_conversation_context(
        self,
        workflow_id: UUID,
        max_turns: Optional[int] = None,
        max_tokens: Optional[int] = None,
        preserve_last_n: int = 5
    ) -> Optional[int]:
        """Prune conversation context to reduce memory usage.
        
        Args:
            workflow_id: Workflow context ID
            max_turns: Maximum turns to keep
            max_tokens: Maximum tokens to keep
            preserve_last_n: Number of most recent turns to preserve
            
        Returns:
            Number of turns pruned if successful, None if workflow not found
        """
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None
            
        original_count = len(workflow.conversation_turns)
        turns = workflow.conversation_turns
        
        # Always preserve most recent turns
        if preserve_last_n:
            preserved = turns[-preserve_last_n:]
            turns = turns[:-preserve_last_n]
        else:
            preserved = []
            
        # Apply turn limit
        if max_turns and len(turns) > max_turns:
            turns = turns[-max_turns:]
            
        # Apply token limit
        if max_tokens:
            total_tokens = sum(t.input_tokens + t.output_tokens for t in preserved)
            filtered_turns = []
            
            for turn in reversed(turns):
                turn_tokens = turn.input_tokens + turn.output_tokens
                if total_tokens + turn_tokens > max_tokens:
                    break
                    
                filtered_turns.insert(0, turn)
                total_tokens += turn_tokens
                
            turns = filtered_turns
            
        # Update workflow with pruned context
        workflow.conversation_turns = turns + preserved
        await self._session.flush()
        
        pruned_count = original_count - len(workflow.conversation_turns)
        
        logger.info(
            "Pruned conversation context",
            workflow_id=workflow_id,
            pruned_count=pruned_count,
            remaining_count=len(workflow.conversation_turns),
            tenant_id=self._tenant_id
        )
        
        return pruned_count
