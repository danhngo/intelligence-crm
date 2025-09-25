"""Workflow Executor

This module implements the core workflow execution engine using LangChain for
orchestrating AI workflows with error handling, monitoring and optimization.
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import UUID

from langchain.llms import BaseLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks import BaseCallbackHandler
from pydantic import BaseModel

from app.core.config import settings
from app.models.workflow import WorkflowContext, WorkflowResult
from .prompts import PromptManager
from .memory import MemoryManager
from .tools import ToolRegistry


class WorkflowExecutor:
    """Core workflow execution engine."""
    
    def __init__(
        self,
        llm: BaseLLM,
        prompt_manager: PromptManager,
        memory_manager: MemoryManager,
        tool_registry: ToolRegistry,
        callbacks: Optional[List[BaseCallbackHandler]] = None
    ):
        """Initialize workflow executor with dependencies.
        
        Args:
            llm: Base language model to use
            prompt_manager: Manages prompt templates and versions
            memory_manager: Handles conversation memory and context
            tool_registry: Available tool integrations
            callbacks: Optional callback handlers for monitoring
        """
        self.llm = llm
        self.prompt_manager = prompt_manager
        self.memory_manager = memory_manager
        self.tool_registry = tool_registry
        self.callbacks = callbacks or []
        
    async def execute_workflow(
        self,
        workflow_id: UUID,
        context: WorkflowContext,
        **kwargs: Any
    ) -> WorkflowResult:
        """Execute a workflow with the given context.
        
        Args:
            workflow_id: Unique workflow identifier
            context: Workflow execution context
            **kwargs: Additional workflow parameters
            
        Returns:
            WorkflowResult containing execution outputs and metrics
            
        Raises:
            WorkflowExecutionError: If workflow execution fails
        """
        # Initialize workflow execution
        start_time = datetime.utcnow()
        
        try:
            # Load workflow memory and context
            memory = await self.memory_manager.get_memory(workflow_id)
            
            # Get workflow prompt template
            prompt = self.prompt_manager.get_prompt(workflow_id)
            
            # Create LangChain for workflow
            chain = LLMChain(
                llm=self.llm,
                prompt=prompt,
                memory=memory,
                callbacks=self.callbacks
            )
            
            # Execute workflow steps
            result = await chain.arun(
                context=context.dict(),
                **kwargs
            )
            
            # Record metrics and return result
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            return WorkflowResult(
                workflow_id=workflow_id,
                output=result,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                success=True
            )
            
        except Exception as e:
            # Handle workflow execution errors
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            return WorkflowResult(
                workflow_id=workflow_id,
                error=str(e),
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                success=False
            )
