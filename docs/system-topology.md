# System Topology

## High-Level Architecture

```mermaid
flowchart TB
    subgraph system["CRM System"]
        subgraph crm_core["CRM Core Service (8000)"]
            crm_api["CRM API"]
            crm_db[(CRM Database)]
            crm_redis[(Redis Cache 0)]
        end

        subgraph workflow["Workflow Engine (8001)"]
            wf_api["Workflow API"]
            wf_db[(Workflow DB)]
            wf_redis[(Redis Cache 1)]
        end

        subgraph user_mgmt["User Management (8002)"]
            user_api["User API"]
            user_db[(User DB)]
            user_redis[(Redis Cache 2)]
        end

        subgraph comm_hub["Communication Hub (8003)"]
            comm_api["Comm API"]
            comm_db[(Comm DB)]
            comm_redis[(Redis Cache 3)]
        end

        subgraph analytics["Analytics Service (8004)"]
            analytics_api["Analytics API"]
            analytics_db[(Analytics DB)]
            analytics_redis[(Redis Cache 4)]
        end

        subgraph ai_orchestration["AI Orchestration (8005)"]
            ai_api["AI API"]
            ai_db[(AI DB)]
            ai_redis[(Redis Cache 5)]
        end

        %% Database connections
        crm_api --> crm_db
        crm_api --> crm_redis
        wf_api --> wf_db
        wf_api --> wf_redis
        user_api --> user_db
        user_api --> user_redis
        comm_api --> comm_db
        comm_api --> comm_redis
        analytics_api --> analytics_db
        analytics_api --> analytics_redis
        ai_api --> ai_db
        ai_api --> ai_redis

        %% Service interactions
        crm_api --> wf_api
        crm_api --> user_api
        crm_api --> comm_api
        crm_api --> analytics_api
        crm_api --> ai_api
        wf_api --> user_api
        wf_api --> comm_api
        wf_api --> ai_api
        user_api --> comm_api
        analytics_api --> ai_api
        ai_api --> analytics_api
    end
```

## Service Communication Overview

### 1. CRM Core Service (Port 8000)
- **Purpose**: Main entry point for CRM operations
- **Dependencies**:
  - PostgreSQL database (crm)
  - Redis instance (DB 0)
  - Workflow Engine
  - User Management
  - Communication Hub
- **Key Responsibilities**:
  - Customer data management
  - Integration orchestration
  - Business logic coordination

### 2. Workflow Engine (Port 8001)
- **Purpose**: Manages business process workflows
- **Dependencies**:
  - PostgreSQL database (workflows)
  - Redis instance (DB 1)
  - User Management
  - Communication Hub
- **Key Responsibilities**:
  - Workflow definition and execution
  - State management
  - Process automation

### 3. User Management (Port 8002)
- **Purpose**: Handles user authentication and authorization
- **Dependencies**:
  - PostgreSQL database (user_management)
  - Redis instance (DB 2)
  - Communication Hub
- **Key Responsibilities**:
  - User authentication
  - Role management
  - Access control

### 4. Communication Hub (Port 8003)
- **Purpose**: Manages all external communications
- **Dependencies**:
  - PostgreSQL database
  - Redis instance (DB 3)
- **Key Responsibilities**:
  - Message routing
  - Channel management
  - Communication orchestration

### 5. Analytics Service (Port 8004)
- **Purpose**: Provides business intelligence and analytics
- **Dependencies**:
  - PostgreSQL database (analytics)
  - Redis instance (DB 4)
  - AI Orchestration service
- **Key Responsibilities**:
  - Data analysis and reporting
  - Performance metrics
  - Business intelligence dashboards

### 6. AI Orchestration Service (Port 8005)
- **Purpose**: Manages AI/ML workflows and intelligent automation
- **Dependencies**:
  - PostgreSQL database (ai_orchestration)
  - Redis instance (DB 5)
  - LangChain integration
- **Key Responsibilities**:
  - Lead scoring and qualification
  - Content generation
  - Next best action recommendations
  - Customer insights and analytics

## Data Flow

1. **Authentication Flow**:
   - All requests first go through User Management for authentication
   - JWT tokens are used for service-to-service communication

2. **Business Process Flow**:
   - CRM Core receives client requests
   - Delegates workflow execution to Workflow Engine
   - User Management validates permissions
   - Communication Hub handles external messaging
   - Analytics Service provides insights and metrics
   - AI Orchestration enables intelligent automation and recommendations

3. **Data Storage**:
   - Each service has its own PostgreSQL database
   - Redis is used for caching and session management
   - Databases are isolated for service independence

## Network Configuration

- All services are connected through `crm-network`
- Internal service discovery via Docker DNS
- Port mapping:
  - CRM Core: 8000
  - Workflow Engine: 8001
  - User Management: 8002
  - Communication Hub: 8003
  - Analytics Service: 8004
  - AI Orchestration: 8005
  - Postgres instances: 5432, 5434-5436
  - Redis instances: 6379-6382

## Security Considerations

1. **Service Isolation**:
   - Each service has its own database
   - Redis instances are separated by database index
   - Network segregation via Docker network

2. **Authentication**:
   - Centralized authentication through User Management
   - Service-to-service authentication using JWT
   - Rate limiting on API endpoints

3. **Data Protection**:
   - Database credentials managed via environment variables
   - Network access controlled through Docker network
   - Service-level access controls
