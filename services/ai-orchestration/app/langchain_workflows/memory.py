"""Conversation Memory Manager

This module implements conversation memory management with Redis backend
and intelligent context window handling.
"""

from typing import Dict, List, Optional
from uuid import UUID

from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from pydantic import BaseModel

from app.core.config import settings


class MemoryManager:
    """Manages conversation memory with Redis backend."""
    
    def __init__(self, redis_url: Optional[str] = None):
        """Initialize memory manager.
        
        Args:
            redis_url: Optional Redis connection URL
        """
        self.redis_url = redis_url or settings.REDIS_URL
        
    async def get_memory(
        self,
        workflow_id: UUID,
        window_size: int = 10
    ) -> ConversationBufferMemory:
        """Get conversation memory for workflow.
        
        Args:
            workflow_id: Workflow to get memory for
            window_size: Max messages to keep in context
            
        Returns:
            ConversationBufferMemory instance
        """
        # Initialize Redis chat history
        history = RedisChatMessageHistory(
            url=self.redis_url,
            session_id=str(workflow_id),
            key_prefix="memory:"
        )
        
        # Create memory with history
        return ConversationBufferMemory(
            chat_memory=history,
            memory_key="chat_history",
            return_messages=True,
            max_token_limit=window_size * 1000  # Approximate token limit
        )
        
    async def clear_memory(self, workflow_id: UUID) -> None:
        """Clear conversation memory for workflow.
        
        Args:
            workflow_id: Workflow to clear memory for
        """
        history = RedisChatMessageHistory(
            url=self.redis_url,
            session_id=str(workflow_id),
            key_prefix="memory:"
        )
        await history.clear()
