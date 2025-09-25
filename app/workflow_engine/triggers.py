"""
Workflow trigger management for handling workflow execution triggers.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from enum import Enum

from pydantic import BaseModel, Field

class TriggerType(str, Enum):
    """Supported workflow trigger types."""
    CONTACT_CREATED = "CONTACT_CREATED"
    INTERACTION_LOGGED = "INTERACTION_LOGGED"
    LEAD_SCORE_CHANGED = "LEAD_SCORE_CHANGED"
    TIME_BASED = "TIME_BASED"
    MANUAL = "MANUAL"
    WEBHOOK = "WEBHOOK"

class TriggerCondition(BaseModel):
    """Condition that must be met for trigger to fire."""
    field: str
    operator: str  # equals, not_equals, greater_than, less_than, contains
    value: Any

class WorkflowTrigger(BaseModel):
    """Workflow trigger configuration."""
    type: TriggerType
    conditions: List[TriggerCondition] = Field(default_factory=list)
    schedule: Optional[str] = None  # Cron expression for time-based triggers

class TriggerManager:
    """Manages workflow triggers and trigger evaluation."""
    
    def __init__(self):
        """Initialize trigger manager."""
        self._triggers: Dict[str, List[WorkflowTrigger]] = {}
        self._event_handlers: Dict[TriggerType, List[callable]] = {}
        
    def register_trigger(self, workflow_id: str, trigger: WorkflowTrigger):
        """Register a new workflow trigger."""
        if workflow_id not in self._triggers:
            self._triggers[workflow_id] = []
        self._triggers[workflow_id].append(trigger)
        
    def register_event_handler(self, trigger_type: TriggerType, handler: callable):
        """Register event handler for trigger type."""
        if trigger_type not in self._event_handlers:
            self._event_handlers[trigger_type] = []
        self._event_handlers[trigger_type].append(handler)
        
    async def evaluate_event(self, trigger_type: TriggerType, event_data: Dict[str, Any]):
        """Evaluate an event against registered triggers."""
        matching_workflows = []
        
        # Find workflows with matching triggers
        for workflow_id, triggers in self._triggers.items():
            for trigger in triggers:
                if trigger.type == trigger_type:
                    # Check if conditions are met
                    if self._evaluate_conditions(trigger.conditions, event_data):
                        matching_workflows.append(workflow_id)
                        
        # Execute event handlers for matching workflows
        if trigger_type in self._event_handlers:
            for handler in self._event_handlers[trigger_type]:
                for workflow_id in matching_workflows:
                    await handler(workflow_id, event_data)
                    
    def _evaluate_conditions(self, conditions: List[TriggerCondition], event_data: Dict[str, Any]) -> bool:
        """Evaluate if all conditions are met for event data."""
        for condition in conditions:
            field_value = event_data.get(condition.field)
            
            if field_value is None:
                return False
                
            if condition.operator == "equals" and field_value != condition.value:
                return False
            elif condition.operator == "not_equals" and field_value == condition.value:
                return False
            elif condition.operator == "greater_than" and field_value <= condition.value:
                return False
            elif condition.operator == "less_than" and field_value >= condition.value:
                return False
            elif condition.operator == "contains" and condition.value not in field_value:
                return False
                
        return True
