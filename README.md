# Intelligence CRM Platform

A comprehensive microservices-based CRM platform built with LangChain, FastAPI, Next.js, and modern cloud-native technologies.

## � Platform Components

- **🌐 Modern TypeScript Frontend** - Next.js 14 web application with beautiful UI
- **⚡ High-Performance Backend** - FastAPI microservices architecture
- **🤖 AI-Powered Intelligence** - LangChain integration for smart automation
- **📊 Real-time Analytics** - Comprehensive metrics and reporting
- **🔄 Workflow Automation** - Visual workflow designer and execution engine

## �🏗️ Architecture Overview

This platform consists of a modern frontend and multiple backend microservices that work together to provide a complete CRM solution:

### Frontend Application

**🌐 Intelligence CRM Frontend** (Port 3000)
- Next.js 14 with TypeScript
- Modern responsive UI with Tailwind CSS  
- Real-time dashboard with metrics
- Contact management interface
- User authentication and authorization
- Analytics and reporting views
- Workflow management interface

### Backend Services

1. **CRM Core Service** (Port 8001)
   - Core CRM functionality
   - Customer data management
   - Contact management
   - Integration orchestration

2. **User Management Service** (Port 8002)
   - Authentication & authorization
   - User profile management
   - Role-based access control
   - JWT token management

3. **Workflow Engine Service** (Port 8003)
   - Business process automation
   - LangChain workflow orchestration
   - Decision trees and state management
   - Event-driven processing

4. **Communication Hub Service**
   - Multi-channel communication
   - Message routing and processing
   - WebSocket real-time communication
   - Google Cloud integration (PubSub, Translation, Speech)

5. **Analytics Service** (Port 8000)
   - Real-time analytics and metrics
   - Message and conversation analytics
   - Dashboard KPIs
   - Performance monitoring

6. **AI Orchestration Service** (Port 8004)
   - LangChain agent coordination
   - Multi-agent workflows
   - Prompt management
   - Memory and context management

## 🚀 Technology Stack

### Frontend Technologies
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **React Query** - Server state management
- **Framer Motion** - Animation library
- **Heroicons** - Beautiful SVG icons

### Backend Technologies
- **Python 3.11** - Main programming language
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - Async ORM with type hints
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI web server

### AI/ML Components
- **LangChain** - AI/ML orchestration framework
- **LangGraph** - Workflow management and agent coordination
- **Vector Databases** - Semantic search capabilities
- **OpenAI/Claude Integration** - LLM integration

### Data Storage
- **PostgreSQL** - Primary relational database
- **Redis** - Caching and session management
- **Google Cloud Storage** - File and media storage

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Health Checks** - Service monitoring
- **Network Isolation** - Service security

### External Integrations
- **Google Cloud Services**:
  - PubSub for message queuing
  - Translation API
  - Speech-to-Text API
  - Natural Language API
- **Multi-channel Communication**:
  - Email (SMTP/API)
  - SMS integration
  - Social media APIs
  - WebSocket real-time chat

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Git
- Google Cloud Platform account (for cloud services)

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/danhngo/intelligence-crm.git
   cd intelligence-crm
   ```

2. **Set up environment variables**:
   ```bash
   # Copy environment files for each service
   cp services/crm-core/.env.example services/crm-core/.env
   cp services/user-management/.env.example services/user-management/.env
   cp services/workflow-engine/.env.example services/workflow-engine/.env
   cp services/analytics-service/.env.example services/analytics-service/.env
   # Edit each .env file with your configuration
   ```

3. **Start the platform**:
   ```bash
   # Start all services
   docker-compose up -d
   
   # Or start individual services
   cd services/crm-core && docker-compose up -d
   cd services/user-management && docker-compose up -d
   cd services/analytics-service && docker-compose up -d
   ```

4. **Start the frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the platform**:
   - **🌐 Frontend Application**: http://localhost:3000
   - Analytics API: http://localhost:8000/docs
   - CRM Core API: http://localhost:8001/docs  
   - User Management API: http://localhost:8002/docs
   - Workflow Engine API: http://localhost:8003/docs
   - AI Orchestration API: http://localhost:8004/docs

## 🏛️ Service Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CRM Core      │    │ User Management │    │ Workflow Engine │
│   :8000         │◄──►│   :8002         │◄──►│   :8001         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────┬─────▼─────┬─────────────────┐
         │                 │           │                 │
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Communication   │ │   Analytics     │ │ AI Orchestration│
│ Hub             │ │   Service       │ │   Service       │
│                 │ │   :8004         │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## 🔧 Development

### Running Tests
```bash
# Run tests for all services
./scripts/run-tests.sh

# Or run tests for individual services
cd services/analytics-service && pytest
```

### Code Quality
```bash
# Format code
black services/*/app/
isort services/*/app/

# Lint code
flake8 services/*/app/
```

### Database Migrations
```bash
# Run migrations for each service
cd services/crm-core && alembic upgrade head
cd services/user-management && alembic upgrade head
cd services/analytics-service && alembic upgrade head
```

## 📊 Key Features

### 1. Multi-Tenant Architecture
- Tenant isolation at data and service levels
- Configurable tenant settings
- Scalable multi-tenancy support

### 2. Real-Time Communication
- WebSocket support for real-time updates
- Multi-channel message routing
- Event-driven architecture

### 3. AI-Powered Workflows
- LangChain integration for intelligent automation
- Custom agent development
- Prompt engineering and management

### 4. Comprehensive Analytics
- Real-time metrics and KPIs
- Message sentiment analysis
- Performance monitoring
- Custom dashboard creation

### 5. Scalable Microservices
- Independent service deployment
- Health monitoring
- Auto-scaling capabilities

## 🔐 Security

- JWT-based authentication
- Role-based access control (RBAC)
- API rate limiting
- Secure inter-service communication
- Environment-based configuration

## 📈 Monitoring & Observability

- Health check endpoints for all services
- Structured logging with correlation IDs
- Metrics collection and aggregation
- Error tracking and alerting

## 🚀 Deployment

### Docker Compose (Development)
```bash
docker-compose up -d
```

### Kubernetes (Production)
```bash
kubectl apply -f k8s/
```

### Cloud Deployment
- Google Cloud Platform ready
- Azure deployment support
- AWS compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue in this repository
- Check the documentation in each service's README
- Review the API documentation at `/docs` endpoints

## 🎯 Roadmap

- [ ] Advanced AI agent capabilities
- [ ] Enhanced analytics and reporting
- [ ] Mobile app support
- [ ] Advanced workflow designer UI
- [ ] Kubernetes operator
- [ ] Multi-cloud deployment
- [ ] Advanced security features
- [ ] Performance optimizations
