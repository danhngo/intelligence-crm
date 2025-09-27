# AI Orchestration Service Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [API Endpoints](#api-endpoints)
5. [Data Models](#data-models)
6. [Current Implementation](#current-implementation)
7. [Third-Party Integration Requirements](#third-party-integration-requirements)
8. [Deployment Guide](#deployment-guide)
9. [Development Workflow](#development-workflow)
10. [Future Enhancements](#future-enhancements)

---

## 🎯 Overview

The AI Orchestration Service is a comprehensive FastAPI-based microservice that manages all AI/ML operations within the CRM platform. It provides centralized management for machine learning models, batch predictions, training jobs, and automated workflows.

### Key Capabilities
- **Model Management**: Deploy, version, and monitor ML models
- **Batch Processing**: Execute large-scale predictions asynchronously
- **Training Orchestration**: Manage model training lifecycles
- **Workflow Automation**: Orchestrate complex AI processes
- **Real-time Monitoring**: Track performance and health metrics

### Service Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                 AI Orchestration Service                    │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Model Mgmt    │   Predictions   │    Training Jobs        │
├─────────────────┼─────────────────┼─────────────────────────┤
│   Workflows     │   Analytics     │    Health Monitoring    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture

### High-Level Architecture
```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Frontend   │───▶│   API Proxy  │───▶│ AI Service   │
│  (Next.js)   │    │  (Next.js)   │    │  (FastAPI)   │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          ▼                          │
            ┌───────────────┐        ┌─────────────────┐        ┌─────────────────┐
            │   Database    │        │  ML Frameworks  │        │  External APIs  │
            │ (PostgreSQL)  │        │ (scikit-learn,  │        │ (OpenAI, etc.)  │
            │               │        │  PyTorch, etc.) │        │                 │
            └───────────────┘        └─────────────────┘        └─────────────────┘
```

### Component Interaction Flow
1. **Request**: Frontend sends API requests through proxy routes
2. **Processing**: AI service validates and processes requests
3. **Storage**: Data persisted to PostgreSQL database
4. **Execution**: Background tasks execute ML operations
5. **Response**: Real-time status updates and results returned

---

## 🧩 Core Components

### 1. Model Management (`models.py`)
**Purpose**: Centralized ML model lifecycle management

**Key Features**:
- Model registration and metadata storage
- Version control and deployment tracking
- Performance monitoring and metrics
- A/B testing support

**Data Flow**:
```
Model Creation → Validation → Storage → Deployment → Monitoring
```

### 2. Prediction Engine (`predictions.py`)
**Purpose**: Batch and real-time prediction processing

**Key Features**:
- Asynchronous batch processing
- Job queue management
- Progress tracking and status updates
- Result aggregation and storage

**Processing Pipeline**:
```
Input Data → Validation → Model Loading → Prediction → Result Storage → Notification
```

### 3. Training Orchestrator (`training.py`)
**Purpose**: ML model training lifecycle management

**Key Features**:
- Training job scheduling and execution
- Hyperparameter tuning automation
- Progress monitoring with real-time metrics
- Model evaluation and validation

**Training Pipeline**:
```
Data Preparation → Model Configuration → Training Execution → Validation → Deployment
```

### 4. Workflow Engine (`workflows.py`)
**Purpose**: Automated AI process orchestration

**Key Features**:
- Multi-step workflow definition
- Conditional execution logic
- Error handling and retry mechanisms
- Integration with external services

**Workflow Structure**:
```
Trigger → Validation → Step Execution → Decision Points → Completion/Error Handling
```

---

## 📡 API Endpoints

### Models API (`/api/v1/models/`)
```http
GET    /api/v1/models/                    # List all models
POST   /api/v1/models/                    # Create new model  
GET    /api/v1/models/{id}                # Get model details
PUT    /api/v1/models/{id}                # Update model
DELETE /api/v1/models/{id}                # Delete model
POST   /api/v1/models/{id}/predict        # Execute prediction
POST   /api/v1/models/{id}/deploy         # Deploy model
```

### Predictions API (`/api/v1/predictions/`)
```http
GET    /api/v1/predictions/               # List prediction jobs
POST   /api/v1/predictions/batch          # Start batch prediction
GET    /api/v1/predictions/{id}           # Get job details
DELETE /api/v1/predictions/{id}           # Cancel job
GET    /api/v1/predictions/{id}/results   # Get results
```

### Training API (`/api/v1/training/`)
```http
GET    /api/v1/training/jobs              # List training jobs
POST   /api/v1/training/jobs              # Start training job
GET    /api/v1/training/jobs/{id}         # Get job details
PATCH  /api/v1/training/jobs/{id}/cancel  # Cancel training
DELETE /api/v1/training/jobs/{id}         # Delete job
POST   /api/v1/training/hyperparameter-tuning  # Start hyperparameter tuning
```

### Workflows API (`/api/v1/workflows/`)
```http
GET    /api/v1/workflows/                 # List workflows
POST   /api/v1/workflows/                 # Create workflow
GET    /api/v1/workflows/{id}             # Get workflow details
PUT    /api/v1/workflows/{id}             # Update workflow
DELETE /api/v1/workflows/{id}             # Delete workflow
POST   /api/v1/workflows/{id}/execute     # Execute workflow
```

---

## 💾 Data Models

### AI Model Schema
```python
class AIModel(BaseModel):
    id: str
    name: str
    description: Optional[str]
    type: str  # "classification", "regression", "clustering"
    framework: str  # "scikit-learn", "pytorch", "tensorflow"
    version: str
    status: str  # "training", "deployed", "deprecated"
    accuracy: Optional[float]
    model_configuration: Dict[str, Any]
    input_schema: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    deployment_url: Optional[str]
```

### Training Job Schema
```python
class TrainingJob(BaseModel):
    job_id: str
    model_name: str
    algorithm: str
    status: str  # "queued", "running", "completed", "failed"
    progress: float
    metrics: Optional[TrainingMetrics]
    hyperparameters: Dict[str, Any]
    training_data: TrainingDataSource
    validation_config: ValidationConfig
    created_at: datetime
    estimated_completion: Optional[datetime]
```

### Prediction Job Schema
```python
class PredictionJob(BaseModel):
    job_id: str
    model_id: str
    status: str  # "queued", "running", "completed", "failed"
    total_items: int
    completed_items: int
    failed_items: int
    progress: float
    results: List[PredictionResult]
    created_at: datetime
```

---

## 🔧 Current Implementation

### Technology Stack
- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL (via SQLAlchemy)
- **Caching**: Redis
- **Task Queue**: Background Tasks (FastAPI)
- **Validation**: Pydantic v2
- **Authentication**: JWT (planned)
- **Monitoring**: Prometheus metrics (planned)

### Current Status
✅ **Implemented**:
- Complete API endpoints with FastAPI
- Pydantic schemas for data validation
- Mock in-memory storage for development
- Background task processing simulation
- CORS configuration for frontend integration
- Comprehensive error handling

🚧 **In Progress**:
- Database integration (SQLAlchemy models created)
- Redis caching layer
- Authentication and authorization

📋 **Planned**:
- Real ML library integration
- Production database deployment
- Monitoring and logging
- Performance optimization

### File Structure
```
services/ai-orchestration/
├── app/
│   ├── api/v1/
│   │   ├── models.py           # Model management endpoints
│   │   ├── predictions.py      # Prediction job endpoints
│   │   ├── training.py         # Training job endpoints
│   │   ├── workflows.py        # Workflow orchestration endpoints
│   │   └── __init__.py         # API router configuration
│   ├── core/
│   │   ├── config.py           # Application configuration
│   │   ├── database.py         # Database connection setup
│   │   ├── cache.py            # Redis caching setup
│   │   └── security.py         # Authentication utilities
│   ├── models/
│   │   ├── ai_models.py        # SQLAlchemy ORM models
│   │   └── schemas.py          # Pydantic response models
│   └── main.py                 # FastAPI application setup
├── requirements.txt            # Python dependencies
└── Dockerfile                 # Container configuration
```

---

## 🔌 Third-Party Integration Requirements

### Required Integrations

#### 1. **Machine Learning Frameworks**
```python
# Core ML Libraries (Required)
scikit-learn>=1.3.0        # Traditional ML algorithms
pandas>=2.0.0               # Data manipulation
numpy>=1.24.0               # Mathematical operations

# Deep Learning (Optional)
torch>=2.0.0                # PyTorch for neural networks
tensorflow>=2.13.0          # TensorFlow alternative
transformers>=4.30.0        # HuggingFace transformers
```

#### 2. **External AI APIs** (Optional Enhancement)
```python
# OpenAI Integration
openai>=1.0.0               # GPT models for text processing
```

**Use Cases**:
- **Text Analysis**: Sentiment analysis, entity extraction
- **Content Generation**: Email templates, marketing copy
- **Advanced NLP**: Document summarization, translation

**Implementation Example**:
```python
from openai import OpenAI

class AIServiceIntegration:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def analyze_customer_feedback(self, feedback_text: str):
        response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Analyze customer feedback sentiment"},
                {"role": "user", "content": feedback_text}
            ]
        )
        return response.choices[0].message.content
```

#### 3. **Cloud ML Services** (Production Enhancement)
```yaml
# AWS Integration
boto3>=1.28.0               # AWS SDK
sagemaker>=2.180.0          # AWS SageMaker

# Google Cloud
google-cloud-aiplatform>=1.30.0  # Google AI Platform
google-cloud-storage>=2.10.0     # Cloud Storage

# Azure
azure-ai-ml>=1.10.0         # Azure ML
azure-storage-blob>=12.17.0  # Blob Storage
```

#### 4. **Data Processing & Storage**
```python
# Database
psycopg2-binary>=2.9.0      # PostgreSQL adapter
redis>=4.5.0                # Redis for caching

# Data Processing
apache-airflow>=2.7.0       # Workflow orchestration (advanced)
celery>=5.3.0               # Distributed task queue (scale-up)
```

#### 5. **Monitoring & Observability**
```python
# Monitoring
prometheus-client>=0.17.0   # Metrics collection
sentry-sdk>=1.30.0          # Error tracking
structlog>=23.0.0           # Structured logging

# Performance
aioredis>=2.0.0             # Async Redis
asyncpg>=0.28.0             # Async PostgreSQL
```

### Integration Architecture

#### External API Flow
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CRM Request   │───▶│ AI Orchestrator │───▶│  External API   │
└─────────────────┘    └─────────────────┘    │   (OpenAI)      │
                               │               └─────────────────┘
                               ▼                        │
                      ┌─────────────────┐              │
                      │     Cache       │◀─────────────┘
                      │    (Redis)      │
                      └─────────────────┘
```

#### Data Processing Pipeline
```
Raw Data → Preprocessing → Feature Engineering → Model Training → Evaluation → Deployment
    ↓           ↓              ↓                    ↓            ↓         ↓
  Storage    Validation    Transformation       Monitoring   Metrics   Serving
```

### Configuration Requirements

#### Environment Variables
```bash
# Core Configuration
AI_SERVICE_PORT=8005
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_db
REDIS_URL=redis://localhost:6379/0

# External APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
HUGGINGFACE_API_TOKEN=hf_...

# Cloud Services (Optional)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
GOOGLE_CLOUD_PROJECT_ID=...
AZURE_TENANT_ID=...

# Security
JWT_SECRET_KEY=...
CORS_ORIGINS=http://localhost:3000,http://localhost:3002
```

---

## 🚀 Deployment Guide

### Local Development
```bash
# 1. Install Dependencies
cd services/ai-orchestration
pip install -r requirements.txt

# 2. Set Environment Variables
export DATABASE_URL="postgresql://localhost:5432/ai_dev"
export REDIS_URL="redis://localhost:6379/0"

# 3. Start Services
docker-compose up -d postgres redis  # Database services
python -m uvicorn app.main:app --reload --port 8005
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]
```

### Production Deployment
```yaml
# docker-compose.prod.yml
services:
  ai-orchestration:
    build: ./services/ai-orchestration
    ports:
      - "8005:8005"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - postgres
      - redis
    
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ai_production
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
```

---

## 🔄 Development Workflow

### Adding New ML Models
1. **Define Model Schema**: Update Pydantic models
2. **Create Training Pipeline**: Implement training logic
3. **Add API Endpoints**: Create CRUD operations
4. **Test Integration**: Verify end-to-end functionality
5. **Update Documentation**: Document new capabilities

### Integrating External APIs
1. **Add Dependencies**: Update requirements.txt
2. **Configuration**: Add environment variables
3. **Service Layer**: Create integration service
4. **Error Handling**: Implement retry logic
5. **Caching**: Add response caching
6. **Testing**: Mock external services for tests

### Example: Adding OpenAI Integration
```python
# 1. Service Implementation
class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_lead_insights(self, lead_data: dict) -> str:
        prompt = f"Analyze this lead data and provide insights: {lead_data}"
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

# 2. API Endpoint
@router.post("/leads/{lead_id}/ai-insights")
async def generate_lead_insights(lead_id: str, openai_service: OpenAIService = Depends()):
    insights = await openai_service.generate_lead_insights(lead_data)
    return {"insights": insights}
```

---

## 🔮 Future Enhancements

### Short-term (Next 2-3 Months)
- [ ] **Database Integration**: Replace mock storage with PostgreSQL
- [ ] **Authentication**: Implement JWT-based security
- [ ] **Real ML Libraries**: Integrate scikit-learn for actual predictions
- [ ] **File Upload**: Support dataset uploads for training
- [ ] **WebSocket Updates**: Real-time progress notifications

### Medium-term (3-6 Months)
- [ ] **Advanced ML**: PyTorch/TensorFlow integration
- [ ] **Model Registry**: Versioned model storage (MLflow)
- [ ] **A/B Testing**: Model performance comparison
- [ ] **Auto-scaling**: Kubernetes deployment
- [ ] **Monitoring**: Prometheus + Grafana dashboards

### Long-term (6+ Months)
- [ ] **AutoML**: Automated model selection and tuning
- [ ] **Federated Learning**: Distributed model training
- [ ] **Edge Deployment**: Model deployment to edge devices
- [ ] **Advanced Workflows**: Complex multi-model pipelines
- [ ] **Compliance**: GDPR/compliance features

### Third-Party Roadmap
```
Phase 1: Basic ML (scikit-learn, pandas)
Phase 2: Cloud ML (AWS SageMaker, Google AI Platform)  
Phase 3: Advanced AI (OpenAI, Anthropic Claude)
Phase 4: Specialized Services (Computer Vision, NLP APIs)
```

---

## 📞 Support & Resources

### Documentation Links
- **API Documentation**: http://localhost:8005/docs (when running)
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pydantic**: https://docs.pydantic.dev/
- **SQLAlchemy**: https://docs.sqlalchemy.org/

### Development Resources
- **Code Repository**: `/services/ai-orchestration/`
- **Test Files**: `/tests/ai-orchestration/`
- **Configuration**: `app/core/config.py`
- **API Routes**: `app/api/v1/`

### Integration Examples
- **Frontend Integration**: `/frontend/src/app/api/ai/`
- **Test Endpoints**: See `ai-test.html` for testing interface
- **Postman Collection**: `/postman-collections/05-ai-orchestration-api.json`

---

## 🎯 Summary

The AI Orchestration Service provides a robust foundation for ML operations within the CRM platform. The current implementation offers:

✅ **Complete API layer** with comprehensive endpoints
✅ **Modular architecture** supporting multiple ML frameworks  
✅ **Async processing** for scalable batch operations
✅ **Real-time monitoring** with progress tracking
✅ **Production-ready structure** with proper error handling

The service is designed to start with mock implementations and gradually integrate with real ML libraries and external APIs as requirements evolve. The modular architecture ensures easy extension and integration of new AI capabilities.

**Next Steps**: 
1. Integrate real ML libraries (scikit-learn)
2. Connect to production database
3. Add external API integrations (OpenAI, etc.)
4. Implement comprehensive monitoring

This architecture provides a solid foundation for building sophisticated AI-powered features while maintaining flexibility for future enhancements.