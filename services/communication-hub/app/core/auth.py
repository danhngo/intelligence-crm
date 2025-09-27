"""Authentication utilities."""

from typing import Any, Dict
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get current authenticated user."""
    # TODO: Implement JWT token validation
    # This would validate the JWT token and return user info
    
    # For now, return mock user
    return {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "tenant_id": "550e8400-e29b-41d4-a716-446655440001"
    }


async def get_tenant_id(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> UUID:
    """Get tenant ID from current user."""
    return UUID(current_user["tenant_id"])


async def verify_admin_role(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Verify user has admin role."""
    # TODO: Check user roles
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
