"""Prompt Template Manager

This module manages versioned prompt templates with A/B testing capabilities
and tenant customization support.
"""

from typing import Dict, Optional
from uuid import UUID

from langchain.prompts import PromptTemplate
from pydantic import BaseModel

from app.core.config import settings


class PromptVersion(BaseModel):
    """Prompt template version with metadata."""
    
    version: str
    template: str
    description: Optional[str] = None
    is_active: bool = True
    parameters: Dict[str, str] = {}


class PromptManager:
    """Manages versioned prompt templates with A/B testing."""
    
    def __init__(self):
        """Initialize prompt template storage."""
        self.templates: Dict[UUID, Dict[str, PromptVersion]] = {}
        
    def register_prompt(
        self,
        workflow_id: UUID,
        version: str,
        template: str,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, str]] = None
    ) -> PromptTemplate:
        """Register a new prompt template version.
        
        Args:
            workflow_id: Workflow the prompt is for
            version: Version identifier 
            template: Prompt template string
            description: Optional template description
            parameters: Optional parameter descriptions
            
        Returns:
            Created PromptTemplate instance
        """
        if workflow_id not in self.templates:
            self.templates[workflow_id] = {}
            
        prompt_version = PromptVersion(
            version=version,
            template=template,
            description=description,
            parameters=parameters or {}
        )
        
        self.templates[workflow_id][version] = prompt_version
        
        return PromptTemplate(
            template=template,
            input_variables=list(prompt_version.parameters.keys())
        )
        
    def get_prompt(
        self,
        workflow_id: UUID,
        version: Optional[str] = None
    ) -> PromptTemplate:
        """Get prompt template for workflow.
        
        Args:
            workflow_id: Workflow to get prompt for
            version: Optional specific version to get
            
        Returns:
            PromptTemplate instance
            
        Raises:
            KeyError: If workflow or version not found
        """
        if workflow_id not in self.templates:
            raise KeyError(f"No prompts registered for workflow {workflow_id}")
            
        templates = self.templates[workflow_id]
        
        if not templates:
            raise KeyError(f"No prompt versions for workflow {workflow_id}")
            
        if version:
            if version not in templates:
                raise KeyError(f"Version {version} not found")
            prompt_version = templates[version]
        else:
            # Get latest active version
            prompt_version = max(
                (v for v in templates.values() if v.is_active),
                key=lambda v: v.version
            )
            
        return PromptTemplate(
            template=prompt_version.template,
            input_variables=list(prompt_version.parameters.keys())
        )
