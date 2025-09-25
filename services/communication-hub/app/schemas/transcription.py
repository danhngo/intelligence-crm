"""Transcription schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TranscriptionBase(BaseModel):
    """Base transcription schema."""
    
    message_id: UUID
    audio_url: str
    source_lang: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TranscriptionCreate(TranscriptionBase):
    """Schema for creating a transcription."""
    pass


class TranscriptionUpdate(BaseModel):
    """Schema for updating a transcription."""
    
    text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class TranscriptionSegment(BaseModel):
    """Schema for transcription segment."""
    
    start_time: float
    end_time: float
    text: str
    confidence: float
    speaker: Optional[str] = None


class Transcription(TranscriptionBase):
    """Schema for transcription response."""
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    text: str
    confidence: float
    detected_language: Optional[str] = None
    segments: List[TranscriptionSegment] = Field(default_factory=list)
    word_timings: Optional[Dict[str, List[float]]] = None
    alternatives: List[Dict[str, Any]] = Field(default_factory=list)

    class Config:
        """Pydantic config."""
        from_attributes = True
