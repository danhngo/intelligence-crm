"""Workflow schemas."""

import uuid
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from app.models.workflow import ExecutionStatus, StepType, TriggerType, WorkflowStatus


class WorkflowStepBase(BaseModel):
    """Base schema for workflow steps."""
    
    type: StepType
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class HTTPRequestStep(WorkflowStepBase):
    """Schema for HTTP request step."""
    
    type: StepType = StepType.HTTP_REQUEST
    method: str = Field(pattern="^(GET|POST|PUT|DELETE|PATCH)$")
    url: str
    headers: dict[str, str] = Field(default_factory=dict)
    body: Optional[dict[str, Any]] = None
    timeout: int = Field(default=30, ge=1, le=300)
    output_key: Optional[str] = None


class ConditionStep(WorkflowStepBase):
    """Schema for condition step."""
    
    type: StepType = StepType.CONDITION
    condition: dict[str, Any]
    output_key: Optional[str] = None


class EmailStep(WorkflowStepBase):
    """Schema for email step."""
    
    type: StepType = StepType.EMAIL
    to: List[str]
    subject: str
    body: str
    output_key: Optional[str] = None


class DelayStep(WorkflowStepBase):
    """Schema for delay step."""
    
    type: StepType = StepType.DELAY
    seconds: int = Field(ge=0, le=86400)  # Max 24 hours


class FunctionStep(WorkflowStepBase):
    """Schema for function step."""
    
    type: StepType = StepType.FUNCTION
    function: str
    params: dict[str, Any] = Field(default_factory=dict)
    output_key: Optional[str] = None


class WorkflowBase(BaseModel):
    """Base schema for workflow."""
    
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    trigger_type: TriggerType
    trigger_config: dict[str, Any] = Field(default_factory=dict)
    steps: List[dict[str, Any]]  # Can be any of the step types
    status: WorkflowStatus = WorkflowStatus.DRAFT


class WorkflowCreate(WorkflowBase):
    """Schema for creating a workflow."""
    pass


class WorkflowUpdate(WorkflowBase):
    """Schema for updating a workflow."""
    pass


class Workflow(WorkflowBase):
    """Schema for workflow response."""
    
    id: uuid.UUID
    tenant_id: uuid.UUID
    version: int
    is_latest: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class WorkflowExecutionCreate(BaseModel):
    """Schema for creating a workflow execution."""
    
    input_data: dict[str, Any] = Field(default_factory=dict)


class WorkflowExecution(BaseModel):
    """Schema for workflow execution response."""
    
    id: uuid.UUID
    workflow_id: uuid.UUID
    tenant_id: uuid.UUID
    status: ExecutionStatus
    current_step: Optional[int] = None
    input_data: dict[str, Any]
    output_data: dict[str, Any]
    error_data: Optional[dict[str, Any]] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    retries: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class WorkflowLog(BaseModel):
    """Schema for workflow log response."""
    
    id: uuid.UUID
    execution_id: uuid.UUID
    tenant_id: uuid.UUID
    step: int
    step_type: StepType
    message: str
    details: Optional[dict[str, Any]] = None
    timestamp: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True
