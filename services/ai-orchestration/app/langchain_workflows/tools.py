"""LangChain Tool Integrations

This module implements LangChain tools for CRM data access, communication
and analytics integrations.
"""

from typing import Dict, List, Optional
from uuid import UUID

from langchain.tools import BaseTool
from pydantic import BaseModel

from app.core.config import settings
from app.services.crm import CRMService
from app.services.communication import CommunicationService
from app.services.analytics import AnalyticsService


class ToolRegistry:
    """Registry of available LangChain tools."""
    
    def __init__(
        self,
        crm_service: CRMService,
        communication_service: CommunicationService,
        analytics_service: AnalyticsService
    ):
        """Initialize tool registry with service dependencies.
        
        Args:
            crm_service: CRM data access service
            communication_service: Communication service
            analytics_service: Analytics service
        """
        self.crm_service = crm_service
        self.communication_service = communication_service
        self.analytics_service = analytics_service
        
        # Initialize tools
        self.tools = self._create_tools()
        
    def _create_tools(self) -> List[BaseTool]:
        """Create list of available tools.
        
        Returns:
            List of LangChain tool instances
        """
        tools = []
        
        # CRM Data Tools
        tools.extend([
            self._create_contact_tool(),
            self._create_lead_tool(),
            self._create_interaction_tool()
        ])
        
        # Communication Tools  
        tools.extend([
            self._create_email_tool(),
            self._create_sms_tool()
        ])
        
        # Analytics Tools
        tools.extend([
            self._create_insight_tool(),
            self._create_report_tool()
        ])
        
        return tools
        
    def get_tools(self) -> List[BaseTool]:
        """Get list of all available tools.
        
        Returns:
            List of tool instances
        """
        return self.tools.copy()
        
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Get specific tool by name.
        
        Args:
            tool_name: Name of tool to get
            
        Returns:
            Tool instance if found, else None
        """
        return next(
            (tool for tool in self.tools if tool.name == tool_name),
            None
        )
        
    def _create_contact_tool(self) -> BaseTool:
        """Create tool for contact operations."""
        return BaseTool(
            name="contact_tool",
            description="Look up or modify contact information",
            func=self.crm_service.handle_contact_operation
        )
        
    def _create_lead_tool(self) -> BaseTool:
        """Create tool for lead operations."""
        return BaseTool(
            name="lead_tool", 
            description="Qualify and update lead information",
            func=self.crm_service.handle_lead_operation
        )
        
    def _create_interaction_tool(self) -> BaseTool:
        """Create tool for interaction tracking."""
        return BaseTool(
            name="interaction_tool",
            description="Record customer interactions and activities",
            func=self.crm_service.handle_interaction_operation
        )
        
    def _create_email_tool(self) -> BaseTool:
        """Create tool for email operations."""
        return BaseTool(
            name="email_tool",
            description="Send and track email communications",
            func=self.communication_service.handle_email_operation
        )
        
    def _create_sms_tool(self) -> BaseTool:
        """Create tool for SMS operations."""
        return BaseTool(
            name="sms_tool",
            description="Send and track SMS communications",
            func=self.communication_service.handle_sms_operation
        )
        
    def _create_insight_tool(self) -> BaseTool:
        """Create tool for generating insights."""
        return BaseTool(
            name="insight_tool",
            description="Generate customer insights and recommendations",
            func=self.analytics_service.generate_insights
        )
        
    def _create_report_tool(self) -> BaseTool:
        """Create tool for generating reports."""
        return BaseTool(
            name="report_tool",
            description="Generate analytics reports and visualizations",
            func=self.analytics_service.generate_report
        )
