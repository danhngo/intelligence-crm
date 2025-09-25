"""
REST API endpoints for the Workflow Engine Service.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from google.cloud import pubsub_v1

from . import WorkflowDefinition, WorkflowExecution
from .executor import WorkflowExecutor
from .storage import WorkflowStorage
from .triggers import TriggerManager, WorkflowTrigger

# Initialize router
router = APIRouter(prefix="/api/v1")

# Initialize services
workflow_storage = WorkflowStorage(project_id="your-project-id")
workflow_executor = WorkflowExecutor()
trigger_manager = TriggerManager()

# Initialize Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("your-project-id", "workflow-events")

@router.post("/workflows", response_model=WorkflowDefinition)
async def create_workflow(workflow: WorkflowDefinition):
    """Create a new workflow definition."""
    try:
        # Save workflow to Firestore
        workflow_id = await workflow_storage.save_workflow(workflow)
        
        # Register workflow triggers
        trigger_manager.register_trigger(workflow_id, workflow.trigger)
        
        return workflow
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/workflows", response_model=List[WorkflowDefinition])
async def list_workflows(active_only: bool = True):
    """List all workflow definitions."""
    try:
        workflows = await workflow_storage.list_workflows(active_only=active_only)
        return workflows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflows/{workflow_id}", response_model=WorkflowDefinition)
async def get_workflow(workflow_id: str):
    """Get a specific workflow definition."""
    workflow = await workflow_storage.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.post("/workflows/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: str,
    input_data: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Execute a workflow."""
    # Get workflow definition
    workflow = await workflow_storage.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
        
    try:
        # Execute workflow in background
        execution = WorkflowExecution(workflow_id=workflow_id)
        background_tasks.add_task(
            workflow_executor.execute_workflow,
            workflow,
            input_data
        )
        
        # Publish workflow.triggered event
        event_data = {
            "workflow_id": workflow_id,
            "execution_id": execution.id,
            "event": "workflow.triggered"
        }
        publisher.publish(topic_path, str(event_data).encode())
        
        return {"execution_id": execution.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/executions", response_model=List[WorkflowExecution])
async def list_executions(
    workflow_id: Optional[str] = None,
    status: Optional[str] = None
):
    """List workflow executions with optional filtering."""
    try:
        executions = await workflow_storage.list_executions(
            workflow_id=workflow_id,
            status=status
        )
        return executions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/executions/{execution_id}", response_model=WorkflowExecution)
async def get_execution(execution_id: str):
    """Get a specific workflow execution."""
    execution = await workflow_storage.get_execution(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution
