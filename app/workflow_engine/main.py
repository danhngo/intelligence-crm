"""
Main FastAPI application for the Workflow Engine Service.
"""

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

from .api import router as rest_router
from .graphql import schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    print("Starting up Workflow Engine Service...")
    yield
    # Shutdown
    print("Shutting down Workflow Engine Service...")

# Create FastAPI app
app = FastAPI(
    title="Workflow Engine Service",
    description="Intelligent automation using LangGraph for complex decision trees and workflow orchestration",
    version="1.0.0",
    lifespan=lifespan
)

# Add REST API router
app.include_router(rest_router)

# Add GraphQL endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
