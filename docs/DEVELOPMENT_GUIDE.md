# Intelligence CRM - Development Guide

## 🚀 Getting Started

### Prerequisites
- **Docker**: For running services and databases
- **Python 3.11+**: For backend services
- **Node.js 18+**: For frontend development
- **Git**: Version control
- **Google Cloud Account**: For cloud services (optional for local dev)

### Repository Structure Understanding

```
intelligence-crm/
├── .claude/                    # 🤖 Claude Code Spec Framework
│   ├── commands/              # Custom commands for spec-driven development
│   ├── specs/                 # Feature specifications (requirements, design, tasks)
│   ├── steering/              # Project context documents
│   ├── templates/             # Document templates for consistency
│   └── agents/                # Validation agents for quality gates
├── services/                  # 🔧 Backend Microservices
│   ├── crm-core/             # Core CRM functionality (FastAPI)
│   ├── user-management/       # Auth & user management (FastAPI)
│   ├── ai-orchestration/      # LangChain AI services
│   ├── workflow-engine/       # Business process automation
│   ├── analytics-service/     # Real-time analytics
│   └── communication-hub/     # Multi-channel communication
├── frontend/                  # 🌐 Next.js Web Application
├── app/                       # 🔄 Shared workflow components
└── docs/                      # 📚 Documentation
```

## 🏗️ Development Workflow

### 1. Spec-Driven Development with Claude Framework

This project uses a **specification-driven development approach** managed by the Claude Code Spec Framework:

#### Available Commands
```bash
# Feature development workflow
/spec-create <feature-name>          # Create new feature specification
/spec-execute <feature-name> <task>  # Execute individual tasks
/spec-status <feature-name>          # Check progress
/spec-list                          # List all specifications

# Bug management
/bug-create <bug-name>              # Report and track bugs
/bug-analyze <bug-name>             # Analyze bug causes
/bug-fix <bug-name>                 # Implement bug fixes
```

#### Development Phases
1. **Requirements Phase**: Define user stories and acceptance criteria
2. **Design Phase**: Create architecture and technical design
3. **Tasks Phase**: Break down into atomic tasks (15-30 min each)
4. **Implementation Phase**: Execute tasks with validation

### 2. Understanding Atomic Tasks

Tasks are designed for optimal AI-assisted development:
- **File Scope**: 1-3 related files maximum
- **Time-Boxed**: 15-30 minutes completion time
- **Single Purpose**: One testable outcome per task
- **Specific Files**: Exact file paths specified
- **Requirements Traced**: Clear link to requirements

#### Example Good Task
```markdown
- [ ] 5.1 Create User model in internal/models/user.go with GORM tags
  - Add User struct with ID, Email, PasswordHash fields
  - Implement GORM tags for database mapping
  - Add validation tags and methods
  - _Requirements: 1.1, 1.2_
  - _Leverage: internal/models/base.go_
```

## 🔧 Service Development

### Backend Services Architecture

All backend services follow similar patterns:

```
service-name/
├── app/
│   ├── api/v1/               # API endpoints
│   ├── core/                 # Configuration and database
│   ├── models/               # Database models
│   ├── repositories/         # Data access layer
│   ├── schemas/              # Pydantic schemas for API
│   └── main.py              # FastAPI application
├── migrations/               # Database migrations
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

### Service Development Steps

#### 1. Set up Development Environment
```bash
# Navigate to service directory
cd services/crm-core

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### 2. Database Setup
```bash
# Start PostgreSQL with Docker
docker-compose up -d db

# Run database migrations
alembic upgrade head
```

#### 3. Run Service
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Or using Docker
docker-compose up -d
```

#### 4. API Documentation
Visit `http://localhost:8001/docs` for interactive API documentation.

### Key Service Patterns

#### 1. Multi-Tenant Architecture
All services implement tenant isolation:

```python
# Example: Tenant-aware repository
class ContactRepository:
    async def list(self, tenant_id: UUID, skip: int = 0, limit: int = 20):
        query = select(Contact).where(Contact.tenant_id == tenant_id)
        # All queries automatically filtered by tenant_id
```

#### 2. Error Handling
```python
from fastapi import HTTPException

# Consistent error responses
if not contact:
    raise HTTPException(
        status_code=404,
        detail="Contact not found"
    )
```

#### 3. Database Models
```python
from app.models.base import Base, TenantModelMixin, TimestampMixin

class Contact(Base, TenantModelMixin, TimestampMixin):
    __tablename__ = "contacts"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    # Inherits tenant_id, created_at, updated_at
```

## 🌐 Frontend Development

### Frontend Architecture
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **Components**: Headless UI + Heroicons
- **State Management**: React Query for server state
- **Forms**: React Hook Form with validation

### Frontend Development Steps

#### 1. Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### 2. Key Directories
```
src/
├── app/                      # Next.js App Router pages
│   ├── dashboard/           # Dashboard page
│   ├── contacts/            # Contact management
│   └── login/               # Authentication
├── components/              # Reusable components
│   ├── auth/               # Authentication components
│   └── layout/             # Layout components
├── hooks/                   # Custom React hooks
├── types/                   # TypeScript type definitions
└── styles/                  # Global styles
```

#### 3. Adding New Pages
```typescript
// app/new-feature/page.tsx
import { PageLayout } from '@/components/layout/PageLayout';

export default function NewFeaturePage() {
  return (
    <PageLayout title="New Feature">
      <div className="space-y-6">
        {/* Page content */}
      </div>
    </PageLayout>
  );
}
```

#### 4. API Integration
```typescript
// hooks/api.ts
import { useQuery } from 'react-query';

export function useContacts(tenantId: string) {
  return useQuery(['contacts', tenantId], 
    () => fetchContacts(tenantId)
  );
}
```

## 🤖 AI/ML Services Development

### LangChain Integration

The AI services use LangChain and LangGraph for intelligent automation:

```python
# Example: AI Orchestration Service
from langchain.agents import AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

class LeadScoringAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4")
        self.tools = [
            Tool(
                name="database_lookup",
                func=self._lookup_contact_history,
                description="Look up contact interaction history"
            )
        ]
        
    async def score_lead(self, contact_data: dict) -> float:
        # LangChain-powered lead scoring logic
        pass
```

### Vector Database Integration
```python
# Example: RAG implementation
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings

class CustomerInsights:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Pinecone.from_existing_index(
            "customer-insights", 
            self.embeddings
        )
    
    async def get_insights(self, customer_id: str) -> list[str]:
        # RAG-based customer insights
        pass
```

## 🧪 Testing

### Backend Testing
```bash
# Run tests for a service
cd services/crm-core
pytest

# With coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_contact_api.py
```

### Frontend Testing
```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run E2E tests
npm run test:e2e
```

### Test Structure
```python
# Example: API test
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_contact(client: AsyncClient, tenant_id: str):
    contact_data = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    response = await client.post(
        f"/api/v1/contacts/?tenant_id={tenant_id}",
        json=contact_data
    )
    
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
```

## 📊 Monitoring and Debugging

### Health Checks
All services expose health check endpoints:
```bash
# Check service health
curl http://localhost:8001/health

# Expected response
{"status": "healthy", "database": "connected"}
```

### Logging
Services use structured logging:
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "Contact created", 
    contact_id=contact.id, 
    tenant_id=tenant_id
)
```

### Performance Monitoring
- **Response Times**: Target < 2 seconds for 95% of requests
- **Database Queries**: Monitor N+1 queries and slow queries
- **Memory Usage**: Track memory leaks in long-running services

## 🚀 Deployment

### Local Development
```bash
# Start all services
docker-compose up -d

# Start individual service
cd services/crm-core && docker-compose up -d
```

### Production Deployment
```bash
# Build production images
docker build -t crm-core:latest services/crm-core/

# Deploy to Kubernetes
kubectl apply -f k8s/
```

## 🔧 Common Development Tasks

### 1. Adding a New API Endpoint
1. **Define Schema** (Pydantic models)
2. **Create Repository Method** (data access)
3. **Add API Endpoint** (FastAPI router)
4. **Write Tests** (unit and integration)
5. **Update Documentation** (OpenAPI automatic)

### 2. Adding Database Migration
```bash
# Generate migration
alembic revision --autogenerate -m "Add new field to contacts"

# Apply migration
alembic upgrade head
```

### 3. Adding New Frontend Component
```typescript
// components/ContactCard.tsx
interface ContactCardProps {
  contact: Contact;
  onEdit: (id: string) => void;
}

export function ContactCard({ contact, onEdit }: ContactCardProps) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-medium">{contact.name}</h3>
      <p className="text-gray-600">{contact.email}</p>
      <button 
        onClick={() => onEdit(contact.id)}
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
      >
        Edit
      </button>
    </div>
  );
}
```

### 4. Integrating New AI Feature
1. **Create LangChain Agent** in ai-orchestration service
2. **Add API Endpoint** for the AI feature
3. **Update Frontend** to consume AI insights
4. **Add Tests** for AI functionality
5. **Monitor Performance** and costs

## 🔍 Debugging Tips

### Backend Issues
```bash
# View service logs
docker-compose logs -f crm-core

# Connect to database
docker-compose exec db psql -U postgres -d crm_core

# Debug Python service
import pdb; pdb.set_trace()  # Add breakpoint
```

### Frontend Issues
```bash
# Next.js debug mode
DEBUG=* npm run dev

# Check network requests in browser DevTools
# Use React DevTools extension
```

### Performance Issues
- **Database**: Use `EXPLAIN ANALYZE` for slow queries
- **API**: Add timing middleware to measure endpoint performance
- **Frontend**: Use React DevTools Profiler
- **AI Services**: Monitor LangChain operation costs and latencies

## 📚 Learning Resources

### Recommended Study Path
1. **Microservices**: Start with CRM Core service structure
2. **FastAPI**: Learn async/await patterns and dependency injection
3. **Database Design**: Understand multi-tenancy patterns
4. **LangChain**: Explore AI orchestration examples
5. **Next.js**: Modern React patterns and App Router
6. **Testing**: Test-driven development practices
7. **Docker/Kubernetes**: Containerization and orchestration

### Key Files to Study
- `services/crm-core/app/main.py` - FastAPI application setup
- `services/crm-core/app/models/base.py` - Database model patterns
- `services/crm-core/app/api/v1/contacts.py` - API endpoint patterns
- `frontend/src/app/layout.tsx` - Next.js layout patterns
- `.claude/specs/*/requirements.md` - Requirements documentation

This development guide provides a comprehensive overview of working with the Intelligence CRM platform. The spec-driven approach ensures consistent development patterns while the modern tech stack provides excellent learning opportunities in AI, cloud-native development, and modern web applications.