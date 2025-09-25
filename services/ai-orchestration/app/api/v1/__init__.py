"""API Router for AI Orchestration Service."""

from fastapi import APIRouter
from . import insights, workflows, agents

# Create API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(
    insights.router,
    prefix="/insights",
    tags=["insights"]
)

api_router.include_router(
    workflows.router,
    prefix="/workflows", 
    tags=["workflows"]
)

api_router.include_router(
    agents.router,
    prefix="/agents",
    tags=["agents"]
)
