"""Workflow models."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, List

from sqlalchemy import JSON, Boolean, DateTime, Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TenantMixin, TimestampMixin


class TriggerType(str, Enum):
    """Types of workflow triggers."""
    
    EVENT = "event"
    SCHEDULE = "schedule"
    MANUAL = "manual"
    API = "api"


class WorkflowStatus(str, Enum):
    """Status of a workflow definition."""
    
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DISABLED = "disabled"


class ExecutionStatus(str, Enum):
    """Status of a workflow execution."""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"


class StepType(str, Enum):
    """Types of workflow steps."""
    
    HTTP_REQUEST = "http_request"
    CONDITION = "condition"
    EMAIL = "email"
    DELAY = "delay"
    FUNCTION = "function"
    SUBPROCESS = "subprocess"


class Workflow(Base, TenantMixin, TimestampMixin):
    """Workflow definition model."""
    
    __tablename__ = "workflows"
    
    id: Mapped[uuid.UUID] = mapped_column(
        String(36),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    trigger_type: Mapped[TriggerType] = mapped_column(SQLEnum(TriggerType))
    trigger_config: Mapped[dict[str, Any]] = mapped_column(JSON)
    steps: Mapped[list[dict[str, Any]]] = mapped_column(JSON)
    status: Mapped[WorkflowStatus] = mapped_column(
        SQLEnum(WorkflowStatus),
        default=WorkflowStatus.DRAFT
    )
    version: Mapped[int] = mapped_column(default=1)
    is_latest: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    executions: Mapped[List["WorkflowExecution"]] = relationship(
        back_populates="workflow"
    )


class WorkflowExecution(Base, TenantMixin, TimestampMixin):
    """Workflow execution instance model."""
    
    __tablename__ = "workflow_executions"
    
    id: Mapped[uuid.UUID] = mapped_column(
        String(36),
        primary_key=True,
        default=uuid.uuid4
    )
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        String(36),
        ForeignKey("workflows.id")
    )
    status: Mapped[ExecutionStatus] = mapped_column(
        SQLEnum(ExecutionStatus),
        default=ExecutionStatus.PENDING
    )
    current_step: Mapped[int | None] = mapped_column(nullable=True)
    input_data: Mapped[dict[str, Any]] = mapped_column(JSON)
    output_data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    error_data: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retries: Mapped[int] = mapped_column(default=0)
    
    # Relationships
    workflow: Mapped[Workflow] = relationship(back_populates="executions")


class WorkflowLog(Base, TenantMixin):
    """Workflow execution log model."""
    
    __tablename__ = "workflow_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(
        String(36),
        primary_key=True,
        default=uuid.uuid4
    )
    execution_id: Mapped[uuid.UUID] = mapped_column(
        String(36),
        ForeignKey("workflow_executions.id")
    )
    step: Mapped[int] = mapped_column()
    step_type: Mapped[StepType] = mapped_column(SQLEnum(StepType))
    message: Mapped[str] = mapped_column(String(1000))
    details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
