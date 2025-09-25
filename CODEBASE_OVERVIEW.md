# Intelligence CRM Platform - Codebase Overview

## 🎯 Project Purpose

The Intelligence CRM Platform is a **microservices-based, AI-powered CRM and workflow automation platform** specifically designed for small and medium businesses (SMBs) in the marketing industry. This project serves dual objectives:

1. **Production-Ready SaaS Platform**: Democratizes enterprise-level AI capabilities for SMBs
2. **AI Learning Platform**: Hands-on experience with cutting-edge AI technologies including LangChain, LangGraph, and agentic development workflows

## 🏗️ Architecture Overview

### Core Architecture Pattern
- **Microservices Architecture**: Domain-driven design with independent services
- **Cloud-Native**: Built for Google Cloud Platform (GKE, Cloud SQL, Redis, etc.)
- **Event-Driven**: Async communication via REST APIs and Cloud Pub/Sub
- **AI-First**: Every feature leverages AI for intelligent automation

### Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS, React Query |
| **AI/ML Services** | Python 3.11+, LangChain, LangGraph, FastAPI |
| **Core Services** | Go 1.21+, Gin framework, GORM |
| **Data Layer** | PostgreSQL, Redis, Vector Databases |
| **Infrastructure** | Kubernetes (GKE), Docker, Terraform |
| **AI Technologies** | LangChain, LangGraph, RAG, Multi-agent systems |

## 📁 Repository Structure

```
intelligence-crm/
├── .claude/                    # Claude Code Spec Framework
│   ├── commands/              # Custom workflow commands
│   ├── specs/                 # Feature specifications
│   ├── steering/              # Project context documents
│   ├── templates/             # Document templates
│   └── agents/                # Validation agents
├── services/                  # Microservices (Backend)
│   ├── crm-core/             # Core CRM functionality (Python/FastAPI)
│   ├── user-management/       # Authentication & authorization (Python/FastAPI)
│   ├── ai-orchestration/      # LangChain AI services (Python)
│   ├── workflow-engine/       # Business process automation (Python)
│   ├── analytics-service/     # Real-time analytics (Python/FastAPI)
│   └── communication-hub/     # Multi-channel communication (Python)
├── frontend/                  # Web application (Next.js/TypeScript)
├── app/                       # Shared workflow engine components
├── docs/                      # Project documentation
└── infrastructure/            # Infrastructure as Code (Terraform)
```

## 🚀 Services Architecture

### 1. CRM Core Service (Port 8001)
- **Technology**: Python + FastAPI + SQLAlchemy
- **Purpose**: Core CRM functionality, customer data management
- **Key Features**: Contact management, interaction tracking, data persistence
- **Database**: PostgreSQL with multi-tenant isolation

### 2. User Management Service (Port 8002)
- **Technology**: Python + FastAPI + GORM
- **Purpose**: Authentication, authorization, user profiles
- **Key Features**: JWT tokens, RBAC, multi-tenant security
- **Database**: PostgreSQL with Redis caching

### 3. AI Orchestration Service (Port 8004)
- **Technology**: Python + LangChain + LangGraph
- **Purpose**: AI/ML coordination, intelligent automation
- **Key Features**: LLM orchestration, multi-agent workflows, RAG
- **Integration**: Vector databases, OpenAI/Claude APIs

### 4. Workflow Engine Service (Port 8003)
- **Technology**: Python + LangGraph + FastAPI
- **Purpose**: Business process automation, decision trees
- **Key Features**: Visual workflow builder, event-driven processing
- **Integration**: LangChain for AI-powered workflows

### 5. Analytics Service (Port 8000)
- **Technology**: Python + FastAPI + SQLAlchemy
- **Purpose**: Real-time analytics, metrics, reporting
- **Key Features**: Dashboard KPIs, performance monitoring
- **Database**: PostgreSQL + Redis for caching

### 6. Communication Hub Service
- **Technology**: Python + FastAPI + WebSockets
- **Purpose**: Multi-channel communication management
- **Key Features**: Email, SMS, social media integration
- **Integration**: Google Cloud services (PubSub, Translation)

### 7. Frontend Application (Port 3000)
- **Technology**: Next.js 14 + TypeScript + Tailwind CSS
- **Purpose**: User interface, dashboard, workflow management
- **Key Features**: Responsive UI, real-time updates, analytics views
- **Integration**: All backend services via REST APIs

## 🤖 Claude Code Spec Framework

This project uses a sophisticated **specification-driven development system** for managing features and tasks:

### Framework Components
- **Steering Documents**: Project context (product.md, tech.md, structure.md)
- **Specifications**: Feature requirements and design documents
- **Task Breakdown**: Atomic tasks (15-30 minutes, 1-3 files max)
- **Validation Agents**: Automated validation of specifications and tasks
- **Custom Commands**: Workflow automation commands

### Development Workflow
1. **Requirements Phase**: Create user stories and acceptance criteria
2. **Design Phase**: Architecture and technical design
3. **Tasks Phase**: Break down into atomic implementation tasks
4. **Implementation Phase**: Execute individual tasks with validation

### Available Commands
```bash
# Core workflow commands
/spec-create <feature-name>          # Create new feature specification
/spec-execute <feature-name> <task>  # Execute individual tasks
/spec-status <feature-name>          # Monitor progress
/spec-list                          # List all specifications

# Bug management
/bug-create <bug-name>              # Create bug report
/bug-analyze <bug-name>             # Analyze bug
/bug-fix <bug-name>                 # Fix bug
```

## 🔧 Development Environment

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- Git
- Google Cloud Platform account

### Quick Start
1. **Clone and Setup**:
   ```bash
   git clone https://github.com/danhngo/intelligence-crm.git
   cd intelligence-crm
   ```

2. **Environment Configuration**:
   ```bash
   # Copy environment files
   cp .env.example .env
   cp services/*/example.env services/*/.env
   # Edit configuration files
   ```

3. **Start Services**:
   ```bash
   # Individual services
   cd services/crm-core && docker-compose up -d
   cd services/user-management && docker-compose up -d
   cd services/analytics-service && docker-compose up -d
   
   # Frontend
   cd frontend && npm install && npm run dev
   ```

4. **Access Applications**:
   - Frontend: http://localhost:3000
   - CRM Core API: http://localhost:8001/docs
   - User Management API: http://localhost:8002/docs
   - Analytics API: http://localhost:8000/docs

## 📊 Key Features

### 1. Multi-Tenant Architecture
- **Tenant Isolation**: Strict data separation between organizations
- **Security**: Row-level security with automatic tenant filtering
- **Scalability**: Horizontal scaling per tenant

### 2. AI-Powered Intelligence
- **Lead Scoring**: ML algorithms for prospect qualification
- **Workflow Automation**: LangGraph-powered decision trees
- **Customer Insights**: RAG-based analytics and recommendations
- **Multi-Agent Systems**: Coordinated AI agents for complex tasks

### 3. Real-Time Communication
- **WebSocket Support**: Live updates and notifications
- **Multi-Channel**: Email, SMS, social media integration
- **Event-Driven**: Async message processing

### 4. Comprehensive Analytics
- **Real-Time Dashboards**: Live metrics and KPIs
- **Custom Reports**: Flexible reporting engine
- **Performance Monitoring**: System and business metrics

## 🧪 Testing Strategy

### Unit Testing
- **Coverage Target**: 90%+ for service and repository layers
- **Frameworks**: pytest (Python), Jest/React Testing Library (Frontend)
- **Mocking**: testify/mock for external dependencies

### Integration Testing
- **Database Testing**: testcontainers for PostgreSQL
- **API Testing**: Complete request/response cycles
- **Service Integration**: gRPC/REST communication testing

### End-to-End Testing
- **User Journeys**: Complete authentication and CRM workflows
- **Multi-Tenant**: Data isolation verification
- **Performance**: Load testing with concurrent users

## 🔐 Security Features

- **Authentication**: JWT-based with refresh tokens
- **Authorization**: Role-based access control (RBAC)
- **Multi-Tenancy**: Row-level security and data isolation
- **API Security**: Rate limiting, CORS, trusted hosts
- **Audit Logging**: Comprehensive security event tracking

## 📈 Performance Targets

- **Response Time**: Sub-2-second for 95% of requests
- **Uptime**: 99.9% system availability
- **Concurrent Users**: 10,000+ simultaneous users
- **Scalability**: Auto-scaling without performance degradation

## 🚀 Deployment Options

### Development
```bash
docker-compose up -d  # Local development environment
```

### Production
- **Kubernetes (GKE)**: Container orchestration
- **Terraform**: Infrastructure as Code
- **Helm Charts**: Templated deployments
- **CI/CD**: Automated testing and deployment

## 📚 Learning Objectives

This codebase serves as a comprehensive learning platform for:

1. **Microservices Architecture**: Domain-driven design patterns
2. **AI/ML Integration**: LangChain, LangGraph, RAG implementations
3. **Cloud-Native Development**: Kubernetes, serverless, monitoring
4. **Modern Frontend**: React, TypeScript, state management
5. **Database Design**: Multi-tenancy, performance optimization
6. **DevOps Practices**: CI/CD, Infrastructure as Code, monitoring

## 🛠️ Common Development Tasks

### Adding a New Feature
1. Use `/spec-create <feature-name>` to create specification
2. Define requirements and design through validation agents
3. Break down into atomic tasks
4. Execute tasks using `/spec-execute <feature-name> <task-id>`

### Adding a New Service
1. Follow existing service structure patterns
2. Implement health checks and observability
3. Add Docker configuration and Kubernetes manifests
4. Update API gateway routing

### Database Changes
1. Create migrations using Alembic (Python services)
2. Update models with proper typing and validation
3. Add repository layer methods
4. Update API schemas and endpoints

## 🎯 Next Steps for Understanding

1. **Explore Service Code**: Start with `services/crm-core/app/main.py`
2. **Run a Service**: Try `cd services/crm-core && docker-compose up`
3. **Check API Docs**: Visit service `/docs` endpoints
4. **Try Claude Commands**: Use `/spec-list` to see specifications
5. **Review Tests**: Look at existing test patterns
6. **Explore Frontend**: Check `frontend/src` directory structure

This codebase represents a production-ready, AI-powered CRM platform that demonstrates modern development practices while serving as an excellent learning resource for advanced AI and cloud-native technologies.