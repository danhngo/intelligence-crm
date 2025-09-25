"""
Workflow executor using LangGraph for orchestrating workflow execution.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio

from langchain.graphs import StateGraph
from langchain.schema import BaseMessage, SystemMessage, HumanMessage
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from . import WorkflowDefinition, WorkflowExecution

class WorkflowExecutor:
    """Executes workflows using LangGraph for orchestration."""
    
    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """Initialize workflow executor with optional LLM."""
        self.llm = llm or ChatOpenAI(temperature=0)
        
    async def execute_workflow(self, workflow: WorkflowDefinition, input_data: Dict[str, Any]) -> WorkflowExecution:
        """Execute a workflow using LangGraph."""
        # Create workflow execution instance
        execution = WorkflowExecution(workflow_id=workflow.id)
        
        try:
            # Initialize state graph
            workflow_graph = await self._build_state_graph(workflow)
            
            # Initialize execution variables
            variables = {
                **workflow.variables,
                **input_data,
                "execution_id": execution.id,
                "workflow_id": workflow.id,
                "start_time": datetime.utcnow().isoformat()
            }
            
            # Execute workflow graph
            execution.status = "RUNNING"
            result = await workflow_graph.arun(variables)
            
            # Update execution status
            execution.status = "COMPLETED"
            execution.result = result
            execution.completed_at = datetime.utcnow()
            
        except Exception as e:
            execution.status = "FAILED"
            execution.error = str(e)
            execution.completed_at = datetime.utcnow()
            
        return execution
    
    async def _build_state_graph(self, workflow: WorkflowDefinition) -> StateGraph:
        """Build LangGraph state graph from workflow definition."""
        # Initialize state graph
        workflow_graph = StateGraph()
        
        # Add nodes for each step
        for step in workflow.steps:
            step_id = step["id"]
            step_type = step["type"]
            
            # Create step node
            workflow_graph.add_node(step_id, self._create_step_node(step))
            
            # Add edges based on next steps
            for next_step in step.get("next_steps", []):
                workflow_graph.add_edge(step_id, next_step)
        
        return workflow_graph
    
    def _create_step_node(self, step: Dict[str, Any]) -> Any:
        """Create appropriate node handler based on step type."""
        step_type = step["type"]
        step_config = step.get("config", {})
        
        if step_type == "AI_DECISION":
            # Create AI decision node
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=step_config.get("system_prompt", "")),
                MessagesPlaceholder(variable_name="history"),
                HumanMessage(content=step_config.get("human_prompt", ""))
            ])
            
            return {
                "prompt": prompt,
                "llm": self.llm,
                "input_variables": step_config.get("input_variables", [])
            }
            
        elif step_type == "SEND_EMAIL":
            # Create email sending node
            return {
                "template": step_config.get("template"),
                "recipients": step_config.get("recipients", []),
                "subject": step_config.get("subject")
            }
            
        # Add more step type handlers as needed
        
        return step_config
