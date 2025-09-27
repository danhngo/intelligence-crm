"""Predictions API endpoints for batch processing and job management."""

from typing import List, Optional, Dict, Any, Union
from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field
import asyncio

router = APIRouter()


class BatchItem(BaseModel):
    """Individual item in a batch prediction request."""
    id: str = Field(..., description="Item identifier")
    inputs: Dict[str, Union[str, int, float, bool]] = Field(..., description="Input data")


class BatchPredictionRequest(BaseModel):
    """Batch prediction request schema."""
    model_id: str = Field(..., description="Model ID to use for predictions")
    batch_data: List[BatchItem] = Field(..., description="Batch of input data")
    callback_url: Optional[str] = Field(None, description="Callback URL for completion notification")
    priority: str = Field(default="normal", description="Job priority (low, normal, high)")


class PredictionResult(BaseModel):
    """Individual prediction result."""
    id: str = Field(..., description="Item identifier")
    prediction: Union[str, int, float, Dict[str, Any]] = Field(..., description="Prediction result")
    confidence: Optional[float] = Field(None, description="Prediction confidence")
    error: Optional[str] = Field(None, description="Error message if prediction failed")


class BatchJobResponse(BaseModel):
    """Batch job response schema."""
    job_id: str = Field(..., description="Job identifier")
    status: str = Field(..., description="Job status")
    model_id: str = Field(..., description="Model ID used")
    total_items: int = Field(..., description="Total number of items to process")
    completed_items: int = Field(default=0, description="Number of completed items")
    failed_items: int = Field(default=0, description="Number of failed items")
    results: Optional[List[PredictionResult]] = Field(None, description="Prediction results")
    created_at: datetime = Field(..., description="Job creation timestamp")
    started_at: Optional[datetime] = Field(None, description="Job start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Job completion timestamp")
    progress: float = Field(default=0.0, description="Job progress percentage")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")


class JobStatusUpdate(BaseModel):
    """Job status update schema."""
    status: str = Field(..., description="New job status")
    message: Optional[str] = Field(None, description="Status message")


# Mock database for prediction jobs
_jobs_db: Dict[str, Dict[str, Any]] = {}


async def process_batch_predictions(job_id: str, model_id: str, batch_data: List[BatchItem]):
    """Background task to process batch predictions."""
    job = _jobs_db[job_id]
    job["status"] = "running"
    job["started_at"] = datetime.utcnow()
    
    results = []
    completed = 0
    failed = 0
    
    for item in batch_data:
        try:
            # Simulate prediction processing time
            await asyncio.sleep(0.1)
            
            # Mock prediction logic (in real implementation, call the model)
            if "engagement_score" in item.inputs:
                # Lead scoring prediction
                engagement_score = item.inputs.get("engagement_score", 0.5)
                profile_score = item.inputs.get("profile_score", 0.5)
                score = (engagement_score * 0.6 + profile_score * 0.4)
                
                result = PredictionResult(
                    id=item.id,
                    prediction={
                        "category": "high" if score > 0.7 else "medium" if score > 0.4 else "low",
                        "score": round(score, 3)
                    },
                    confidence=round(score, 3)
                )
            else:
                # Generic prediction
                result = PredictionResult(
                    id=item.id,
                    prediction="positive",
                    confidence=0.85
                )
            
            results.append(result)
            completed += 1
            
        except Exception as e:
            result = PredictionResult(
                id=item.id,
                prediction=None,
                error=str(e)
            )
            results.append(result)
            failed += 1
        
        # Update progress
        progress = (completed + failed) / len(batch_data) * 100
        job["progress"] = progress
        job["completed_items"] = completed
        job["failed_items"] = failed
    
    # Job completed
    job["status"] = "completed" if failed == 0 else "completed_with_errors"
    job["completed_at"] = datetime.utcnow()
    job["results"] = [result.dict() for result in results]


@router.post("/batch", response_model=BatchJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_batch_prediction(
    request: BatchPredictionRequest,
    background_tasks: BackgroundTasks
):
    """Create a batch prediction job."""
    job_id = str(uuid4())
    now = datetime.utcnow()
    
    # Estimate completion time (mock calculation)
    estimated_duration_minutes = len(request.batch_data) * 0.1 / 60  # 0.1 seconds per item
    estimated_completion = datetime.utcnow()
    if estimated_duration_minutes > 0.1:  # Only set if more than 6 seconds
        from datetime import timedelta
        estimated_completion = now + timedelta(minutes=estimated_duration_minutes)
    
    job_data = {
        "job_id": job_id,
        "status": "queued",
        "model_id": request.model_id,
        "total_items": len(request.batch_data),
        "completed_items": 0,
        "failed_items": 0,
        "results": None,
        "created_at": now,
        "started_at": None,
        "completed_at": None,
        "progress": 0.0,
        "estimated_completion": estimated_completion,
        "callback_url": request.callback_url,
        "priority": request.priority
    }
    
    _jobs_db[job_id] = job_data
    
    # Start background processing
    background_tasks.add_task(
        process_batch_predictions,
        job_id,
        request.model_id,
        request.batch_data
    )
    
    return BatchJobResponse(**job_data)


@router.get("/{job_id}", response_model=BatchJobResponse)
async def get_prediction_job(job_id: str):
    """Get the status and results of a prediction job."""
    if job_id not in _jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction job {job_id} not found"
        )
    
    job_data = _jobs_db[job_id]
    
    # Convert results back to PredictionResult objects if they exist
    results = None
    if job_data.get("results"):
        results = [PredictionResult(**result) for result in job_data["results"]]
    
    return BatchJobResponse(**{**job_data, "results": results})


@router.get("/", response_model=List[BatchJobResponse])
async def list_prediction_jobs(
    skip: int = 0,
    limit: int = 20,
    status_filter: Optional[str] = None,
    model_id: Optional[str] = None
):
    """List prediction jobs with optional filtering."""
    jobs = list(_jobs_db.values())
    
    # Apply filters
    if status_filter:
        jobs = [job for job in jobs if job["status"] == status_filter]
    if model_id:
        jobs = [job for job in jobs if job["model_id"] == model_id]
    
    # Sort by creation time (newest first)
    jobs = sorted(jobs, key=lambda x: x["created_at"], reverse=True)
    
    # Apply pagination
    jobs = jobs[skip:skip + limit]
    
    # Convert to response models
    response_jobs = []
    for job in jobs:
        results = None
        if job.get("results"):
            results = [PredictionResult(**result) for result in job["results"]]
        response_jobs.append(BatchJobResponse(**{**job, "results": results}))
    
    return response_jobs


@router.patch("/{job_id}/status", response_model=BatchJobResponse)
async def update_job_status(job_id: str, update: JobStatusUpdate):
    """Update the status of a prediction job (admin operation)."""
    if job_id not in _jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction job {job_id} not found"
        )
    
    job = _jobs_db[job_id]
    
    # Only allow certain status transitions
    allowed_transitions = {
        "queued": ["running", "cancelled"],
        "running": ["completed", "failed", "cancelled"],
        "completed": [],
        "failed": ["queued"],  # Allow retry
        "cancelled": ["queued"]  # Allow restart
    }
    
    current_status = job["status"]
    new_status = update.status
    
    if new_status not in allowed_transitions.get(current_status, []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot transition from {current_status} to {new_status}"
        )
    
    job["status"] = new_status
    if new_status in ["completed", "failed", "cancelled"]:
        job["completed_at"] = datetime.utcnow()
    
    return BatchJobResponse(**job)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prediction_job(job_id: str):
    """Delete a prediction job and its results."""
    if job_id not in _jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction job {job_id} not found"
        )
    
    job = _jobs_db[job_id]
    
    # Only allow deletion of completed or failed jobs
    if job["status"] in ["running", "queued"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete running or queued jobs. Cancel the job first."
        )
    
    del _jobs_db[job_id]


@router.get("/{job_id}/results", response_model=List[PredictionResult])
async def get_job_results(job_id: str, skip: int = 0, limit: int = 100):
    """Get paginated results from a completed prediction job."""
    if job_id not in _jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction job {job_id} not found"
        )
    
    job = _jobs_db[job_id]
    
    if not job.get("results"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No results available for this job"
        )
    
    results = job["results"][skip:skip + limit]
    return [PredictionResult(**result) for result in results]


@router.get("/stats/overview")
async def get_prediction_stats():
    """Get overall prediction statistics."""
    total_jobs = len(_jobs_db)
    
    status_counts = {}
    total_predictions = 0
    successful_predictions = 0
    
    for job in _jobs_db.values():
        status = job["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
        total_predictions += job["total_items"]
        successful_predictions += job["completed_items"]
    
    success_rate = (successful_predictions / total_predictions * 100) if total_predictions > 0 else 0
    
    return {
        "total_jobs": total_jobs,
        "status_distribution": status_counts,
        "total_predictions": total_predictions,
        "successful_predictions": successful_predictions,
        "success_rate": round(success_rate, 2),
        "avg_items_per_job": round(total_predictions / total_jobs, 1) if total_jobs > 0 else 0
    }