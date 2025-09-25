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