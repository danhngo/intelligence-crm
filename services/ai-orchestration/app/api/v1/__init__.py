"""API Router for AI Orchestration Service."""

from fastapi import APIRouter
from . import insights, workflows, agents, models, predictions, training

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

api_router.include_router(
    models.router,
    prefix="/models",
    tags=["models"]
)

api_router.include_router(
    predictions.router,
    prefix="/predictions",
    tags=["predictions"]
)

api_router.include_router(
    training.router,
    prefix="/training",
    tags=["training"]
)
