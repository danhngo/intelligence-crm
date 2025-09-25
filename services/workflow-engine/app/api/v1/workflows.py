"""Workflow API endpoints."""

import uuid
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.workflow import (
    ExecutionStatus,
    Workflow as WorkflowModel,
    WorkflowExecution as WorkflowExecutionModel,
    WorkflowLog as WorkflowLogModel,
    WorkflowStatus
)
from app.schemas.workflow import (
    Workflow,
    WorkflowCreate,
    WorkflowExecution,
    WorkflowExecutionCreate,
    WorkflowLog,
    WorkflowUpdate
)
from app.services.workflow import WorkflowExecutionService

router = APIRouter()


@router.post("/workflows", response_model=Workflow)
async def create_workflow(
    workflow: WorkflowCreate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> WorkflowModel:
    """Create a new workflow."""
    db_workflow = WorkflowModel(**workflow.model_dump(), tenant_id=tenant_id)
    db.add(db_workflow)
    await db.commit()
    await db.refresh(db_workflow)
    return db_workflow


@router.get("/workflows", response_model=List[Workflow])
async def list_workflows(
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[uuid.UUID, Query()],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    status: Annotated[Optional[WorkflowStatus], Query()] = None
) -> List[WorkflowModel]:
    """List workflows."""
    query = select(WorkflowModel).where(
        WorkflowModel.tenant_id == tenant_id
    )
    
    if status:
        query = query.where(WorkflowModel.status == status)
        
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/workflows/{workflow_id}", response_model=Workflow)
async def get_workflow(
    workflow_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> WorkflowModel:
    """Get a specific workflow."""
    query = select(WorkflowModel).where(
        and_(
            WorkflowModel.id == workflow_id,
            WorkflowModel.tenant_id == tenant_id
        )
    )
    result = await db.execute(query)
    workflow = result.scalar_one_or_none()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
        
    return workflow


@router.put("/workflows/{workflow_id}", response_model=Workflow)
async def update_workflow(
    workflow_id: Annotated[uuid.UUID, Path()],
    workflow: WorkflowUpdate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> WorkflowModel:
    """Update a workflow."""
    # Get existing workflow
    query = select(WorkflowModel).where(
        and_(
            WorkflowModel.id == workflow_id,
            WorkflowModel.tenant_id == tenant_id
        )
    )
    result = await db.execute(query)
    db_workflow = result.scalar_one_or_none()
    
    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Create new version
    new_version = WorkflowModel(
        **workflow.model_dump(),
        tenant_id=tenant_id,
        version=db_workflow.version + 1
    )
    db_workflow.is_latest = False
    
    db.add(new_version)
    await db.commit()
    await db.refresh(new_version)
    
    return new_version


@router.post("/workflows/{workflow_id}/execute", response_model=WorkflowExecution)
async def execute_workflow(
    workflow_id: Annotated[uuid.UUID, Path()],
    execution: WorkflowExecutionCreate,
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> WorkflowExecutionModel:
    """Execute a workflow."""
    # Get workflow
    query = select(WorkflowModel).where(
        and_(
            WorkflowModel.id == workflow_id,
            WorkflowModel.tenant_id == tenant_id,
            WorkflowModel.status == WorkflowStatus.ACTIVE
        )
    )
    result = await db.execute(query)
    workflow = result.scalar_one_or_none()
    
    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Active workflow not found"
        )
    
    # Execute workflow
    service = WorkflowExecutionService(db)
    return await service.execute_workflow(
        workflow,
        execution.input_data,
        tenant_id
    )


@router.get("/executions", response_model=List[WorkflowExecution])
async def list_executions(
    tenant_id: Annotated[uuid.UUID, Query()],
    workflow_id: Annotated[Optional[uuid.UUID], Query()] = None,
    status: Annotated[Optional[ExecutionStatus], Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> List[WorkflowExecutionModel]:
    """List workflow executions."""
    query = select(WorkflowExecutionModel).where(
        WorkflowExecutionModel.tenant_id == tenant_id
    )
    
    if workflow_id:
        query = query.where(WorkflowExecutionModel.workflow_id == workflow_id)
        
    if status:
        query = query.where(WorkflowExecutionModel.status == status)
        
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/executions/{execution_id}", response_model=WorkflowExecution)
async def get_execution(
    execution_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> WorkflowExecutionModel:
    """Get a specific workflow execution."""
    query = select(WorkflowExecutionModel).where(
        and_(
            WorkflowExecutionModel.id == execution_id,
            WorkflowExecutionModel.tenant_id == tenant_id
        )
    )
    result = await db.execute(query)
    execution = result.scalar_one_or_none()
    
    if not execution:
        raise HTTPException(
            status_code=404,
            detail="Workflow execution not found"
        )
        
    return execution


@router.get("/executions/{execution_id}/logs", response_model=List[WorkflowLog])
async def get_execution_logs(
    execution_id: Annotated[uuid.UUID, Path()],
    tenant_id: Annotated[uuid.UUID, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> List[WorkflowLogModel]:
    """Get logs for a specific workflow execution."""
    query = select(WorkflowLogModel).where(
        and_(
            WorkflowLogModel.execution_id == execution_id,
            WorkflowLogModel.tenant_id == tenant_id
        )
    ).order_by(WorkflowLogModel.timestamp)
    
    result = await db.execute(query)
    return result.scalars().all()
