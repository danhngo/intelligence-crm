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

        subgraph comm_hub["Communication Hub"]
            comm_api["Comm API"]
            comm_db[(Comm DB)]
            comm_redis[(Redis Cache 3)]
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

        %% Service interactions
        crm_api --> wf_api
        crm_api --> user_api
        crm_api --> comm_api
        wf_api --> user_api
        wf_api --> comm_api
        user_api --> comm_api
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

### 4. Communication Hub
- **Purpose**: Manages all external communications
- **Dependencies**:
  - PostgreSQL database
  - Redis instance (DB 3)
- **Key Responsibilities**:
  - Message routing
  - Channel management
  - Communication orchestration

## Data Flow

1. **Authentication Flow**:
   - All requests first go through User Management for authentication
   - JWT tokens are used for service-to-service communication

2. **Business Process Flow**:
   - CRM Core receives client requests
   - Delegates workflow execution to Workflow Engine
   - User Management validates permissions
   - Communication Hub handles external messaging

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
  - Postgres instances: 5432-5434
  - Redis instances: 6379-6381

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
