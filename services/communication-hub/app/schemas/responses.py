"""API response schemas."""

from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Error detail schema."""
    
    code: str
    message: str
    target: Optional[str] = None
    details: Optional[List["ErrorDetail"]] = None


class Error(BaseModel):
    """API error schema."""
    
    code: str
    message: str
    target: Optional[str] = None
    details: List[ErrorDetail] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None


class PaginationMetadata(BaseModel):
    """Pagination metadata schema."""
    
    total: int
    page: int
    per_page: int
    pages: int


class PaginatedResponse(GenericModel, Generic[T]):
    """Generic paginated response schema."""
    
    data: List[T]
    metadata: PaginationMetadata


class SuccessResponse(GenericModel, Generic[T]):
    """Generic success response schema."""
    
    data: T
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BatchOperationResult(BaseModel):
    """Batch operation result schema."""
    
    success_count: int
    error_count: int
    failed_ids: List[UUID] = Field(default_factory=list)
    errors: Dict[UUID, Error] = Field(default_factory=dict)
