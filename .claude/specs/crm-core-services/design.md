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