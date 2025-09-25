"""Simple workflow API endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class WorkflowCreate(BaseModel):
    """Workflow creation model."""
    name: str
    description: str = ""
    steps: List[Dict[str, Any]] = []
    triggers: List[str] = []


class WorkflowResponse(BaseModel):
    """Workflow response model."""
    id: str
    name: str
    description: str
    status: str
    created_at: str
    steps: List[Dict[str, Any]] = []


@router.get("/types", response_model=List[Dict[str, Any]])
async def get_workflow_types(
    db: AsyncSession = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get available workflow types."""
    # Mock implementation
    return [
        {
            "id": "lead-qualification",
            "name": "Lead Qualification",
            "description": "Automatically qualify and score incoming leads",
            "category": "sales",
            "triggers": ["new_lead", "lead_updated"]
        },
        {
            "id": "customer-onboarding",
            "name": "Customer Onboarding",
            "description": "Automated customer onboarding process",
            "category": "customer_success",
            "triggers": ["new_customer", "trial_started"]
        },
        {
            "id": "follow-up-sequence",
            "name": "Follow-up Sequence",
            "description": "Automated follow-up email sequence",
            "category": "marketing",
            "triggers": ["demo_completed", "proposal_sent"]
        },
        {
            "id": "support-escalation",
            "name": "Support Escalation",
            "description": "Escalate support tickets based on priority",
            "category": "support",
            "triggers": ["ticket_created", "sla_breach"]
        }
    ]


@router.get("/", response_model=List[WorkflowResponse])
async def list_workflows(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
) -> List[WorkflowResponse]:
    """List all workflows."""
    # Mock implementation
    import datetime
    
    workflows = []
    for i in range(min(limit, 10)):
        workflows.append(WorkflowResponse(
            id=f"wf-{offset + i + 1}",
            name=f"Workflow {offset + i + 1}",
            description=f"Description for workflow {offset + i + 1}",
            status="active" if i % 3 != 2 else "inactive",
            created_at=datetime.datetime.utcnow().isoformat(),
            steps=[
                {"type": "trigger", "name": "new_lead"},
                {"type": "condition", "name": "score > 80"},
                {"type": "action", "name": "assign_to_sales"}
            ]
        ))
    
    return workflows


@router.post("/", response_model=WorkflowResponse)
async def create_workflow(
    workflow: WorkflowCreate,
    db: AsyncSession = Depends(get_db)
) -> WorkflowResponse:
    """Create a new workflow."""
    # Mock implementation
    import uuid
    import datetime
    
    workflow_id = str(uuid.uuid4())
    
    return WorkflowResponse(
        id=workflow_id,
        name=workflow.name,
        description=workflow.description,
        status="active",
        created_at=datetime.datetime.utcnow().isoformat(),
        steps=workflow.steps
    )


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: str,
    db: AsyncSession = Depends(get_db)
) -> WorkflowResponse:
    """Get a specific workflow."""
    # Mock implementation
    import datetime
    
    return WorkflowResponse(
        id=workflow_id,
        name=f"Workflow {workflow_id}",
        description="Sample workflow description",
        status="active",
        created_at=datetime.datetime.utcnow().isoformat(),
        steps=[
            {"type": "trigger", "name": "new_lead"},
            {"type": "condition", "name": "score > 80"},
            {"type": "action", "name": "assign_to_sales"}
        ]
    )


@router.post("/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: str,
    input_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Execute a workflow with given input data."""
    # Mock implementation
    import uuid
    import datetime
    
    execution_id = str(uuid.uuid4())
    
    return {
        "execution_id": execution_id,
        "workflow_id": workflow_id,
        "status": "running",
        "started_at": datetime.datetime.utcnow().isoformat(),
        "input_data": input_data,
        "current_step": 1,
        "total_steps": 3
    }


@router.get("/{workflow_id}/executions")
async def list_workflow_executions(
    workflow_id: str,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
) -> List[Dict[str, Any]]:
    """List executions for a specific workflow."""
    # Mock implementation
    import datetime
    
    executions = []
    for i in range(min(limit, 5)):
        executions.append({
            "id": f"exec-{i + 1}",
            "workflow_id": workflow_id,
            "status": "completed" if i % 2 == 0 else "running",
            "started_at": datetime.datetime.utcnow().isoformat(),
            "completed_at": datetime.datetime.utcnow().isoformat() if i % 2 == 0 else None,
            "duration_seconds": 45 + i * 10 if i % 2 == 0 else None
        })
    
    return executions
