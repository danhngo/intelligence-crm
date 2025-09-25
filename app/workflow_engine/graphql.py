"""
GraphQL schema and resolvers for workflow management.
"""

import strawberry
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from . import WorkflowDefinition, WorkflowExecution, WorkflowTrigger
from .storage import WorkflowStorage

# Initialize storage
workflow_storage = WorkflowStorage(project_id="your-project-id")

@strawberry.type
class WorkflowStep:
    id: str
    name: str
    type: str
    config: str
    next_steps: List[str]

@strawberry.type
class Workflow:
    id: UUID
    name: str
    description: Optional[str]
    version: int
    is_active: bool
    trigger: str
    steps: List[WorkflowStep]
    variables: str
    owner: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    last_executed: Optional[datetime]
    execution_stats: str

@strawberry.type
class WorkflowExecutionStatus:
    id: UUID
    workflow_id: UUID
    status: str
    current_step: Optional[str]
    variables: str
    result: Optional[str]
    error: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]

@strawberry.input
class WorkflowInput:
    name: str
    description: Optional[str]
    trigger: str
    steps: List[str]
    variables: str
    owner: str
    tags: List[str]

@strawberry.type
class Query:
    @strawberry.field
    async def workflow(self, id: UUID) -> Optional[Workflow]:
        """Get a specific workflow by ID."""
        workflow = await workflow_storage.get_workflow(str(id))
        return Workflow(**workflow.dict()) if workflow else None

    @strawberry.field
    async def workflows(
        self,
        active_only: bool = True,
        limit: int = 50
    ) -> List[Workflow]:
        """List workflows with optional filtering."""
        workflows = await workflow_storage.list_workflows(active_only=active_only)
        return [Workflow(**w.dict()) for w in workflows[:limit]]

    @strawberry.field
    async def workflow_execution(self, id: UUID) -> Optional[WorkflowExecutionStatus]:
        """Get a specific workflow execution by ID."""
        execution = await workflow_storage.get_execution(str(id))
        return WorkflowExecutionStatus(**execution.dict()) if execution else None

    @strawberry.field
    async def workflow_executions(
        self,
        workflow_id: Optional[UUID] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[WorkflowExecutionStatus]:
        """List workflow executions with optional filtering."""
        executions = await workflow_storage.list_executions(
            workflow_id=str(workflow_id) if workflow_id else None,
            status=status
        )
        return [WorkflowExecutionStatus(**e.dict()) for e in executions[:limit]]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_workflow(self, input: WorkflowInput) -> Workflow:
        """Create a new workflow."""
        workflow = WorkflowDefinition(
            name=input.name,
            description=input.description,
            trigger=input.trigger,
            steps=input.steps,
            variables=input.variables,
            owner=input.owner,
            tags=input.tags
        )
        await workflow_storage.save_workflow(workflow)
        return Workflow(**workflow.dict())

    @strawberry.mutation
    async def update_workflow(self, id: UUID, input: WorkflowInput) -> Workflow:
        """Update an existing workflow."""
        existing = await workflow_storage.get_workflow(str(id))
        if not existing:
            raise ValueError("Workflow not found")

        workflow = WorkflowDefinition(
            id=str(id),
            name=input.name,
            description=input.description,
            trigger=input.trigger,
            steps=input.steps,
            variables=input.variables,
            owner=input.owner,
            tags=input.tags,
            version=existing.version + 1
        )
        await workflow_storage.save_workflow(workflow)
        return Workflow(**workflow.dict())

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def workflow_status(self, execution_id: UUID) -> WorkflowExecutionStatus:
        """Subscribe to workflow execution status updates."""
        async for execution in workflow_storage.watch_execution(str(execution_id)):
            yield WorkflowExecutionStatus(**execution.dict())

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)
