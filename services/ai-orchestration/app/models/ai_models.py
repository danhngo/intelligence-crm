"""AI Model Management Database Models

This module defines the database models for AI model storage, versioning,
deployment tracking, and performance monitoring.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

from sqlalchemy import Column, DateTime, Integer, String, JSON, Float, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base


class ModelStatus(str, Enum):
    """AI model deployment status."""
    DRAFT = "draft"
    TRAINING = "training"
    DEPLOYED = "deployed"
    DEPRECATED = "deprecated"
    FAILED = "failed"


class ModelType(str, Enum):
    """Types of AI models."""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    RECOMMENDATION = "recommendation"
    NATURAL_LANGUAGE = "natural_language"
    COMPUTER_VISION = "computer_vision"


class ModelFramework(str, Enum):
    """ML frameworks supported."""
    SCIKIT_LEARN = "scikit-learn"
    TENSORFLOW = "tensorflow"
    PYTORCH = "pytorch"
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"
    HUGGINGFACE = "huggingface"
    LANGCHAIN = "langchain"


class AIModel(Base):
    """AI model registry and metadata."""
    
    # Model identification
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    version = Column(String, nullable=False)
    
    # Model classification
    model_type = Column(String, nullable=False)  # Use string for flexibility
    framework = Column(String, nullable=False)
    algorithm = Column(String)
    
    # Status and lifecycle
    status = Column(String, nullable=False, default=ModelStatus.DRAFT.value)
    
    # Model configuration and schema
    model_config = Column(JSON, nullable=False, default=dict)
    input_schema = Column(JSON, nullable=False, default=dict)
    output_schema = Column(JSON, default=dict)
    
    # Performance metrics
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    
    # Deployment information
    deployment_url = Column(String)
    deployment_config = Column(JSON, default=dict)
    
    # Model artifacts and storage
    model_path = Column(String)
    checkpoint_path = Column(String)
    artifacts_metadata = Column(JSON, default=dict)
    
    # Usage tracking
    prediction_count = Column(Integer, default=0)
    total_inference_time_ms = Column(Integer, default=0)
    avg_inference_time_ms = Column(Float, default=0.0)
    
    # Training information
    training_job_id = Column(UUID(as_uuid=True))
    training_data_info = Column(JSON, default=dict)
    hyperparameters = Column(JSON, default=dict)
    
    # Versioning and lineage
    parent_model_id = Column(UUID(as_uuid=True))
    tags = Column(JSON, default=list)
    
    def update_performance_metrics(
        self,
        accuracy: Optional[float] = None,
        precision: Optional[float] = None,
        recall: Optional[float] = None,
        f1_score: Optional[float] = None
    ) -> None:
        """Update model performance metrics."""
        if accuracy is not None:
            self.accuracy = accuracy
        if precision is not None:
            self.precision = precision
        if recall is not None:
            self.recall = recall
        if f1_score is not None:
            self.f1_score = f1_score
        
        self.updated_at = datetime.utcnow()
    
    def record_prediction(self, inference_time_ms: int) -> None:
        """Record a prediction and update usage metrics."""
        self.prediction_count += 1
        self.total_inference_time_ms += inference_time_ms
        self.avg_inference_time_ms = self.total_inference_time_ms / self.prediction_count
        self.updated_at = datetime.utcnow()


class PredictionJob(Base):
    """Batch prediction job tracking."""
    
    # Job identification
    job_name = Column(String)
    model_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Job configuration
    batch_size = Column(Integer)
    priority = Column(String, default="normal")
    callback_url = Column(String)
    
    # Status and progress
    status = Column(String, nullable=False, default="queued")
    progress = Column(Float, default=0.0)
    
    # Data and results
    input_data = Column(JSON)
    results = Column(JSON)
    
    # Execution timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    estimated_completion = Column(DateTime(timezone=True))
    
    # Metrics and statistics
    total_items = Column(Integer, default=0)
    completed_items = Column(Integer, default=0)
    failed_items = Column(Integer, default=0)
    
    # Error tracking
    error_message = Column(Text)
    error_details = Column(JSON)
    
    def update_progress(self, completed: int, failed: int = 0) -> None:
        """Update job progress."""
        self.completed_items = completed
        self.failed_items = failed
        
        if self.total_items > 0:
            self.progress = (completed + failed) / self.total_items * 100.0
        
        self.updated_at = datetime.utcnow()


class TrainingJob(Base):
    """Model training job tracking."""
    
    # Job identification
    job_name = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    description = Column(Text)
    
    # Training configuration
    algorithm = Column(String, nullable=False)
    hyperparameters = Column(JSON, nullable=False, default=dict)
    training_config = Column(JSON, default=dict)
    
    # Data configuration
    training_data_source = Column(JSON, nullable=False)
    validation_config = Column(JSON, default=dict)
    
    # Status and progress
    status = Column(String, nullable=False, default="queued")
    progress = Column(Float, default=0.0)
    
    # Execution timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    estimated_completion = Column(DateTime(timezone=True))
    
    # Training metrics
    current_epoch = Column(Integer, default=0)
    total_epochs = Column(Integer)
    training_loss = Column(Float)
    validation_loss = Column(Float)
    training_accuracy = Column(Float)
    validation_accuracy = Column(Float)
    
    # Final model information
    generated_model_id = Column(UUID(as_uuid=True))
    final_metrics = Column(JSON, default=dict)
    
    # Deployment settings
    auto_deploy = Column(Boolean, default=False)
    deployed = Column(Boolean, default=False)
    
    # Resource usage
    training_time_seconds = Column(Float)
    compute_cost = Column(Float)
    
    # Error tracking
    error_message = Column(Text)
    error_details = Column(JSON)
    
    # Tags and metadata
    tags = Column(JSON, default=list)
    experiment_metadata = Column(JSON, default=dict)
    
    def update_training_metrics(
        self,
        epoch: int,
        training_loss: Optional[float] = None,
        validation_loss: Optional[float] = None,
        training_accuracy: Optional[float] = None,
        validation_accuracy: Optional[float] = None
    ) -> None:
        """Update training progress and metrics."""
        self.current_epoch = epoch
        
        if training_loss is not None:
            self.training_loss = training_loss
        if validation_loss is not None:
            self.validation_loss = validation_loss
        if training_accuracy is not None:
            self.training_accuracy = training_accuracy
        if validation_accuracy is not None:
            self.validation_accuracy = validation_accuracy
        
        # Update progress if total epochs is known
        if self.total_epochs and self.total_epochs > 0:
            self.progress = (epoch / self.total_epochs) * 100.0
        
        self.updated_at = datetime.utcnow()
    
    def complete_training(
        self,
        model_id: UUID,
        final_metrics: Dict[str, Any],
        training_time: float
    ) -> None:
        """Complete training job with final results."""
        self.status = "completed"
        self.completed_at = datetime.utcnow()
        self.progress = 100.0
        self.generated_model_id = model_id
        self.final_metrics = final_metrics
        self.training_time_seconds = training_time


class ModelExperiment(Base):
    """Model experimentation and A/B testing tracking."""
    
    # Experiment identification
    experiment_name = Column(String, nullable=False, index=True)
    description = Column(Text)
    
    # Experiment configuration
    model_ids = Column(JSON, nullable=False)  # List of model IDs in experiment
    traffic_split = Column(JSON, default=dict)  # Traffic allocation percentages
    
    # Status and timing
    status = Column(String, default="draft")  # draft, running, paused, completed
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    
    # Success criteria
    primary_metric = Column(String)
    success_criteria = Column(JSON, default=dict)
    
    # Results and statistics
    results = Column(JSON, default=dict)
    statistical_significance = Column(Float)
    winner_model_id = Column(UUID(as_uuid=True))
    
    # Metadata
    tags = Column(JSON, default=list)
    experiment_metadata = Column(JSON, default=dict)