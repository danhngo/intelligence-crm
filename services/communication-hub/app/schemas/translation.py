"""Translation schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TranslationBase(BaseModel):
    """Base translation schema."""
    
    message_id: UUID
    source_lang: str
    target_lang: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TranslationCreate(TranslationBase):
    """Schema for creating a translation."""
    pass


class TranslationUpdate(BaseModel):
    """Schema for updating a translation."""
    
    text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Translation(TranslationBase):
    """Schema for translation response."""
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    confidence: float
    translated_text: str
    detected_source_lang: Optional[str] = None
    alternatives: List[Dict[str, Any]] = Field(default_factory=list)

    class Config:
        """Pydantic config."""
        from_attributes = True
