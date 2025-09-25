"""Init file for API package."""

from app.api.analytics import router as analytics_router

__all__ = [
    "analytics_router",
]
