"""
Storage interface for workflow state persistence using Firestore.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from google.cloud import firestore
from . import WorkflowDefinition, WorkflowExecution

class WorkflowStorage:
    """Storage interface for workflow state persistence."""
    
    def __init__(self, project_id: str):
        """Initialize Firestore client."""
        self.db = firestore.Client(project=project_id)
        self.workflows_collection = self.db.collection('workflows')
        self.executions_collection = self.db.collection('workflow_executions')
        
    async def save_workflow(self, workflow: WorkflowDefinition) -> str:
        """Save workflow definition to Firestore."""
        workflow_ref = self.workflows_collection.document(workflow.id)
        workflow_ref.set(workflow.dict())
        return workflow.id
        
    async def get_workflow(self, workflow_id: str) -> Optional[WorkflowDefinition]:
        """Retrieve workflow definition from Firestore."""
        workflow_ref = self.workflows_collection.document(workflow_id)
        workflow_doc = workflow_ref.get()
        
        if workflow_doc.exists:
            return WorkflowDefinition(**workflow_doc.to_dict())
        return None
        
    async def list_workflows(self, active_only: bool = True) -> List[WorkflowDefinition]:
        """List workflow definitions from Firestore."""
        query = self.workflows_collection
        if active_only:
            query = query.where('is_active', '==', True)
            
        workflows = []
        for doc in query.stream():
            workflows.append(WorkflowDefinition(**doc.to_dict()))
        return workflows
        
    async def save_execution(self, execution: WorkflowExecution) -> str:
        """Save workflow execution state to Firestore."""
        execution_ref = self.executions_collection.document(execution.id)
        execution_ref.set(execution.dict())
        return execution.id
        
    async def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Retrieve workflow execution state from Firestore."""
        execution_ref = self.executions_collection.document(execution_id)
        execution_doc = execution_ref.get()
        
        if execution_doc.exists:
            return WorkflowExecution(**execution_doc.to_dict())
        return None
        
    async def list_executions(self, workflow_id: Optional[str] = None, status: Optional[str] = None) -> List[WorkflowExecution]:
        """List workflow executions from Firestore."""
        query = self.executions_collection
        
        if workflow_id:
            query = query.where('workflow_id', '==', workflow_id)
        if status:
            query = query.where('status', '==', status)
            
        executions = []
        for doc in query.stream():
            executions.append(WorkflowExecution(**doc.to_dict()))
        return executions
        
    async def update_execution_status(self, execution_id: str, status: str, result: Optional[Dict[str, Any]] = None, error: Optional[str] = None):
        """Update workflow execution status."""
        execution_ref = self.executions_collection.document(execution_id)
        update_data = {
            'status': status,
            'completed_at': datetime.utcnow()
        }
        
        if result is not None:
            update_data['result'] = result
        if error is not None:
            update_data['error'] = error
            
        execution_ref.update(update_data)
