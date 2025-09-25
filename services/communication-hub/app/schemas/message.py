"""Message and conversation schemas."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.models.message import (
    ChannelType,
    ConversationStatus,
    Direction,
    MessageStatus,
    MessageType,
    Priority,
    RecipientType,
    ResolutionStatus,
    SenderType,
)


class MessageContent(BaseModel):
    """Message content schema."""
    
    text: str
    html: Optional[str] = None
    attachments: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MessageParty(BaseModel):
    """Message party (sender/recipient) schema."""
    
    id: str
    type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MessageSentiment(BaseModel):
    """Message sentiment schema."""
    
    score: float = Field(ge=-1, le=1)
    confidence: float = Field(ge=0, le=1)
    labels: List[str] = Field(default_factory=list)


class MessageIntent(BaseModel):
    """Message intent schema."""
    
    name: str
    confidence: float = Field(ge=0, le=1)
    entities: Dict[str, Any] = Field(default_factory=dict)


class MessageBase(BaseModel):
    """Base message schema."""
    
    conversation_id: uuid.UUID
    channel_id: uuid.UUID
    type: MessageType
    direction: Direction
    content: MessageContent
    sender: MessageParty
    recipient: MessageParty
    status: MessageStatus = MessageStatus.PENDING
    priority: Priority = Priority.MEDIUM
    tags: List[str] = Field(default_factory=list)
    sentiment: Optional[MessageSentiment] = None
    intent: Optional[MessageIntent] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MessageCreate(MessageBase):
    """Schema for creating a message."""
    pass


class MessageUpdate(BaseModel):
    """Schema for updating a message."""
    
    status: Optional[MessageStatus] = None
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class Message(MessageBase):
    """Schema for message response."""
    
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class ConversationMetrics(BaseModel):
    """Conversation metrics schema."""
    
    message_count: int = 0
    response_time: float = 0
    resolution: Optional[Dict[str, Any]] = None


class ConversationBase(BaseModel):
    """Base conversation schema."""
    
    channel_id: uuid.UUID
    participants: List[str] = Field(default_factory=list)
    status: ConversationStatus = ConversationStatus.ACTIVE
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ConversationCreate(ConversationBase):
    """Schema for creating a conversation."""
    pass


class ConversationUpdate(BaseModel):
    """Schema for updating a conversation."""
    
    participants: Optional[List[str]] = None
    status: Optional[ConversationStatus] = None
    metadata: Optional[Dict[str, Any]] = None


class Conversation(ConversationBase):
    """Schema for conversation response."""
    
    id: uuid.UUID
    message_count: int
    avg_response_time: Optional[float] = None
    resolution_status: Optional[ResolutionStatus] = None
    resolution_time: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = Field(default_factory=list)

    class Config:
        """Pydantic config."""
        from_attributes = True


# WebSocket schemas
class WSMessageSend(BaseModel):
    """Schema for sending message through WebSocket."""
    
    content: str
    conversation_id: uuid.UUID


class WSTypingIndicator(BaseModel):
    """Schema for typing indicator through WebSocket."""
    
    conversation_id: uuid.UUID
    is_typing: bool


class WSPresenceUpdate(BaseModel):
    """Schema for presence update through WebSocket."""
    
    status: str
