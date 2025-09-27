"""AI Models API endpoints for model management and deployment."""

from typing import List, Optional, Dict, Any, Union
from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()


class ModelConfig(BaseModel):
    """Model configuration schema."""
    algorithm: str = Field(..., description="ML algorithm type")
    hyperparameters: Dict[str, Any] = Field(default_factory=dict, description="Model hyperparameters")
    features: Optional[List[str]] = Field(default=None, description="Feature names")


class InputSchema(BaseModel):
    """Model input schema definition."""
    type: str = Field(default="object", description="Schema type")
    properties: Dict[str, Dict[str, str]] = Field(..., description="Schema properties")
    required: List[str] = Field(default_factory=list, description="Required fields")


class ModelCreate(BaseModel):
    """Model creation request."""
    name: str = Field(..., description="Model name")
    description: Optional[str] = Field(None, description="Model description")
    type: str = Field(..., description="Model type (classification, regression, etc.)")
    framework: str = Field(..., description="ML framework (scikit-learn, tensorflow, etc.)")
    version: str = Field(..., description="Model version")
    model_configuration: ModelConfig = Field(..., description="Model configuration")
    input_schema: InputSchema = Field(..., description="Input schema definition")


class ModelResponse(BaseModel):
    """Model response schema."""
    id: str = Field(..., description="Model ID")
    name: str = Field(..., description="Model name")
    description: Optional[str] = Field(None, description="Model description")
    type: str = Field(..., description="Model type")
    framework: str = Field(..., description="ML framework")
    version: str = Field(..., description="Model version")
    status: str = Field(..., description="Model status (deployed, training, etc.)")
    model_configuration: ModelConfig = Field(..., description="Model configuration")
    input_schema: InputSchema = Field(..., description="Input schema")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    accuracy: Optional[float] = Field(None, description="Model accuracy score")
    deployment_url: Optional[str] = Field(None, description="Model deployment endpoint")


class PredictionRequest(BaseModel):
    """Prediction request schema."""
    inputs: Dict[str, Union[str, int, float, bool]] = Field(..., description="Input data for prediction")
    options: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Prediction options")


class PredictionResponse(BaseModel):
    """Prediction response schema."""
    prediction: Union[str, int, float, Dict[str, Any]] = Field(..., description="Model prediction")
    confidence: Optional[float] = Field(None, description="Prediction confidence score")
    explanation: Optional[Dict[str, Any]] = Field(None, description="Prediction explanation")
    model_id: str = Field(..., description="Model ID used for prediction")
    timestamp: datetime = Field(..., description="Prediction timestamp")


# Mock database for models (in production, this would be a real database)
_models_db: Dict[str, Dict[str, Any]] = {}


@router.get("/", response_model=List[ModelResponse])
async def list_models(
    skip: int = 0,
    limit: int = 20,
    model_type: Optional[str] = None,
    status: Optional[str] = None
):
    """List available AI models."""
    models = list(_models_db.values())
    
    # Apply filters
    if model_type:
        models = [m for m in models if m.get("type") == model_type]
    if status:
        models = [m for m in models if m.get("status") == status]
    
    # Apply pagination
    models = models[skip:skip + limit]
    
    return [ModelResponse(**model) for model in models]


@router.post("/", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def deploy_model(model: ModelCreate):
    """Deploy a new AI model."""
    model_id = str(uuid4())
    now = datetime.utcnow()
    
    model_data = {
        "id": model_id,
        "name": model.name,
        "description": model.description,
        "type": model.type,
        "framework": model.framework,
        "version": model.version,
        "status": "deployed",
        "model_configuration": model.model_configuration.dict(),
        "input_schema": model.input_schema.dict(),
        "created_at": now,
        "updated_at": now,
        "accuracy": 0.85,  # Mock accuracy
        "deployment_url": f"/api/v1/models/{model_id}/predict"
    }
    
    _models_db[model_id] = model_data
    
    return ModelResponse(**model_data)


@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(model_id: str):
    """Get details of a specific model."""
    if model_id not in _models_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with id {model_id} not found"
        )
    
    return ModelResponse(**_models_db[model_id])


@router.put("/{model_id}", response_model=ModelResponse)
async def update_model(model_id: str, model: ModelCreate):
    """Update an existing model."""
    if model_id not in _models_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with id {model_id} not found"
        )
    
    existing_model = _models_db[model_id]
    updated_model = {
        **existing_model,
        "name": model.name,
        "description": model.description,
        "type": model.type,
        "framework": model.framework,
        "version": model.version,
        "model_configuration": model.model_configuration.dict(),
        "input_schema": model.input_schema.dict(),
        "updated_at": datetime.utcnow()
    }
    
    _models_db[model_id] = updated_model
    
    return ModelResponse(**updated_model)


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(model_id: str):
    """Delete a model."""
    if model_id not in _models_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with id {model_id} not found"
        )
    
    del _models_db[model_id]


@router.post("/{model_id}/predict", response_model=PredictionResponse)
async def predict_with_model(model_id: str, request: PredictionRequest):
    """Make a prediction using a specific model."""
    if model_id not in _models_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with id {model_id} not found"
        )
    
    model = _models_db[model_id]
    
    if model["status"] != "deployed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Model {model_id} is not deployed (status: {model['status']})"
        )
    
    # Mock prediction logic based on model type
    if model["type"] == "classification":
        if "lead_scoring" in model["name"].lower():
            # Lead scoring prediction
            engagement_score = request.inputs.get("engagement_score", 0.5)
            profile_score = request.inputs.get("profile_score", 0.5)
            interaction_frequency = request.inputs.get("interaction_frequency", 5)
            
            # Simple scoring formula
            score = (engagement_score * 0.4 + profile_score * 0.4 + (interaction_frequency / 20) * 0.2)
            prediction = "high" if score > 0.7 else "medium" if score > 0.4 else "low"
            
            response = PredictionResponse(
                prediction={
                    "category": prediction,
                    "score": round(score, 3),
                    "probability": round(score, 3)
                },
                confidence=round(score, 3),
                explanation={
                    "engagement_weight": 0.4,
                    "profile_weight": 0.4,
                    "interaction_weight": 0.2,
                    "factors": {
                        "engagement_score": engagement_score,
                        "profile_score": profile_score,
                        "interaction_frequency": interaction_frequency
                    }
                },
                model_id=model_id,
                timestamp=datetime.utcnow()
            )
        else:
            # Generic classification
            response = PredictionResponse(
                prediction="positive",
                confidence=0.85,
                explanation={"model_type": "classification", "algorithm": model["model_configuration"]["algorithm"]},
                model_id=model_id,
                timestamp=datetime.utcnow()
            )
    else:
        # Generic prediction for other types
        response = PredictionResponse(
            prediction=42.5,
            confidence=0.80,
            explanation={"model_type": model["type"], "algorithm": model["model_configuration"]["algorithm"]},
            model_id=model_id,
            timestamp=datetime.utcnow()
        )
    
    return response


@router.get("/{model_id}/metrics")
async def get_model_metrics(model_id: str):
    """Get performance metrics for a model."""
    if model_id not in _models_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with id {model_id} not found"
        )
    
    # Mock metrics
    return {
        "model_id": model_id,
        "accuracy": 0.85,
        "precision": 0.83,
        "recall": 0.87,
        "f1_score": 0.85,
        "predictions_count": 1523,
        "avg_prediction_time_ms": 45.2,
        "last_evaluation": datetime.utcnow().isoformat()
    }
