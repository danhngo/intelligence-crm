"""Training API endpoints for model training and retraining jobs."""

from typing import List, Optional, Dict, Any, Union
from uuid import uuid4
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field
import asyncio

router = APIRouter()


class TrainingDataSource(BaseModel):
    """Training data source configuration."""
    source: str = Field(..., description="Data source type (database, file, api)")
    connection_string: Optional[str] = Field(None, description="Database connection string")
    query: Optional[str] = Field(None, description="SQL query for data extraction")
    file_path: Optional[str] = Field(None, description="Path to training data file")
    api_endpoint: Optional[str] = Field(None, description="API endpoint for data")
    target_column: str = Field(..., description="Target column name for supervised learning")


class ValidationConfig(BaseModel):
    """Model validation configuration."""
    method: str = Field(..., description="Validation method (cross_validation, holdout, etc.)")
    test_size: Optional[float] = Field(0.2, description="Test set size (0.0-1.0)")
    folds: Optional[int] = Field(5, description="Number of folds for cross-validation")
    stratify: Optional[bool] = Field(True, description="Whether to stratify splits")


class TrainingJobRequest(BaseModel):
    """Training job creation request."""
    model_name: str = Field(..., description="Name for the trained model")
    description: Optional[str] = Field(None, description="Training job description")
    algorithm: str = Field(..., description="ML algorithm to use")
    hyperparameters: Dict[str, Any] = Field(default_factory=dict, description="Algorithm hyperparameters")
    training_data: TrainingDataSource = Field(..., description="Training data configuration")
    validation: ValidationConfig = Field(..., description="Validation configuration")
    auto_deploy: bool = Field(default=False, description="Auto-deploy model if training succeeds")
    tags: Optional[List[str]] = Field(default_factory=list, description="Training job tags")


class TrainingMetrics(BaseModel):
    """Training metrics and evaluation results."""
    accuracy: Optional[float] = Field(None, description="Model accuracy")
    precision: Optional[float] = Field(None, description="Model precision")
    recall: Optional[float] = Field(None, description="Model recall")
    f1_score: Optional[float] = Field(None, description="F1 score")
    auc_roc: Optional[float] = Field(None, description="AUC-ROC score")
    loss: Optional[float] = Field(None, description="Training loss")
    val_loss: Optional[float] = Field(None, description="Validation loss")
    training_time_seconds: Optional[float] = Field(None, description="Training duration")
    epochs_completed: Optional[int] = Field(None, description="Number of epochs completed")


class TrainingJobResponse(BaseModel):
    """Training job response schema."""
    job_id: str = Field(..., description="Training job identifier")
    model_name: str = Field(..., description="Model name")
    description: Optional[str] = Field(None, description="Job description")
    algorithm: str = Field(..., description="ML algorithm")
    status: str = Field(..., description="Job status")
    progress: float = Field(default=0.0, description="Training progress percentage")
    metrics: Optional[TrainingMetrics] = Field(None, description="Training metrics")
    model_id: Optional[str] = Field(None, description="Generated model ID if successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime = Field(..., description="Job creation timestamp")
    started_at: Optional[datetime] = Field(None, description="Training start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Training completion timestamp")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")
    auto_deploy: bool = Field(..., description="Whether to auto-deploy after training")
    deployed: bool = Field(default=False, description="Whether model has been deployed")


class HyperparameterTuningRequest(BaseModel):
    """Hyperparameter tuning request."""
    model_name: str = Field(..., description="Base model name")
    algorithm: str = Field(..., description="ML algorithm")
    parameter_grid: Dict[str, List[Any]] = Field(..., description="Hyperparameter search grid")
    training_data: TrainingDataSource = Field(..., description="Training data configuration")
    validation: ValidationConfig = Field(..., description="Validation configuration")
    optimization_metric: str = Field(default="accuracy", description="Metric to optimize")
    max_trials: int = Field(default=20, description="Maximum number of trials")


# Mock database for training jobs
_training_jobs_db: Dict[str, Dict[str, Any]] = {}


async def simulate_training_job(job_id: str, algorithm: str, hyperparameters: Dict[str, Any]):
    """Simulate model training process."""
    job = _training_jobs_db[job_id]
    job["status"] = "running"
    job["started_at"] = datetime.utcnow()
    
    # Simulate training progress
    total_epochs = hyperparameters.get("n_estimators", hyperparameters.get("epochs", 100))
    
    for epoch in range(1, total_epochs + 1):
        # Simulate training time
        await asyncio.sleep(0.01)  # Fast simulation
        
        # Update progress
        progress = (epoch / total_epochs) * 100
        job["progress"] = progress
        
        # Simulate improving metrics
        base_accuracy = 0.6
        improvement = (epoch / total_epochs) * 0.25  # Up to 25% improvement
        noise = 0.02 * (1 - epoch / total_epochs)  # Decreasing noise
        
        current_accuracy = base_accuracy + improvement + (noise * (0.5 - abs(0.5 - (epoch % 10) / 10)))
        
        metrics = TrainingMetrics(
            accuracy=round(current_accuracy, 4),
            precision=round(current_accuracy * 0.98, 4),
            recall=round(current_accuracy * 1.02, 4),
            f1_score=round(current_accuracy, 4),
            loss=round((1 - current_accuracy) * 0.8, 4),
            val_loss=round((1 - current_accuracy) * 0.9, 4),
            training_time_seconds=epoch * 0.01,
            epochs_completed=epoch
        )
        
        job["metrics"] = metrics.dict()
        
        # Early stopping simulation
        if epoch > 10 and current_accuracy > 0.95:
            break
    
    # Training completed
    job["status"] = "completed"
    job["completed_at"] = datetime.utcnow()
    job["progress"] = 100.0
    
    # Generate model ID
    model_id = str(uuid4())
    job["model_id"] = model_id
    
    # Auto-deploy if requested
    if job["auto_deploy"]:
        # Simulate deployment
        await asyncio.sleep(0.1)
        job["deployed"] = True


@router.post("/jobs", response_model=TrainingJobResponse, status_code=status.HTTP_201_CREATED)
async def create_training_job(
    request: TrainingJobRequest,
    background_tasks: BackgroundTasks
):
    """Start a new model training job."""
    job_id = str(uuid4())
    now = datetime.utcnow()
    
    # Estimate completion time based on algorithm and data size
    base_minutes = {
        "linear_regression": 2,
        "logistic_regression": 3,
        "random_forest": 5,
        "xgboost": 8,
        "neural_network": 15,
        "deep_learning": 30
    }.get(request.algorithm, 10)
    
    estimated_completion = now + timedelta(minutes=base_minutes)
    
    job_data = {
        "job_id": job_id,
        "model_name": request.model_name,
        "description": request.description,
        "algorithm": request.algorithm,
        "status": "queued",
        "progress": 0.0,
        "metrics": None,
        "model_id": None,
        "error_message": None,
        "created_at": now,
        "started_at": None,
        "completed_at": None,
        "estimated_completion": estimated_completion,
        "auto_deploy": request.auto_deploy,
        "deployed": False,
        "hyperparameters": request.hyperparameters,
        "training_data": request.training_data.dict(),
        "validation": request.validation.dict(),
        "tags": request.tags
    }
    
    _training_jobs_db[job_id] = job_data
    
    # Start background training
    background_tasks.add_task(
        simulate_training_job,
        job_id,
        request.algorithm,
        request.hyperparameters
    )
    
    return TrainingJobResponse(**job_data)


@router.get("/jobs/{job_id}", response_model=TrainingJobResponse)
async def get_training_job(job_id: str):
    """Get details of a specific training job."""
    if job_id not in _training_jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training job {job_id} not found"
        )
    
    job_data = _training_jobs_db[job_id]
    
    # Convert metrics back to object if they exist
    metrics = None
    if job_data.get("metrics"):
        metrics = TrainingMetrics(**job_data["metrics"])
    
    return TrainingJobResponse(**{**job_data, "metrics": metrics})


@router.get("/jobs", response_model=List[TrainingJobResponse])
async def list_training_jobs(
    skip: int = 0,
    limit: int = 20,
    status_filter: Optional[str] = None,
    algorithm: Optional[str] = None,
    tags: Optional[str] = None
):
    """List training jobs with optional filtering."""
    jobs = list(_training_jobs_db.values())
    
    # Apply filters
    if status_filter:
        jobs = [job for job in jobs if job["status"] == status_filter]
    if algorithm:
        jobs = [job for job in jobs if job["algorithm"] == algorithm]
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",")]
        jobs = [job for job in jobs if any(tag in job.get("tags", []) for tag in tag_list)]
    
    # Sort by creation time (newest first)
    jobs = sorted(jobs, key=lambda x: x["created_at"], reverse=True)
    
    # Apply pagination
    jobs = jobs[skip:skip + limit]
    
    # Convert to response models
    response_jobs = []
    for job in jobs:
        metrics = None
        if job.get("metrics"):
            metrics = TrainingMetrics(**job["metrics"])
        response_jobs.append(TrainingJobResponse(**{**job, "metrics": metrics}))
    
    return response_jobs


@router.patch("/jobs/{job_id}/cancel", response_model=TrainingJobResponse)
async def cancel_training_job(job_id: str):
    """Cancel a running training job."""
    if job_id not in _training_jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training job {job_id} not found"
        )
    
    job = _training_jobs_db[job_id]
    
    if job["status"] not in ["queued", "running"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel job with status: {job['status']}"
        )
    
    job["status"] = "cancelled"
    job["completed_at"] = datetime.utcnow()
    job["error_message"] = "Training job cancelled by user"
    
    return TrainingJobResponse(**job)


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_training_job(job_id: str):
    """Delete a training job and its artifacts."""
    if job_id not in _training_jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training job {job_id} not found"
        )
    
    job = _training_jobs_db[job_id]
    
    if job["status"] in ["running", "queued"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete running or queued jobs. Cancel the job first."
        )
    
    del _training_jobs_db[job_id]


@router.post("/hyperparameter-tuning", response_model=TrainingJobResponse)
async def start_hyperparameter_tuning(
    request: HyperparameterTuningRequest,
    background_tasks: BackgroundTasks
):
    """Start hyperparameter tuning job."""
    job_id = str(uuid4())
    now = datetime.utcnow()
    
    # Estimate completion time for hyperparameter tuning
    estimated_minutes = request.max_trials * 2  # 2 minutes per trial
    estimated_completion = now + timedelta(minutes=estimated_minutes)
    
    # Create training job with hyperparameter tuning
    job_data = {
        "job_id": job_id,
        "model_name": f"{request.model_name}_tuned",
        "description": f"Hyperparameter tuning for {request.model_name}",
        "algorithm": request.algorithm,
        "status": "queued",
        "progress": 0.0,
        "metrics": None,
        "model_id": None,
        "error_message": None,
        "created_at": now,
        "started_at": None,
        "completed_at": None,
        "estimated_completion": estimated_completion,
        "auto_deploy": False,
        "deployed": False,
        "hyperparameters": {"tuning": True, "max_trials": request.max_trials},
        "training_data": request.training_data.dict(),
        "validation": request.validation.dict(),
        "tags": ["hyperparameter_tuning"]
    }
    
    _training_jobs_db[job_id] = job_data
    
    # Start background tuning (simplified as regular training for demo)
    background_tasks.add_task(
        simulate_training_job,
        job_id,
        request.algorithm,
        {"n_estimators": request.max_trials}
    )
    
    return TrainingJobResponse(**job_data)


@router.get("/algorithms")
async def get_supported_algorithms():
    """Get list of supported ML algorithms."""
    return {
        "algorithms": [
            {
                "name": "linear_regression",
                "type": "regression",
                "description": "Linear regression for continuous targets",
                "hyperparameters": ["fit_intercept", "normalize"]
            },
            {
                "name": "logistic_regression",
                "type": "classification",
                "description": "Logistic regression for binary/multiclass classification",
                "hyperparameters": ["C", "penalty", "solver", "max_iter"]
            },
            {
                "name": "random_forest",
                "type": "both",
                "description": "Random Forest ensemble method",
                "hyperparameters": ["n_estimators", "max_depth", "min_samples_split", "random_state"]
            },
            {
                "name": "xgboost",
                "type": "both",
                "description": "XGBoost gradient boosting",
                "hyperparameters": ["learning_rate", "max_depth", "n_estimators", "subsample"]
            },
            {
                "name": "neural_network",
                "type": "both",
                "description": "Multi-layer Perceptron neural network",
                "hyperparameters": ["hidden_layer_sizes", "activation", "learning_rate", "max_iter"]
            }
        ]
    }


@router.get("/stats/overview")
async def get_training_stats():
    """Get overall training statistics."""
    total_jobs = len(_training_jobs_db)
    
    status_counts = {}
    algorithm_counts = {}
    successful_jobs = 0
    
    for job in _training_jobs_db.values():
        status = job["status"]
        algorithm = job["algorithm"]
        
        status_counts[status] = status_counts.get(status, 0) + 1
        algorithm_counts[algorithm] = algorithm_counts.get(algorithm, 0) + 1
        
        if status == "completed":
            successful_jobs += 1
    
    success_rate = (successful_jobs / total_jobs * 100) if total_jobs > 0 else 0
    
    return {
        "total_jobs": total_jobs,
        "successful_jobs": successful_jobs,
        "success_rate": round(success_rate, 2),
        "status_distribution": status_counts,
        "algorithm_distribution": algorithm_counts,
        "avg_training_time_minutes": 5.2  # Mock average
    }