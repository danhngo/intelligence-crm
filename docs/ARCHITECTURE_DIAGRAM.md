# Intelligence CRM - Architecture Diagrams

## 🏗️ System Architecture Overview

```mermaid
graph TB
    subgraph "Frontend Layer"
        WEB[🌐 Next.js Frontend<br/>Port 3000<br/>TypeScript + Tailwind]
    end

    subgraph "API Gateway Layer"
        GATEWAY[🚪 API Gateway<br/>Nginx Ingress<br/>Load Balancer]
    end

    subgraph "Core Services"
        CRM[📋 CRM Core Service<br/>Port 8001<br/>Python + FastAPI]
        USER[👤 User Management<br/>Port 8002<br/>Python + FastAPI]
        AI[🤖 AI Orchestration<br/>Port 8004<br/>Python + LangChain]
        WORKFLOW[⚡ Workflow Engine<br/>Port 8003<br/>Python + LangGraph]
        ANALYTICS[📊 Analytics Service<br/>Port 8000<br/>Python + FastAPI]
        COMM[💬 Communication Hub<br/>Python + WebSockets]
    end

    subgraph "Data Layer"
        POSTGRES[(🐘 PostgreSQL<br/>Multi-tenant DB)]
        REDIS[(⚡ Redis<br/>Cache & Sessions)]
        VECTOR[(🔍 Vector DB<br/>Pinecone/ChromaDB)]
    end

    subgraph "External Services"
        OPENAI[🧠 OpenAI/Claude APIs]
        GOOGLE[☁️ Google Cloud Services<br/>PubSub, Translation, Speech]
        EMAIL[📧 Email Services<br/>SMTP/SendGrid]
    end

    subgraph "Infrastructure"
        K8S[⚙️ Kubernetes<br/>GKE Cluster]
        MONITOR[📈 Monitoring<br/>Cloud Logging & Metrics]
    end

    WEB --> GATEWAY
    GATEWAY --> CRM
    GATEWAY --> USER
    GATEWAY --> AI
    GATEWAY --> WORKFLOW
    GATEWAY --> ANALYTICS
    GATEWAY --> COMM

    CRM --> POSTGRES
    USER --> POSTGRES
    USER --> REDIS
    ANALYTICS --> POSTGRES
    ANALYTICS --> REDIS

    AI --> VECTOR
    AI --> OPENAI
    WORKFLOW --> AI
    WORKFLOW --> GOOGLE

    COMM --> EMAIL
    COMM --> GOOGLE

    CRM -.-> USER
    AI -.-> CRM
    WORKFLOW -.-> CRM
    ANALYTICS -.-> CRM

    K8S -.-> MONITOR
```

## 🔄 Service Interaction Patterns

### 1. User Authentication Flow
```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Gateway
    participant UserMgmt
    participant Database

    User->>Frontend: Login Request
    Frontend->>Gateway: POST /auth/login
    Gateway->>UserMgmt: Forward Request
    UserMgmt->>Database: Validate Credentials
    Database-->>UserMgmt: User Data
    UserMgmt-->>Gateway: JWT Token
    Gateway-->>Frontend: Authentication Response
    Frontend-->>User: Dashboard Access
```

### 2. Contact Management Flow
```mermaid
sequenceDiagram
    participant Frontend
    participant Gateway
    participant CRMCore
    participant Database
    participant Analytics

    Frontend->>Gateway: Create Contact
    Gateway->>CRMCore: POST /contacts
    CRMCore->>Database: Insert Contact
    Database-->>CRMCore: Contact Created
    CRMCore->>Analytics: Contact Event
    Analytics->>Database: Update Metrics
    CRMCore-->>Gateway: Contact Response
    Gateway-->>Frontend: Success Response
```

### 3. AI-Powered Lead Scoring Flow
```mermaid
sequenceDiagram
    participant CRMCore
    participant AIOrchestration
    participant VectorDB
    participant OpenAI
    participant Database

    CRMCore->>AIOrchestration: Score Lead Request
    AIOrchestration->>VectorDB: Retrieve Similar Leads
    VectorDB-->>AIOrchestration: Historical Data
    AIOrchestration->>OpenAI: Generate Score
    OpenAI-->>AIOrchestration: Lead Score
    AIOrchestration->>Database: Store Score
    AIOrchestration-->>CRMCore: Score Response
```

### 4. Workflow Automation Flow
```mermaid
sequenceDiagram
    participant Trigger
    participant WorkflowEngine
    participant AIOrchestration
    participant CommunicationHub
    participant ExternalAPI

    Trigger->>WorkflowEngine: Event Triggered
    WorkflowEngine->>AIOrchestration: AI Decision Point
    AIOrchestration-->>WorkflowEngine: Decision Result
    WorkflowEngine->>CommunicationHub: Send Message
    CommunicationHub->>ExternalAPI: Email/SMS
    ExternalAPI-->>CommunicationHub: Delivery Status
    CommunicationHub-->>WorkflowEngine: Status Update
```

## 🏛️ Database Architecture

### Multi-Tenant Data Model
```mermaid
erDiagram
    TENANTS {
        uuid id PK
        string name
        string domain
        datetime created_at
        datetime updated_at
    }

    USERS {
        uuid id PK
        uuid tenant_id FK
        string email
        string password_hash
        string role
        datetime created_at
        datetime updated_at
    }

    CONTACTS {
        uuid id PK
        uuid tenant_id FK
        string email
        string first_name
        string last_name
        string company
        string phone
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    INTERACTIONS {
        uuid id PK
        uuid tenant_id FK
        uuid contact_id FK
        string type
        string content
        datetime occurred_at
        datetime created_at
    }

    LEAD_SCORES {
        uuid id PK
        uuid tenant_id FK
        uuid contact_id FK
        float score
        json metadata
        datetime calculated_at
    }

    WORKFLOWS {
        uuid id PK
        uuid tenant_id FK
        string name
        json definition
        boolean active
        datetime created_at
        datetime updated_at
    }

    TENANTS ||--o{ USERS : has
    TENANTS ||--o{ CONTACTS : has
    TENANTS ||--o{ INTERACTIONS : has
    TENANTS ||--o{ LEAD_SCORES : has
    TENANTS ||--o{ WORKFLOWS : has
    CONTACTS ||--o{ INTERACTIONS : has
    CONTACTS ||--o{ LEAD_SCORES : has
```

## 🔧 Service-Specific Architectures

### CRM Core Service Architecture
```mermaid
graph TB
    subgraph "CRM Core Service"
        API[📡 FastAPI Router]
        BL[🧠 Business Logic Layer]
        REPO[💾 Repository Layer]
        MODELS[🗃️ SQLAlchemy Models]
    end

    subgraph "External Dependencies"
        DB[(PostgreSQL)]
        CACHE[(Redis)]
        ANALYTICS_SVC[Analytics Service]
    end

    API --> BL
    BL --> REPO
    REPO --> MODELS
    MODELS --> DB
    REPO --> CACHE
    BL --> ANALYTICS_SVC
```

### AI Orchestration Service Architecture
```mermaid
graph TB
    subgraph "AI Orchestration Service"
        API[📡 FastAPI Router]
        AGENTS[🤖 LangChain Agents]
        TOOLS[🔧 Custom Tools]
        MEMORY[🧠 Agent Memory]
        PROMPTS[📝 Prompt Templates]
    end

    subgraph "AI Infrastructure"
        LLM[🧠 LLM APIs<br/>OpenAI/Claude]
        VECTOR[🔍 Vector Database]
        EMBEDDINGS[📊 Embeddings]
    end

    subgraph "Data Sources"
        CRM_DATA[CRM Data]
        KNOWLEDGE[Knowledge Base]
    end

    API --> AGENTS
    AGENTS --> TOOLS
    AGENTS --> MEMORY
    AGENTS --> PROMPTS
    AGENTS --> LLM
    TOOLS --> VECTOR
    VECTOR --> EMBEDDINGS
    TOOLS --> CRM_DATA
    TOOLS --> KNOWLEDGE
```

### Frontend Architecture
```mermaid
graph TB
    subgraph "Next.js Frontend"
        PAGES[📄 App Router Pages]
        COMPONENTS[🧩 React Components]
        HOOKS[🎣 Custom Hooks]
        STATE[🗃️ State Management]
        API_CLIENT[🌐 API Client]
    end

    subgraph "UI Framework"
        TAILWIND[🎨 Tailwind CSS]
        HEADLESS[🔧 Headless UI]
        ICONS[✨ Heroicons]
    end

    subgraph "Backend APIs"
        CRM_API[CRM Core API]
        USER_API[User Management API]
        AI_API[AI Orchestration API]
        ANALYTICS_API[Analytics API]
    end

    PAGES --> COMPONENTS
    COMPONENTS --> HOOKS
    HOOKS --> STATE
    HOOKS --> API_CLIENT
    COMPONENTS --> TAILWIND
    COMPONENTS --> HEADLESS
    COMPONENTS --> ICONS
    API_CLIENT --> CRM_API
    API_CLIENT --> USER_API
    API_CLIENT --> AI_API
    API_CLIENT --> ANALYTICS_API
```

## 🚀 Deployment Architecture

### Development Environment
```mermaid
graph TB
    subgraph "Developer Machine"
        CODE[💻 Source Code]
        DOCKER[🐳 Docker Compose]
        LOCAL_DB[(Local PostgreSQL)]
        LOCAL_REDIS[(Local Redis)]
    end

    subgraph "Development Services"
        DEV_FRONTEND[Frontend Dev Server<br/>Port 3000]
        DEV_CRM[CRM Service<br/>Port 8001]
        DEV_USER[User Service<br/>Port 8002]
        DEV_AI[AI Service<br/>Port 8004]
    end

    CODE --> DOCKER
    DOCKER --> DEV_FRONTEND
    DOCKER --> DEV_CRM
    DOCKER --> DEV_USER
    DOCKER --> DEV_AI
    DOCKER --> LOCAL_DB
    DOCKER --> LOCAL_REDIS
```

### Production Environment (Kubernetes)
```mermaid
graph TB
    subgraph "Google Kubernetes Engine"
        subgraph "Ingress Layer"
            INGRESS[🚪 Nginx Ingress Controller]
            CERT[🔒 SSL/TLS Certificates]
        end

        subgraph "Application Pods"
            FE_PODS[🌐 Frontend Pods<br/>3 replicas]
            CRM_PODS[📋 CRM Pods<br/>5 replicas]
            USER_PODS[👤 User Pods<br/>3 replicas]
            AI_PODS[🤖 AI Pods<br/>2 replicas]
            WF_PODS[⚡ Workflow Pods<br/>2 replicas]
        end

        subgraph "Data Layer"
            CLOUD_SQL[(☁️ Cloud SQL<br/>PostgreSQL)]
            MEMORYSTORE[(⚡ Memorystore<br/>Redis)]
        end

        subgraph "Monitoring"
            PROMETHEUS[📊 Prometheus]
            GRAFANA[📈 Grafana]
            LOGGING[📝 Cloud Logging]
        end
    end

    subgraph "External Services"
        CDN[🌍 Cloud CDN]
        STORAGE[💾 Cloud Storage]
        AI_APIS[🧠 AI APIs]
    end

    INGRESS --> FE_PODS
    INGRESS --> CRM_PODS
    INGRESS --> USER_PODS
    INGRESS --> AI_PODS
    INGRESS --> WF_PODS

    CRM_PODS --> CLOUD_SQL
    USER_PODS --> CLOUD_SQL
    USER_PODS --> MEMORYSTORE
    AI_PODS --> AI_APIS

    FE_PODS --> CDN
    AI_PODS --> STORAGE

    PROMETHEUS --> GRAFANA
    ALL_PODS --> LOGGING
```

## 🔄 Data Flow Patterns

### Real-time Analytics Flow
```mermaid
graph LR
    USER_ACTION[👤 User Action] --> EVENT_BUS[📡 Event Bus]
    EVENT_BUS --> STREAM_PROCESSOR[⚡ Stream Processor]
    STREAM_PROCESSOR --> METRICS_DB[(📊 Metrics DB)]
    STREAM_PROCESSOR --> REAL_TIME_DASH[📈 Real-time Dashboard]
    METRICS_DB --> BATCH_ANALYTICS[📊 Batch Analytics]
    BATCH_ANALYTICS --> REPORTS[📋 Reports]
```

### Multi-tenant Data Isolation
```mermaid
graph TB
    REQUEST[🌐 Incoming Request] --> AUTH[🔐 Authentication]
    AUTH --> TENANT_ID[🏢 Extract Tenant ID]
    TENANT_ID --> DB_FILTER[🔍 Database Filter]
    DB_FILTER --> TENANT_DATA[(🗃️ Tenant-Specific Data)]
    TENANT_DATA --> RESPONSE[📤 Filtered Response]
```

## 🛡️ Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        WAF[🛡️ Web Application Firewall]
        TLS[🔒 TLS Termination]
        JWT[🎫 JWT Authentication]
        RBAC[👥 Role-Based Access Control]
        TENANT[🏢 Tenant Isolation]
        ENCRYPTION[🔐 Data Encryption]
    end

    subgraph "Threat Protection"
        RATE_LIMIT[⏱️ Rate Limiting]
        INPUT_VALIDATION[✅ Input Validation]
        SQL_INJECTION[🚫 SQL Injection Protection]
        XSS_PROTECTION[🚫 XSS Protection]
    end

    REQUEST[🌐 Request] --> WAF
    WAF --> TLS
    TLS --> JWT
    JWT --> RBAC
    RBAC --> TENANT
    TENANT --> ENCRYPTION

    WAF --> RATE_LIMIT
    TLS --> INPUT_VALIDATION
    RBAC --> SQL_INJECTION
    TENANT --> XSS_PROTECTION
```

This architecture demonstrates a modern, scalable, AI-powered CRM platform built with microservices principles, cloud-native patterns, and enterprise-grade security. The system is designed for high availability, horizontal scaling, and multi-tenancy while providing rich AI capabilities through LangChain integration.