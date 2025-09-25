# crm-core-services - Task 49

Execute task 49 for the crm-core-services specification.

## Task Description
Create HTTP server for CRM Management Service

## Code Reuse
**Leverage existing code**: Gin framework, gRPC client integration, middleware

## Requirements Reference
**Requirements**: 7.1, 7.4

## Usage
```
/Task:49-crm-core-services
```

## Instructions

Execute with @spec-task-executor agent the following task: "Create HTTP server for CRM Management Service"

```
Use the @spec-task-executor agent to implement task 49: "Create HTTP server for CRM Management Service" for the crm-core-services specification and include all the below context.

# Steering Context
## Steering Documents Context (Pre-loaded)

### Product Context
# Product Overview

## Product Purpose
Build an intelligent CRM and automated workflows platform specifically designed for the marketing industry, targeting small and medium businesses (SMBs). The platform democratizes enterprise-level AI capabilities, enabling SMBs to compete with larger enterprises through AI-powered customer relationship management, lead scoring, workflow automation, and intelligent insights. This project serves dual objectives: creating a market-ready SaaS solution while providing hands-on learning experience with cutting-edge AI technologies including LangChain, LangGraph, and agentic development workflows.

## Target Users
**Primary Users**: Marketing professionals, sales managers, and business owners at SMBs in the marketing industry

**User Needs and Pain Points**:
- Limited resources to implement complex CRM systems
- Difficulty competing with larger companies using advanced AI tools
- Manual processes for lead qualification and customer communication
- Lack of actionable insights from customer data
- Need for affordable, scalable solutions that grow with their business
- Desire for automation without losing personal touch in customer relationships

## Key Features

1. **Core CRM Management**: Comprehensive contact management with interaction tracking, timeline views, and automated follow-up recommendations
2. **AI-Powered Lead Scoring**: Intelligent prospect qualification using machine learning algorithms with continuous improvement
3. **Intelligent Workflow Automation**: LangGraph-powered visual workflow builder with AI decision points and multi-channel triggers
4. **Agentic RAG Customer Insights**: AI-driven customer analytics providing actionable recommendations and predictive insights
5. **Multi-Channel Communication Hub**: Unified platform for email, SMS, social media, and other communication channels
6. **Advanced Analytics and Reporting**: Real-time dashboards with AI-generated insights, custom reports, and performance tracking
7. **User Management and Security**: Role-based access control with enterprise-grade security and compliance features

## Business Objectives

**Primary Objectives**:
- Create a production-ready SaaS platform serving SMBs in the marketing industry
- Achieve product-market fit with cost-effective pricing suitable for SMB budgets
- Build a scalable, reliable platform capable of handling 10,000+ concurrent users
- Generate sustainable revenue through subscription-based SaaS model

**Learning Objectives**:
- Master advanced AI technologies through practical implementation
- Gain expertise in LLM orchestration, vector databases, and inference infrastructure
- Develop proficiency in agentic workflows and multi-agent systems
- Learn modern cloud-native architecture patterns and microservices design

## Success Metrics

**Performance Metrics**:
- **Response Time**: Sub-2-second response times for 95% of requests
- **Uptime**: 99.9% system availability
- **Concurrent Users**: Support for 10,000+ simultaneous users
- **Scalability**: Auto-scaling to handle traffic spikes without degradation

**Business Metrics**:
- **Customer Acquisition**: Target 100+ SMB customers within first year
- **Customer Retention**: 85%+ monthly retention rate
- **Cost Efficiency**: Maintain operational costs under 30% of revenue
- **Feature Adoption**: 70%+ active usage of core AI features

**Learning Metrics**:
- **Technology Mastery**: Successful implementation of all planned AI technologies
- **Code Quality**: 90%+ test coverage with comprehensive validation
- **Architecture Patterns**: Implement production-ready microservices architecture
- **Performance Optimization**: Meet all specified performance benchmarks

## Product Principles

1. **AI-First Design**: Every feature should leverage AI to provide intelligent automation and insights, not just basic functionality
2. **SMB-Centric Approach**: Design for resource-constrained businesses with simple interfaces, affordable pricing, and quick time-to-value
3. **Scalable Architecture**: Build for growth with cloud-native patterns, microservices, and auto-scaling capabilities from day one
4. **Learning Through Building**: Balance practical business requirements with learning objectives, ensuring both goals are achieved
5. **Security and Compliance**: Implement enterprise-grade security suitable for handling sensitive customer data with full compliance
6. **Cost Efficiency**: Optimize for operational costs to maintain sustainable pricing for SMB market

## Monitoring & Visibility

**Dashboard Type**: Web-based admin dashboard with mobile-responsive design
**Real-time Updates**: WebSocket connections for live updates on workflows, lead scoring, and system performance
**Key Metrics Displayed**:
- System performance (response times, uptime, error rates)
- Business metrics (lead conversion, workflow completion, user engagement)
- AI model performance (scoring accuracy, recommendation effectiveness)
- Resource utilization and cost optimization opportunities

**Sharing Capabilities**:
- Read-only dashboard sharing for stakeholders
- Automated report generation and email delivery
- API access for custom integrations and third-party tools
- Export capabilities for compliance and audit requirements

## Future Vision

The platform will evolve into a comprehensive marketing intelligence suite that serves as the central nervous system for SMB marketing operations.

### Potential Enhancements

**Advanced AI Capabilities**:
- Multi-modal AI supporting voice, image, and video content analysis
- Predictive analytics for market trends and customer behavior
- Advanced personalization engines for hyper-targeted campaigns
- Integration with emerging AI models and technologies

**Platform Expansion**:
- Industry-specific modules beyond marketing (sales, customer success, finance)
- Integration marketplace with hundreds of third-party tools
- Advanced workflow templates and industry-specific best practices
- White-label solutions for agencies and consultants

**Collaboration Features**:
- Team collaboration tools with role-based permissions
- Customer portal for direct interaction and feedback
- Partner ecosystem for integrators and developers
- Community features for knowledge sharing and best practices

**Global Reach**:
- Multi-language support for international markets
- Regional compliance and data residency options
- Localized features for different business cultures
- Currency and tax handling for global operations

---

### Technology Context
# Technology Stack

## Project Type
Cloud-native SaaS platform built as a microservices architecture, comprising a TypeScript/React web application frontend, Python AI/ML services, Go core services, and comprehensive Google Cloud Platform infrastructure. The platform serves as both a production-ready intelligent CRM solution and a learning environment for advanced AI technologies.

## Core Technologies

### Primary Language(s)
- **Frontend**: TypeScript 5.x with React 18.x and modern ES2022+ features
- **AI/ML Services**: Python 3.11+ with async/await patterns and type hints
- **Core Services**: Go 1.21+ for high-performance, low-latency operations
- **Infrastructure**: HCL (Terraform) for Infrastructure as Code
- **Configuration**: YAML for Kubernetes manifests and service configuration

### Key Dependencies/Libraries

**AI/ML Stack**:
- **LangChain**: LLM orchestration, prompt templates, memory management, and tool integration
- **LangGraph**: Complex workflow orchestration, decision trees, and multi-agent coordination
- **LangSmith**: LLM application observability and debugging
- **Pydantic**: Data validation and serialization with automatic API documentation
- **FastAPI**: High-performance async web framework with OpenAPI integration
- **scikit-learn**: Machine learning algorithms for lead scoring and analytics

**Frontend Technologies**:
- **React**: Component-based UI with hooks and suspense for async operations
- **Material-UI (MUI)**: Enterprise-ready component library with theming support
- **Redux Toolkit**: Predictable state management with RTK Query for API integration
- **React Query**: Server state management and caching for optimal performance
- **TypeScript**: Static typing for enhanced developer experience and code quality

**Backend Services (Go)**:
- **Gin**: High-performance HTTP web framework with middleware support
- **GORM**: ORM for database operations with migration support
- **Go-Redis**: Redis client for caching and session management
- **Testify**: Testing framework with assertions and mocking capabilities

**Infrastructure & DevOps**:
- **Kubernetes (GKE)**: Container orchestration with auto-scaling and load balancing
- **Docker**: Containerization with multi-stage builds for optimized images
- **Terraform**: Infrastructure as Code for reproducible deployments
- **Helm**: Kubernetes package manager for templated deployments

### Application Architecture
Microservices architecture following domain-driven design principles with event-driven communication patterns. The system comprises six core services communicating through REST APIs, GraphQL, and asynchronous messaging via Cloud Pub/Sub. Each service is independently deployable, scalable, and maintainable.

**Service Boundaries**:
- CRM Management Service (Go)
- AI/ML Orchestration Service (Python)
- Workflow Engine Service (Python)
- Communication Hub Service (Go)
- Analytics Service (Python)
- User Management Service (Go)

### Data Storage
- **Primary Storage**: Cloud SQL (PostgreSQL 15+) for transactional data with read replicas
- **Document Store**: Firestore for real-time data and user preferences
- **Vector Database**: Pinecone or Google Cloud Vector Search for RAG implementations
- **Data Warehouse**: BigQuery for analytics, reporting, and machine learning workflows
- **Caching**: Redis (Cloud Memorystore) for session management and performance optimization
- **Object Storage**: Cloud Storage for file uploads, backups, and static assets
- **Data Formats**: JSON for API communication, Protocol Buffers for internal service communication

### External Integrations
- **Google Cloud Services**: Vertex AI for ML model serving, Cloud Pub/Sub for messaging, Cloud Monitoring for observability
- **Authentication**: Firebase Auth with OAuth2/OIDC for social login and enterprise SSO
- **Communication APIs**: SendGrid (email), Twilio (SMS), Slack/Teams APIs for notifications
- **CRM Integrations**: Salesforce, HubSpot, Pipedrive APIs for data import/export
- **Payment Processing**: Stripe for subscription management and billing
- **Protocols**: HTTP/REST, GraphQL, WebSocket for real-time updates, gRPC for inter-service communication

### Monitoring & Dashboard Technologies
- **Frontend Framework**: React with TypeScript and Material-UI for responsive design
- **Real-time Communication**: WebSocket connections for live updates, Server-Sent Events for notifications
- **Visualization Libraries**: Chart.js for business metrics, React virtualization for large datasets
- **State Management**: Redux Toolkit with RTK Query for optimistic updates and caching
- **Error Tracking**: Sentry for frontend and backend error monitoring with performance insights

## Development Environment

### Build & Development Tools
- **Build System**: Vite for frontend with HMR, Docker multi-stage builds for services
- **Package Management**: npm/pnpm for frontend, pip with Poetry for Python, Go modules for Go services
- **Development Workflow**: Hot reload for all services, Docker Compose for local development environment
- **API Documentation**: OpenAPI/Swagger with auto-generation from code annotations
- **Database Migrations**: Flyway for SQL migrations, GORM AutoMigrate for development

### Code Quality Tools
- **Static Analysis**: ESLint + Prettier (frontend), Black + Ruff (Python), golangci-lint (Go)
- **Type Checking**: TypeScript strict mode, mypy for Python, native Go type system
- **Testing Framework**: Jest + React Testing Library (frontend), pytest (Python), testify (Go)
- **API Testing**: Postman collections, automated integration tests with testcontainers
- **Security Scanning**: Snyk for dependency vulnerabilities, SonarQube for code quality

### Version Control & Collaboration
- **VCS**: Git with conventional commits for semantic versioning
- **Branching Strategy**: GitHub Flow with feature branches and pull request reviews
- **Code Review Process**: Required PR reviews with automated checks (tests, linting, security)
- **CI/CD**: Google Cloud Build with multi-stage pipelines for testing, building, and deployment

### Dashboard Development
- **Live Reload**: Vite HMR for instant feedback during development
- **Port Management**: Configurable ports for all services with Docker Compose port mapping
- **Multi-Instance Support**: Docker Compose profiles for running selective services during development

## Deployment & Distribution

- **Target Platform**: Google Cloud Platform with multi-region deployment capability
- **Distribution Method**: SaaS platform with web-based access, no client installation required
- **Deployment Strategy**: Blue-green deployments with canary releases for zero-downtime updates
- **Container Registry**: Google Container Registry with vulnerability scanning
- **Environment Management**: Separate GKE clusters for development, staging, and production

## Technical Requirements & Constraints

### Performance Requirements
- **Response Time**: Sub-2-second response times for 95% of user requests
- **Throughput**: Support 10,000+ concurrent users with horizontal auto-scaling
- **AI Processing**: ML inference within 2 seconds for lead scoring and recommendations
- **Database Performance**: Query response times under 100ms for typical operations
- **Frontend Performance**: Core Web Vitals compliance with LCP < 2.5s, FID < 100ms

### Compatibility Requirements
- **Browser Support**: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- **Mobile Responsiveness**: Full functionality on tablets and smartphones
- **API Versioning**: Semantic versioning with backward compatibility for 2 major versions
- **Database Compatibility**: PostgreSQL 13+ with read replica support

### Security & Compliance
- **Authentication**: Multi-factor authentication with OAuth2/OIDC integration
- **Data Encryption**: TLS 1.3 in transit, AES-256 at rest for all sensitive data
- **Compliance**: GDPR, CCPA, SOC 2 Type II compliance with audit trails
- **Access Control**: Role-based access control (RBAC) with principle of least privilege
- **API Security**: Rate limiting, input validation, SQL injection prevention, CORS configuration

### Scalability & Reliability
- **Expected Load**: Start with 100 SMB customers, scale to 10,000+ users within 2 years
- **Availability**: 99.9% uptime with automated failover and disaster recovery
- **Auto-scaling**: Kubernetes HPA based on CPU, memory, and custom metrics
- **Data Backup**: Automated daily backups with 30-day retention and point-in-time recovery

## Technical Decisions & Rationale

### Decision Log

1. **Microservices over Monolith**: Chosen for independent scaling, technology diversity (Python for AI, Go for performance), and team autonomy. Trade-off: Increased operational complexity managed through Kubernetes and service mesh.

2. **LangChain + LangGraph**: Selected for rapid AI development and workflow orchestration. Provides abstraction over LLM providers and enables complex multi-agent workflows essential for intelligent automation.

3. **TypeScript Frontend**: Ensures type safety and better developer experience. Material-UI chosen for enterprise-ready components and accessibility compliance required for SMB market.

4. **Google Cloud Platform**: Provides integrated AI services (Vertex AI), managed infrastructure, and compliance certifications needed for enterprise sales. Cost optimization through committed use discounts.

5. **PostgreSQL + Firestore Hybrid**: PostgreSQL for transactional consistency, Firestore for real-time features. Avoids vendor lock-in while leveraging Google Cloud's managed services.

6. **Go for Core Services**: Chosen for performance-critical operations like authentication and real-time messaging. Lower resource usage reduces operational costs for SMB-focused pricing model.

## Known Limitations

- **AI Model Dependencies**: Reliance on external LLM providers (OpenAI, Google) creates potential latency and cost concerns. Mitigation: Implement caching and consider on-premise models for future versions.

- **Multi-tenancy Complexity**: Current design uses shared databases with tenant isolation. Future consideration: Move to database-per-tenant for larger customers requiring data residency.

- **Real-time Scaling**: WebSocket connections require sticky sessions, limiting horizontal scaling. Future solution: Implement Redis-based session sharing or move to serverless WebSocket solutions.

- **Development Environment Complexity**: Multiple services require significant local resources. Mitigation: Provide cloud-based development environments and selective service startup options.

- **AI Model Versioning**: No current strategy for AI model versioning and A/B testing. Future implementation: MLOps pipeline with model experiment tracking and gradual rollouts.

---

### Structure Context
# Project Structure

## Directory Organization

```
claude-code-langchain/
├── .claude/                     # Spec framework configuration
│   ├── agents/                  # Validation agents
│   ├── commands/                # Custom commands
│   ├── specs/                   # Feature specifications
│   ├── bugs/                    # Bug tracking
│   ├── steering/                # Project context documents
│   └── templates/               # Document templates
├── services/                    # Microservices
│   ├── crm-management/          # CRM core service (Go)
│   │   ├── cmd/                 # Service entry points
│   │   ├── internal/            # Private application logic
│   │   │   ├── handlers/        # HTTP handlers
│   │   │   ├── services/        # Business logic
│   │   │   ├── models/          # Data models
│   │   │   └── repository/      # Data access layer
│   │   ├── pkg/                 # Public packages
│   │   ├── migrations/          # Database migrations
│   │   └── Dockerfile          # Container configuration
│   ├── ai-orchestration/        # AI/ML service (Python)
│   │   ├── app/                 # Application code
│   │   │   ├── api/             # API endpoints
│   │   │   ├── core/            # Business logic
│   │   │   ├── models/          # Data models
│   │   │   ├── services/        # Service layer
│   │   │   └── utils/           # Utilities
│   │   ├── langchain_workflows/ # LangChain integrations
│   │   ├── requirements.txt     # Python dependencies
│   │   └── Dockerfile          # Container configuration
│   ├── workflow-engine/         # Workflow service (Python)
│   ├── communication-hub/       # Communication service (Go)
│   ├── analytics-service/       # Analytics service (Python)
│   └── user-management/         # Auth service (Go)
├── frontend/                    # React TypeScript application
│   ├── src/                     # Source code
│   │   ├── components/          # Reusable UI components
│   │   │   ├── common/          # Generic components
│   │   │   ├── crm/             # CRM-specific components
│   │   │   ├── workflows/       # Workflow components
│   │   │   └── analytics/       # Analytics components
│   │   ├── pages/               # Page components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── services/            # API client services
│   │   ├── store/               # Redux store configuration
│   │   ├── types/               # TypeScript type definitions
│   │   └── utils/               # Utility functions
│   ├── public/                  # Static assets
│   ├── package.json             # Dependencies
│   └── Dockerfile              # Container configuration
├── infrastructure/              # Infrastructure as Code
│   ├── terraform/               # Terraform configurations
│   │   ├── environments/        # Per-environment configs
│   │   │   ├── dev/
│   │   │   ├── staging/
│   │   │   └── prod/
│   │   ├── modules/             # Reusable Terraform modules
│   │   └── shared/              # Shared resources
│   ├── kubernetes/              # Kubernetes manifests
│   │   ├── base/                # Base configurations
│   │   ├── overlays/            # Environment-specific overlays
│   │   └── helm-charts/         # Helm chart definitions
│   └── scripts/                 # Deployment and utility scripts
├── shared/                      # Shared code and definitions
│   ├── proto/                   # Protocol buffer definitions
│   ├── types/                   # Shared type definitions
│   └── configs/                 # Shared configuration files
├── docs/                        # Project documentation
│   ├── api/                     # API documentation
│   ├── architecture/            # Architecture diagrams and docs
│   ├── deployment/              # Deployment guides
│   └── user-guides/             # End-user documentation
├── tests/                       # Integration and E2E tests
│   ├── e2e/                     # End-to-end tests
│   ├── integration/             # Integration tests
│   └── load/                    # Performance/load tests
├── docker-compose.yml           # Local development environment
├── requirements.md              # Generated requirements document
├── design.md                    # Generated design document
└── spec.md                     # Original project specification
```

## Naming Conventions

### Files and Directories
- **Services**: `kebab-case` for service directories (e.g., `crm-management`, `ai-orchestration`)
- **Go packages**: `lowercase` single words or `snake_case` (e.g., `handlers`, `user_service`)
- **Python modules**: `snake_case` (e.g., `langchain_workflows`, `api_client`)
- **TypeScript components**: `PascalCase` (e.g., `ContactForm.tsx`, `DashboardWidget.tsx`)
- **Configuration files**: `kebab-case` (e.g., `docker-compose.yml`, `api-gateway.yaml`)
- **Tests**: `[filename]_test.go` (Go), `test_[filename].py` (Python), `[filename].test.ts` (TypeScript)

### Code Naming
- **Go**:
  - Types/Structs: `PascalCase` (e.g., `ContactService`, `UserRepository`)
  - Functions/Methods: `PascalCase` for public, `camelCase` for private
  - Constants: `PascalCase` or `UPPER_SNAKE_CASE` for package-level constants
  - Variables: `camelCase`
- **Python**:
  - Classes: `PascalCase` (e.g., `AIOrchestrator`, `WorkflowEngine`)
  - Functions/Methods: `snake_case` (e.g., `process_lead`, `generate_insights`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT`)
  - Variables: `snake_case`
- **TypeScript**:
  - Interfaces/Types: `PascalCase` (e.g., `ContactData`, `APIResponse`)
  - Functions/Methods: `camelCase` (e.g., `handleSubmit`, `fetchContacts`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `API_BASE_URL`, `MAX_FILE_SIZE`)
  - Variables: `camelCase`

## Import Patterns

### Import Order (TypeScript/JavaScript)
1. React and React-related imports
2. External library imports (alphabetical)
3. Internal shared utilities and types
4. Relative imports from same feature
5. CSS/style imports

```typescript
import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Box, Typography, Button } from '@mui/material';

import { apiClient } from '@/services/api';
import { ContactData, APIResponse } from '@/types/crm';
import { formatDate, validateEmail } from '@/utils/common';

import { ContactFormProps } from './types';
import './ContactForm.css';
```

### Import Order (Python)
1. Standard library imports
2. Third-party library imports
3. Local application imports
4. Relative imports

```python
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from langchain.llms import OpenAI
from pydantic import BaseModel

from app.core.config import settings
from app.models.contact import Contact
from app.services.crm_service import CRMService

from .schemas import ContactCreate, ContactResponse
```

### Import Order (Go)
1. Standard library imports
2. Third-party imports
3. Local package imports

```go
import (
    "context"
    "fmt"
    "net/http"
    "time"

    "github.com/gin-gonic/gin"
    "github.com/google/uuid"
    "gorm.io/gorm"

    "github.com/your-org/crm-management/internal/models"
    "github.com/your-org/crm-management/internal/services"
    "github.com/your-org/crm-management/pkg/logger"
)
```

## Code Structure Patterns

### Microservice Organization (Go)
```go
// internal/handlers/contact_handler.go
package handlers

// 1. Imports and dependencies
// 2. Handler struct definition
// 3. Constructor function
// 4. HTTP handler methods
// 5. Helper/validation functions
// 6. Error handling utilities
```

### Service Layer Organization (Python)
```python
# app/services/ai_orchestration_service.py

# 1. Imports and type definitions
# 2. Service class definition
# 3. Constructor and dependency injection
# 4. Public interface methods
# 5. Private helper methods
# 6. Error handling and logging
```

### React Component Organization (TypeScript)
```typescript
// src/components/crm/ContactForm.tsx

// 1. Imports (external, internal, types)
// 2. Interface/type definitions
// 3. Component definition with props
// 4. Custom hooks and state management
// 5. Event handlers and business logic
// 6. Render logic and JSX
// 7. Default export and named exports
```

## Code Organization Principles

1. **Domain-Driven Design**: Each microservice represents a clear business domain with well-defined boundaries
2. **Separation of Concerns**: Clear separation between API layer, business logic, and data access
3. **Dependency Injection**: Services receive dependencies through constructors for testability
4. **Single Responsibility**: Each module, class, and function has one clear purpose
5. **Interface Segregation**: Define focused interfaces rather than large, monolithic ones
6. **Error Handling**: Consistent error handling patterns across all services and layers

## Module Boundaries

### Service Communication
- **Public APIs**: Well-defined REST and GraphQL APIs for external communication
- **Internal Communication**: gRPC for high-performance inter-service communication
- **Event-Driven**: Use Cloud Pub/Sub for asynchronous, decoupled communication
- **Shared Types**: Protocol buffer definitions in `/shared/proto/` for type safety

### Dependency Direction
- **Frontend → Services**: Only through public APIs, never direct database access
- **Services → Shared**: Can depend on shared utilities and types
- **Services ↔ Services**: Only through public APIs, no direct dependencies
- **Infrastructure ← Services**: Services depend on infrastructure abstractions, not implementations

### Data Access Patterns
- **Repository Pattern**: Abstract data access behind interfaces for testability
- **Database per Service**: Each microservice owns its data and database schema
- **Event Sourcing**: Consider for audit trails and complex business workflows
- **Read Models**: Separate read and write models for optimal performance

## Code Size Guidelines

### File Size Limits
- **Go files**: Maximum 500 lines per file
- **Python files**: Maximum 400 lines per file
- **TypeScript files**: Maximum 300 lines per file (components), 500 lines (utilities)
- **Configuration files**: Keep focused and under 200 lines

### Function/Method Size
- **Functions**: Maximum 50 lines for complex business logic, 20 lines preferred
- **HTTP handlers**: Maximum 30 lines, delegate to service layer
- **React components**: Maximum 150 lines, extract custom hooks for complex logic
- **Database queries**: Use query builders or ORMs, avoid raw SQL over 10 lines

### Complexity Guidelines
- **Cyclomatic complexity**: Maximum 10 per function
- **Nesting depth**: Maximum 4 levels of nested blocks
- **Parameter count**: Maximum 5 parameters per function, use structs/objects for more

## API Design Structure

### RESTful Endpoint Organization
```
/api/v1/
├── /crm/
│   ├── /contacts/           # Contact management
│   ├── /interactions/       # Customer interactions
│   └── /leads/              # Lead management
├── /ai/
│   ├── /scoring/            # Lead scoring
│   ├── /insights/           # Customer insights
│   └── /workflows/          # AI workflow management
├── /communication/
│   ├── /email/              # Email integration
│   ├── /sms/                # SMS integration
│   └── /notifications/      # Push notifications
└── /analytics/
    ├── /reports/            # Custom reports
    ├── /dashboards/         # Dashboard data
    └── /metrics/            # Performance metrics
```

### GraphQL Schema Organization
- **Modular schemas**: Separate schema files per domain
- **Type composition**: Use interfaces and unions for flexibility
- **Query optimization**: Implement DataLoader pattern for N+1 prevention
- **Real-time subscriptions**: Use subscriptions for live updates

## Testing Structure

### Test Organization
```
tests/
├── unit/                    # Unit tests mirroring source structure
│   ├── services/
│   ├── handlers/
│   └── utils/
├── integration/             # Integration tests by feature
│   ├── crm/
│   ├── ai/
│   └── workflows/
├── e2e/                     # End-to-end user workflows
│   ├── user-journeys/
│   ├── api-workflows/
│   └── ui-scenarios/
└── performance/             # Load and performance tests
    ├── load-tests/
    └── stress-tests/
```

### Test Naming Conventions
- **Unit tests**: `Test[FunctionName]` (Go), `test_[function_name]` (Python), `[functionName].test.ts` (TypeScript)
- **Integration tests**: `Test[FeatureName]Integration`
- **E2E tests**: Descriptive names like `user_can_create_contact_and_send_email`

## Documentation Standards

- **API Documentation**: Auto-generated from OpenAPI specifications and GraphQL schemas
- **Code Documentation**: All public functions/methods must have documentation comments
- **Architecture Documentation**: Keep architectural decisions recorded in `/docs/architecture/`
- **Deployment Documentation**: Step-by-step guides in `/docs/deployment/`
- **README Files**: Each service must have a README with setup, build, and test instructions
- **Inline Comments**: Complex business logic should include explanatory comments

**Note**: Steering documents have been pre-loaded. Do not use get-content to fetch them again.

# Specification Context
## Specification Context (Pre-loaded): crm-core-services

### Requirements
# Requirements Document - CRM Core Services

## Introduction

The CRM Core Services specification defines the foundational microservices that form the backbone of the intelligent CRM platform. This includes the User Management Service and CRM Management Service, which provide essential user authentication, authorization, contact management, and interaction tracking capabilities. These services are built using Go for high-performance, low-latency operations and serve as the foundation upon which AI-powered features will be built.

The core services implement enterprise-grade security, scalability patterns, and cost-efficient architectures suitable for SMB customers while providing the technical foundation for learning advanced cloud-native development patterns.

## Alignment with Product Vision

This specification directly supports the product vision by:

- **SMB-Centric Foundation**: Establishing cost-efficient, scalable core services that can grow with SMB needs
- **Enterprise Security**: Implementing role-based access control and security features required for business data
- **Learning Platform**: Providing hands-on experience with Go microservices, Kubernetes, and cloud-native patterns
- **AI-Ready Architecture**: Creating data models and APIs that support future AI-powered features like lead scoring and workflow automation
- **Performance Focus**: Delivering sub-2-second response times and 10K+ concurrent user support from the foundation level

## Requirements

### Requirement 1: User Management and Authentication

**User Story:** As an SMB business owner, I want secure user authentication and role-based access control, so that I can safely manage team access to customer data and ensure compliance with data protection regulations.

#### Acceptance Criteria

1. WHEN a user registers with email/password THEN the system SHALL hash passwords using bcrypt and store securely in PostgreSQL
2. WHEN a user attempts login THEN the system SHALL validate credentials and return JWT tokens with 24-hour expiration
3. IF user credentials are invalid THEN the system SHALL return proper error response and log security events
4. WHEN JWT token expires THEN the system SHALL require re-authentication and refresh token flow
5. WHEN user updates profile information THEN the system SHALL validate changes and maintain audit trail

### Requirement 2: Role-Based Access Control (RBAC)

**User Story:** As a team manager, I want to assign different permission levels to team members, so that sensitive customer data is only accessible to authorized personnel.

#### Acceptance Criteria

1. WHEN admin creates user account THEN the system SHALL allow assignment of roles: Admin, Manager, Sales, Marketing
2. WHEN user attempts protected action THEN the system SHALL validate role permissions before proceeding
3. IF user lacks required permissions THEN the system SHALL deny access and return 403 Forbidden response
4. WHEN role permissions change THEN the system SHALL update user access immediately without requiring logout
5. WHEN viewing user list THEN admins SHALL see role assignments and permission levels

### Requirement 3: Core Contact Management

**User Story:** As a marketing professional, I want comprehensive contact management with search and organization capabilities, so that I can efficiently track and nurture customer relationships.

#### Acceptance Criteria

1. WHEN creating new contact THEN the system SHALL store name, email, phone, company, title, and custom fields in PostgreSQL
2. WHEN searching contacts THEN the system SHALL return results within 500ms using fuzzy matching on name, email, company
3. WHEN viewing contact details THEN the system SHALL display complete profile with interaction history and relationship data
4. IF contact data validation fails THEN the system SHALL return specific field errors and prevent incomplete saves
5. WHEN importing contact lists THEN the system SHALL process CSV files and handle duplicate detection/merging

### Requirement 4: Interaction Tracking and Timeline

**User Story:** As a sales representative, I want automatic tracking of customer interactions with timeline views, so that I can maintain context and provide personalized follow-ups.

#### Acceptance Criteria

1. WHEN customer interaction occurs THEN the system SHALL automatically log timestamp, type, channel, and context
2. WHEN viewing contact timeline THEN the system SHALL display chronological interaction history with filtering options
3. IF interaction data is incomplete THEN the system SHALL store partial data and flag for manual review
4. WHEN adding manual interaction notes THEN the system SHALL store rich text content with author attribution
5. WHEN generating interaction reports THEN the system SHALL provide metrics on frequency, outcomes, and next actions

### Requirement 5: Lead Management and Scoring Foundation

**User Story:** As a sales manager, I want lead status tracking and basic scoring capabilities, so that my team can prioritize high-value prospects effectively.

#### Acceptance Criteria

1. WHEN new lead enters system THEN the system SHALL assign status: New, Qualified, Nurturing, Converted, or Lost
2. WHEN lead status changes THEN the system SHALL log transition with timestamp and reason
3. IF lead has been inactive for 30+ days THEN the system SHALL flag for follow-up and notify assigned representative
4. WHEN viewing lead pipeline THEN the system SHALL display leads by status with conversion metrics
5. WHEN lead converts THEN the system SHALL automatically create customer record and update reporting metrics

### Requirement 6: Multi-tenant Data Isolation

**User Story:** As a SaaS platform operator, I want strict data isolation between customer organizations, so that each SMB client's data remains completely private and secure.

#### Acceptance Criteria

1. WHEN user authenticates THEN the system SHALL identify tenant organization and enforce data scope boundaries
2. WHEN querying data THEN the system SHALL automatically filter all results by tenant ID without manual specification
3. IF cross-tenant data access is attempted THEN the system SHALL block access and log security violation
4. WHEN creating new records THEN the system SHALL automatically assign current user's tenant ID
5. WHEN running background processes THEN the system SHALL process each tenant's data in complete isolation

### Requirement 7: API Gateway and Service Communication

**User Story:** As a platform developer, I want standardized API endpoints and inter-service communication, so that frontend applications and other services can reliably integrate with core CRM functionality.

#### Acceptance Criteria

1. WHEN external client calls API THEN the system SHALL authenticate JWT tokens and enforce rate limiting
2. WHEN service-to-service communication occurs THEN the system SHALL use gRPC with protocol buffer definitions
3. IF API rate limits are exceeded THEN the system SHALL return 429 Too Many Requests with retry-after headers
4. WHEN API errors occur THEN the system SHALL return consistent error format with correlation IDs for debugging
5. WHEN API documentation is accessed THEN the system SHALL provide up-to-date OpenAPI specifications with examples

## Non-Functional Requirements

### Performance
- **Response Time**: 95% of API requests complete within 500ms, 99% within 2 seconds
- **Throughput**: Support minimum 10,000 concurrent users with horizontal scaling
- **Database Performance**: Contact searches complete within 100ms with proper indexing
- **Memory Usage**: Each service instance uses maximum 512MB RAM under normal load
- **CPU Efficiency**: Maintain <70% CPU utilization under peak load with auto-scaling

### Security
- **Authentication**: JWT-based authentication with bcrypt password hashing (cost factor 12)
- **Data Encryption**: TLS 1.3 for all API communication, AES-256 encryption at rest
- **Access Control**: Role-based permissions with principle of least privilege
- **Audit Logging**: Complete audit trail for all user actions and data modifications
- **Vulnerability Management**: Regular security scanning and dependency updates

### Reliability
- **Availability**: 99.9% uptime with automated health checks and failover
- **Data Consistency**: ACID transactions for critical operations with proper rollback handling
- **Error Recovery**: Graceful degradation during service failures with circuit breaker patterns
- **Backup Strategy**: Automated daily backups with 30-day retention and point-in-time recovery
- **Monitoring**: Real-time monitoring with alerting for performance and error thresholds

### Usability
- **API Design**: RESTful APIs following OpenAPI 3.0 standards with clear documentation
- **Error Messages**: User-friendly error messages with actionable guidance
- **Response Format**: Consistent JSON response structure across all endpoints
- **Pagination**: Cursor-based pagination for large data sets with configurable page sizes
- **API Versioning**: Semantic versioning with backward compatibility for 2 major versions

### Scalability
- **Horizontal Scaling**: Kubernetes-based auto-scaling based on CPU and memory metrics
- **Database Scaling**: Read replica support with connection pooling for read-heavy operations
- **Caching Strategy**: Redis-based caching for frequently accessed data with TTL management
- **Load Balancing**: Layer 7 load balancing with health checks and session affinity where needed
- **Resource Optimization**: Efficient resource utilization with container resource limits and requests

### Compliance
- **Data Protection**: GDPR and CCPA compliance with data subject rights and consent management
- **SOC 2**: Type II compliance with security, availability, and confidentiality controls
- **Data Residency**: Support for regional data residency requirements where applicable
- **Retention Policies**: Configurable data retention with automated deletion of expired records
- **Privacy Controls**: User consent management and data portability features

---

### Design
# Design Document - CRM Core Services

## Overview

The CRM Core Services design implements two foundational microservices that form the backbone of the intelligent CRM platform: the User Management Service and CRM Management Service. Built with Go for high-performance operations, these services provide enterprise-grade authentication, authorization, contact management, and interaction tracking capabilities while maintaining cost-efficiency suitable for SMBs.

The design follows cloud-native patterns with Kubernetes deployment, implements multi-tenant data isolation, and provides AI-ready data models and APIs that support future machine learning integrations. The architecture emphasizes performance (sub-2-second response times), scalability (10K+ concurrent users), and security (SOC 2 compliance) while serving as a comprehensive learning platform for Go microservices development.

## Steering Document Alignment

### Technical Standards (tech.md)
The design strictly follows documented technical patterns:
- **Go Microservices**: Using Gin framework for HTTP APIs and GORM for database operations
- **Database Strategy**: PostgreSQL for transactional data with Redis caching layer
- **Authentication**: JWT-based authentication with bcrypt password hashing
- **Infrastructure**: Kubernetes deployment on Google Cloud Platform with auto-scaling
- **Communication**: REST APIs for external clients, gRPC for inter-service communication
- **Monitoring**: Cloud Monitoring integration with structured logging and metrics

### Project Structure (structure.md)
Implementation follows established project organization:
- **Service Organization**: Domain-driven design with clear service boundaries
- **Go Package Structure**: Standard layout with `cmd/`, `internal/`, and `pkg/` directories
- **Naming Conventions**: PascalCase for public types, camelCase for private functions
- **Import Patterns**: Standard library → Third-party → Local packages ordering
- **Testing Structure**: Comprehensive unit, integration, and E2E test organization

## Code Reuse Analysis

Since this is a greenfield implementation, the focus is on establishing foundational patterns and integrating with existing cloud infrastructure and established libraries.

### Existing Components to Leverage
- **Gin Framework**: High-performance HTTP router with middleware support for request handling
- **GORM**: Feature-rich ORM with automatic migrations, associations, and query optimization
- **Google Cloud SDK**: Native integration with GKE, Cloud SQL, Cloud Monitoring, and IAM
- **JWT-Go**: Robust JWT token generation and validation with proper security standards
- **Testify**: Comprehensive testing framework with assertions, mocking, and test suites
- **Viper**: Configuration management with environment variable and file support
- **Kubernetes Helm Charts**: Standard deployment patterns and configuration management

### Integration Points
- **Cloud SQL PostgreSQL**: Managed database service with automatic backups and read replicas
- **Cloud Memorystore Redis**: Managed Redis for caching and session storage
- **Google Cloud Monitoring**: Native observability with metrics, logging, and alerting
- **Cloud IAM**: Integration with Google Cloud identity and access management
- **Protocol Buffers**: Type-safe inter-service communication with generated Go structs

## Architecture

The system implements a clean microservices architecture with domain-driven design principles, ensuring each service has clear responsibilities and well-defined boundaries.

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Frontend]
        API[API Clients]
    end

    subgraph "API Gateway Layer"
        GATEWAY[API Gateway<br/>Nginx Ingress]
    end

    subgraph "Core Services"
        USER[User Management Service<br/>Go + Gin + GORM]
        CRM[CRM Management Service<br/>Go + Gin + GORM]
    end

    subgraph "Data Layer"
        POSTGRES[(PostgreSQL<br/>Cloud SQL)]
        REDIS[(Redis<br/>Memorystore)]
    end

    subgraph "Infrastructure"
        K8S[Kubernetes<br/>GKE Cluster]
        MONITOR[Cloud Monitoring]
    end

    WEB --> GATEWAY
    API --> GATEWAY
    GATEWAY --> USER
    GATEWAY --> CRM
    USER --> POSTGRES
    CRM --> POSTGRES
    USER --> REDIS
    CRM --> REDIS
    USER -.->|gRPC| CRM
    USER --> MONITOR
    CRM --> MONITOR
```

## Service Architecture Details

```mermaid
graph TD
    subgraph "User Management Service"
        AUTH[Authentication Handler]
        RBAC[RBAC Handler]
        USER_SVC[User Service Layer]
        USER_REPO[User Repository]
    end

    subgraph "CRM Management Service"
        CONTACT[Contact Handler]
        INTERACT[Interaction Handler]
        LEAD[Lead Handler]
        CRM_SVC[CRM Service Layer]
        CRM_REPO[CRM Repository]
    end

    subgraph "Data Models"
        USER_MODEL[User/Role Models]
        CONTACT_MODEL[Contact Models]
        INTERACTION_MODEL[Interaction Models]
        LEAD_MODEL[Lead Models]
    end

    AUTH --> USER_SVC
    RBAC --> USER_SVC
    USER_SVC --> USER_REPO
    USER_REPO --> USER_MODEL

    CONTACT --> CRM_SVC
    INTERACT --> CRM_SVC
    LEAD --> CRM_SVC
    CRM_SVC --> CRM_REPO
    CRM_REPO --> CONTACT_MODEL
    CRM_REPO --> INTERACTION_MODEL
    CRM_REPO --> LEAD_MODEL
```

## Components and Interfaces

### User Management Service

**Purpose:** Provides authentication, authorization, and user management capabilities with multi-tenant isolation.

**Interfaces:**
- `POST /api/v1/auth/login` - User authentication with JWT token generation
- `POST /api/v1/auth/register` - New user registration with role assignment
- `POST /api/v1/auth/refresh` - JWT token refresh with validation
- `GET /api/v1/users` - List users with role-based filtering
- `PUT /api/v1/users/{id}` - Update user profile with audit logging
- `POST /api/v1/users/{id}/roles` - Assign/modify user roles (admin only)
- gRPC `ValidateToken(token)` - Inter-service token validation
- gRPC `GetUserPermissions(userId)` - Role-based permission lookup

**Dependencies:**
- PostgreSQL for user data persistence
- Redis for session management and token blacklisting
- bcrypt for password hashing (cost factor 12)
- JWT-Go for token generation and validation

**Reuses:** Standard Gin middleware, GORM models, Cloud Monitoring integration patterns

### CRM Management Service

**Purpose:** Manages contacts, interactions, and leads with comprehensive search and timeline capabilities.

**Interfaces:**
- `GET /api/v1/contacts` - Search contacts with fuzzy matching and pagination
- `POST /api/v1/contacts` - Create new contact with validation and duplicate detection
- `GET /api/v1/contacts/{id}` - Retrieve contact details with interaction history
- `PUT /api/v1/contacts/{id}` - Update contact information with audit trail
- `POST /api/v1/contacts/import` - Bulk import contacts from CSV files
- `POST /api/v1/interactions` - Log customer interactions with timeline integration
- `GET /api/v1/interactions/{contactId}` - Retrieve interaction timeline with filtering
- `GET /api/v1/leads` - Lead pipeline view with status filtering and metrics
- `PUT /api/v1/leads/{id}/status` - Update lead status with transition logging
- gRPC `GetContactData(contactId)` - Inter-service contact data retrieval

**Dependencies:**
- PostgreSQL for CRM data with optimized indexes for search
- Redis for caching frequently accessed contact data
- User Management Service for authentication and authorization
- Full-text search capabilities using PostgreSQL extensions

**Reuses:** User Management Service authentication, standardized API response formats, pagination patterns

## Data Models

### User Management Models

```go
// User represents a system user with multi-tenant isolation
type User struct {
    ID          uuid.UUID  `gorm:"primaryKey;type:uuid;default:gen_random_uuid()" json:"id"`
    TenantID    uuid.UUID  `gorm:"not null;index" json:"tenant_id"`
    Email       string     `gorm:"uniqueIndex:idx_tenant_email;not null" json:"email"`
    PasswordHash string    `gorm:"not null" json:"-"`
    FirstName   string     `gorm:"not null" json:"first_name"`
    LastName    string     `gorm:"not null" json:"last_name"`
    Role        Role       `gorm:"not null" json:"role"`
    IsActive    bool       `gorm:"default:true" json:"is_active"`
    LastLoginAt *time.Time `json:"last_login_at"`
    CreatedAt   time.Time  `json:"created_at"`
    UpdatedAt   time.Time  `json:"updated_at"`
}

// Role defines user permission levels
type Role string

const (
    RoleAdmin     Role = "admin"
    RoleManager   Role = "manager"
    RoleSales     Role = "sales"
    RoleMarketing Role = "marketing"
)

// Permission represents granular permissions
type Permission struct {
    ID       uuid.UUID `gorm:"primaryKey;type:uuid;default:gen_random_uuid()"`
    Role     Role      `gorm:"not null;index"`
    Resource string    `gorm:"not null"`  // contacts, interactions, leads, users
    Action   string    `gorm:"not null"`  // create, read, update, delete
    Allowed  bool      `gorm:"not null"`
}
```

### CRM Management Models

```go
// Contact represents a customer contact with full profile information
type Contact struct {
    ID              uuid.UUID            `gorm:"primaryKey;type:uuid;default:gen_random_uuid()" json:"id"`
    TenantID        uuid.UUID            `gorm:"not null;index" json:"tenant_id"`
    Email           string               `gorm:"index:idx_tenant_email;not null" json:"email"`
    FirstName       string               `gorm:"not null" json:"first_name"`
    LastName        string               `gorm:"not null" json:"last_name"`
    Company         string               `gorm:"index:idx_tenant_company" json:"company"`
    Title           string               `json:"title"`
    Phone           string               `json:"phone"`
    Address         string               `json:"address"`
    CustomFields    datatypes.JSON       `json:"custom_fields"`
    Tags            pq.StringArray       `gorm:"type:text[]" json:"tags"`
    LeadScore       *int                 `gorm:"index" json:"lead_score"`
    Status          ContactStatus        `gorm:"default:'active'" json:"status"`
    Source          string               `json:"source"`          // web, import, api, referral
    AssignedUserID  *uuid.UUID           `gorm:"index" json:"assigned_user_id"`
    LastContactedAt *time.Time           `json:"last_contacted_at"`
    Interactions    []Interaction        `gorm:"foreignKey:ContactID" json:"interactions,omitempty"`
    CreatedAt       time.Time            `json:"created_at"`
    UpdatedAt       time.Time            `json:"updated_at"`
}

// Interaction represents customer interaction events
type Interaction struct {
    ID          uuid.UUID       `gorm:"primaryKey;type:uuid;default:gen_random_uuid()" json:"id"`
    TenantID    uuid.UUID       `gorm:"not null;index" json:"tenant_id"`
    ContactID   uuid.UUID       `gorm:"not null;index" json:"contact_id"`
    UserID      uuid.UUID       `gorm:"not null" json:"user_id"`
    Type        InteractionType `gorm:"not null" json:"type"`
    Channel     string          `gorm:"not null" json:"channel"`     // email, phone, meeting, chat
    Subject     string          `json:"subject"`
    Content     string          `json:"content"`
    Outcome     string          `json:"outcome"`                     // interested, not_interested, follow_up
    NextAction  string          `json:"next_action"`
    ScheduledAt *time.Time      `json:"scheduled_at"`
    CompletedAt *time.Time      `json:"completed_at"`
    CreatedAt   time.Time       `json:"created_at"`
    UpdatedAt   time.Time       `json:"updated_at"`
}

// Lead represents a sales lead with status tracking
type Lead struct {
    ID              uuid.UUID     `gorm:"primaryKey;type:uuid;default:gen_random_uuid()" json:"id"`
    TenantID        uuid.UUID     `gorm:"not null;index" json:"tenant_id"`
    ContactID       uuid.UUID     `gorm:"not null;index" json:"contact_id"`
    Status          LeadStatus    `gorm:"not null;index" json:"status"`
    Score           int           `gorm:"default:0" json:"score"`
    Value           *float64      `json:"value"`                 // estimated deal value
    Probability     *int          `json:"probability"`           // conversion probability %
    ExpectedCloseAt *time.Time    `json:"expected_close_at"`
    AssignedUserID  uuid.UUID     `gorm:"not null;index" json:"assigned_user_id"`
    Source          string        `json:"source"`
    Campaign        string        `json:"campaign"`
    StatusHistory   []LeadStatus  `gorm:"type:jsonb" json:"status_history"`
    CreatedAt       time.Time     `json:"created_at"`
    UpdatedAt       time.Time     `json:"updated_at"`
}

type ContactStatus string
type InteractionType string
type LeadStatus string

const (
    ContactActive   ContactStatus = "active"
    ContactInactive ContactStatus = "inactive"
    ContactArchived ContactStatus = "archived"

    InteractionCall     InteractionType = "call"
    InteractionEmail    InteractionType = "email"
    InteractionMeeting  InteractionType = "meeting"
    InteractionNote     InteractionType = "note"

    LeadNew        LeadStatus = "new"
    LeadQualified  LeadStatus = "qualified"
    LeadNurturing  LeadStatus = "nurturing"
    LeadConverted  LeadStatus = "converted"
    LeadLost       LeadStatus = "lost"
)
```

## API Design Specifications

### Authentication Flow
```
POST /api/v1/auth/login
{
  "email": "user@company.com",
  "password": "securePassword123"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@company.com",
    "first_name": "John",
    "last_name": "Smith",
    "role": "manager"
  }
}
```

### Contact Search API
```
GET /api/v1/contacts?search=john&company=acme&limit=20&cursor=abc123
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

Response: 200 OK
{
  "contacts": [...],
  "pagination": {
    "has_next": true,
    "next_cursor": "def456",
    "total_count": 150
  }
}
```

## Error Handling

### Error Scenarios and Responses

1. **Authentication Failure**
   - **Handling:** Return 401 with clear error message and security event logging
   - **User Impact:** Login form displays "Invalid credentials" with rate limiting after 5 attempts

2. **Authorization Failure**
   - **Handling:** Return 403 with permission details and audit logging
   - **User Impact:** Access denied message with explanation of required role/permission

3. **Validation Errors**
   - **Handling:** Return 400 with field-specific error details
   - **User Impact:** Form displays inline validation errors for each problematic field

4. **Rate Limiting**
   - **Handling:** Return 429 with retry-after header
   - **User Impact:** Temporary request throttling with clear retry guidance

5. **Database Connection Failures**
   - **Handling:** Circuit breaker pattern with fallback to cached data where possible
   - **User Impact:** Graceful degradation with notification of limited functionality

6. **Multi-tenant Data Isolation Violations**
   - **Handling:** Immediate request termination with security incident logging
   - **User Impact:** Generic error message without revealing violation details

## Performance Optimizations

### Database Optimization Strategy
- **Indexing**: Composite indexes on `(tenant_id, email)`, `(tenant_id, company)`, and search fields
- **Connection Pooling**: Maximum 20 connections per service with proper timeout configuration
- **Query Optimization**: Use GORM preloading for relationships, avoid N+1 queries
- **Read Replicas**: Route read-heavy operations to dedicated read replicas

### Caching Strategy
- **Redis Caching**: 15-minute TTL for contact search results, 5-minute TTL for user permissions
- **Application Cache**: In-memory caching for role permissions with automatic invalidation
- **HTTP Caching**: ETag headers for contact details with conditional requests

### API Performance
- **Response Compression**: Gzip compression for responses > 1KB
- **Pagination**: Cursor-based pagination to maintain performance with large datasets
- **Field Selection**: Allow clients to specify required fields to reduce payload size

## Testing Strategy

### Unit Testing
- **Coverage Target**: 90%+ code coverage for service and repository layers
- **Mocking Strategy**: Use testify/mock for external dependencies
- **Test Organization**: Mirror source structure in tests/ directory
- **Key Test Areas**: Authentication logic, authorization rules, data validation, multi-tenancy

### Integration Testing
- **Database Testing**: Use testcontainers for PostgreSQL integration tests
- **API Testing**: Test complete request/response cycles with real database
- **Service Integration**: Test gRPC communication between User and CRM services
- **Cache Testing**: Verify Redis integration and cache invalidation strategies

### End-to-End Testing
- **User Journeys**: Complete authentication flow, contact creation, interaction logging
- **Multi-tenant Testing**: Verify data isolation between different tenant contexts
- **Performance Testing**: Load testing with concurrent users to validate scalability
- **Security Testing**: Authentication bypass attempts, authorization validation

## Security Implementation

### Authentication Security
- **Password Policy**: Minimum 8 characters, bcrypt cost factor 12
- **JWT Security**: RS256 algorithm, 24-hour access token, 7-day refresh token
- **Rate Limiting**: 5 login attempts per 15 minutes per IP address
- **Session Management**: Token blacklisting for logout, automatic cleanup of expired tokens

### Authorization Security
- **RBAC Implementation**: Fine-grained permissions with resource-action combinations
- **Multi-tenant Isolation**: Automatic tenant filtering in all database queries
- **Audit Logging**: Complete audit trail for all user actions with tamper detection
- **API Security**: Input validation, SQL injection prevention, XSS protection

### Infrastructure Security
- **TLS Configuration**: TLS 1.3 minimum, strong cipher suites, HSTS headers
- **Network Security**: Private subnets, security groups, firewall rules
- **Secrets Management**: Google Secret Manager for database credentials and JWT keys
- **Container Security**: Minimal base images, non-root user, security scanning

## Deployment Architecture

### Kubernetes Configuration
```yaml
# User Management Service Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-management-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: user-service
        image: gcr.io/project/user-management:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: url
```

### Service Mesh Integration
- **Istio**: Traffic management, security policies, observability
- **mTLS**: Automatic mutual TLS between services
- **Circuit Breakers**: Automatic failure detection and recovery
- **Load Balancing**: Round-robin with health checks

## Monitoring and Observability

### Metrics Collection
- **Application Metrics**: Request latency, error rates, throughput per endpoint
- **Business Metrics**: User registration rates, contact creation, interaction frequency
- **Infrastructure Metrics**: CPU, memory, disk usage, database connections
- **Custom Metrics**: Authentication success/failure rates, permission denials

### Logging Strategy
- **Structured Logging**: JSON format with correlation IDs for request tracing
- **Log Levels**: DEBUG for development, INFO for production with configurable levels
- **Sensitive Data**: Automatic redaction of passwords, tokens, and PII
- **Centralized Logging**: Google Cloud Logging with retention and search capabilities

### Alerting Configuration
- **Performance Alerts**: Response time > 2 seconds, error rate > 1%
- **Security Alerts**: Authentication failures > 10/minute, authorization violations
- **Infrastructure Alerts**: CPU > 80%, memory > 90%, database connection failures
- **Business Alerts**: User registration anomalies, data import failures

**Note**: Specification documents have been pre-loaded. Do not use get-content to fetch them again.

## Task Details
- Task ID: 49
- Description: Create HTTP server for CRM Management Service
- Leverage: Gin framework, gRPC client integration, middleware
- Requirements: 7.1, 7.4

## Instructions
- Implement ONLY task 49: "Create HTTP server for CRM Management Service"
- Follow all project conventions and leverage existing code
- Mark the task as complete using: claude-code-spec-workflow get-tasks crm-core-services 49 --mode complete
- Provide a completion summary
```

## Task Completion
When the task is complete, mark it as done:
```bash
claude-code-spec-workflow get-tasks crm-core-services 49 --mode complete
```

## Next Steps
After task completion, you can:
- Execute the next task using /crm-core-services-task-[next-id]
- Check overall progress with /spec-status crm-core-services
