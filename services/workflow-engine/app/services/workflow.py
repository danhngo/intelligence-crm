"""Workflow execution service."""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Any, Optional

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.workflow import (
    ExecutionStatus,
    StepType,
    Workflow,
    WorkflowExecution,
    WorkflowLog
)


class WorkflowExecutionService:
    """Service for executing workflows."""
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize service."""
        self.session = session
        
    async def execute_workflow(
        self,
        workflow: Workflow,
        input_data: dict[str, Any],
        tenant_id: uuid.UUID
    ) -> WorkflowExecution:
        """Execute a workflow with given input data."""
        # Create execution record
        execution = WorkflowExecution(
            workflow_id=workflow.id,
            tenant_id=tenant_id,
            input_data=input_data,
            start_time=datetime.utcnow()
        )
        self.session.add(execution)
        await self.session.commit()
        
        try:
            # Execute workflow steps
            output_data = await self._execute_steps(workflow, execution, input_data)
            
            # Update execution record with success
            execution.status = ExecutionStatus.COMPLETED
            execution.output_data = output_data
            execution.end_time = datetime.utcnow()
            
        except Exception as e:
            # Update execution record with failure
            execution.status = ExecutionStatus.FAILED
            execution.error_data = {
                "error": str(e),
                "step": execution.current_step
            }
            execution.end_time = datetime.utcnow()
            
            # Log error
            await self._log_step(
                execution.id,
                execution.current_step or 0,
                StepType.FUNCTION,
                f"Error executing step: {str(e)}",
                {"error": str(e)},
                tenant_id
            )
            
        await self.session.commit()
        return execution
    
    async def _execute_steps(
        self,
        workflow: Workflow,
        execution: WorkflowExecution,
        input_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute workflow steps sequentially."""
        context = {
            "input": input_data,
            "output": {},
            "vars": {}
        }
        
        for i, step in enumerate(workflow.steps):
            execution.current_step = i
            await self.session.commit()
            
            step_type = StepType(step["type"])
            
            try:
                if step_type == StepType.HTTP_REQUEST:
                    result = await self._execute_http_request(step, context)
                elif step_type == StepType.CONDITION:
                    result = await self._execute_condition(step, context)
                elif step_type == StepType.EMAIL:
                    result = await self._execute_email(step, context)
                elif step_type == StepType.DELAY:
                    result = await self._execute_delay(step)
                elif step_type == StepType.FUNCTION:
                    result = await self._execute_function(step, context)
                else:
                    raise ValueError(f"Unsupported step type: {step_type}")
                
                # Update context with step result
                if "output_key" in step:
                    context["vars"][step["output_key"]] = result
                
                # Log successful step execution
                await self._log_step(
                    execution.id,
                    i,
                    step_type,
                    f"Successfully executed {step_type} step",
                    {"result": result},
                    workflow.tenant_id
                )
                
            except Exception as e:
                # Log failed step execution
                await self._log_step(
                    execution.id,
                    i,
                    step_type,
                    f"Failed to execute {step_type} step",
                    {"error": str(e)},
                    workflow.tenant_id
                )
                raise
        
        return context["vars"]
    
    async def _execute_http_request(
        self,
        step: dict[str, Any],
        context: dict[str, Any]
    ) -> Any:
        """Execute HTTP request step."""
        async with httpx.AsyncClient() as client:
            # Prepare request
            method = step["method"]
            url = self._interpolate(step["url"], context)
            headers = {
                k: self._interpolate(v, context)
                for k, v in step.get("headers", {}).items()
            }
            
            # Handle body
            body = None
            if "body" in step:
                body = json.loads(self._interpolate(
                    json.dumps(step["body"]),
                    context
                ))
            
            # Make request
            response = await client.request(
                method,
                url,
                headers=headers,
                json=body,
                timeout=step.get("timeout", 30)
            )
            response.raise_for_status()
            
            return response.json()
    
    async def _execute_condition(
        self,
        step: dict[str, Any],
        context: dict[str, Any]
    ) -> bool:
        """Execute condition step."""
        condition = step["condition"]
        if condition["type"] == "comparison":
            left = self._get_value(condition["left"], context)
            right = self._get_value(condition["right"], context)
            operator = condition["operator"]
            
            if operator == "eq":
                return left == right
            elif operator == "neq":
                return left != right
            elif operator == "gt":
                return left > right
            elif operator == "gte":
                return left >= right
            elif operator == "lt":
                return left < right
            elif operator == "lte":
                return left <= right
            else:
                raise ValueError(f"Unsupported operator: {operator}")
        else:
            raise ValueError(f"Unsupported condition type: {condition['type']}")
    
    async def _execute_email(
        self,
        step: dict[str, Any],
        context: dict[str, Any]
    ) -> bool:
        """Execute email step."""
        # TODO: Implement email sending logic
        # This is a placeholder that simulates email sending
        await asyncio.sleep(1)
        return True
    
    async def _execute_delay(self, step: dict[str, Any]) -> None:
        """Execute delay step."""
        seconds = step["seconds"]
        if not isinstance(seconds, (int, float)) or seconds < 0:
            raise ValueError("Delay must be a non-negative number")
        await asyncio.sleep(seconds)
    
    async def _execute_function(
        self,
        step: dict[str, Any],
        context: dict[str, Any]
    ) -> Any:
        """Execute function step."""
        function_type = step["function"]
        
        if function_type == "transform":
            # Handle data transformation
            template = step["template"]
            return self._interpolate(json.dumps(template), context)
        else:
            raise ValueError(f"Unsupported function type: {function_type}")
    
    async def _log_step(
        self,
        execution_id: uuid.UUID,
        step: int,
        step_type: StepType,
        message: str,
        details: Optional[dict[str, Any]],
        tenant_id: uuid.UUID
    ) -> None:
        """Log a workflow step execution."""
        log = WorkflowLog(
            execution_id=execution_id,
            step=step,
            step_type=step_type,
            message=message,
            details=details,
            tenant_id=tenant_id
        )
        self.session.add(log)
        await self.session.commit()
    
    def _interpolate(self, template: str, context: dict[str, Any]) -> str:
        """Interpolate variables in a template string."""
        # Simple variable substitution using format strings
        # For production, consider using a proper template engine
        result = template
        
        # Replace input variables
        for key, value in context["input"].items():
            result = result.replace(f"{{{{ input.{key} }}}}", str(value))
        
        # Replace output variables
        for key, value in context["vars"].items():
            result = result.replace(f"{{{{ vars.{key} }}}}", str(value))
        
        return result
    
    def _get_value(
        self,
        value_def: dict[str, Any],
        context: dict[str, Any]
    ) -> Any:
        """Get a value from the context or a literal."""
        if value_def["type"] == "variable":
            path = value_def["path"].split(".")
            current = context
            for part in path:
                current = current[part]
            return current
        elif value_def["type"] == "literal":
            return value_def["value"]
        else:
            raise ValueError(f"Unsupported value type: {value_def['type']}")
