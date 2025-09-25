# Implementation Plan - CRM Core Services

## Task Overview
This implementation plan breaks down the CRM Core Services into atomic, executable tasks that implement two foundational Go microservices: User Management Service and CRM Management Service. Each task is designed for 15-30 minute execution windows, touches 1-3 files maximum, and provides clear success criteria.

The implementation follows a layered approach starting with infrastructure setup, then data models, service layers, API handlers, security features, and finally deployment configurations. Tasks leverage existing Go libraries (Gin, GORM, JWT-Go) and Google Cloud services while establishing patterns for future AI service integrations.

## Steering Document Compliance
Tasks follow structure.md conventions with proper Go service organization (`cmd/`, `internal/`, `pkg/` directories) and tech.md patterns (Gin framework, GORM ORM, PostgreSQL + Redis architecture). All implementation follows established naming conventions, import patterns, and testing strategies documented in the steering context.

## Atomic Task Requirements
**Each task meets these criteria for optimal agent execution:**
- **File Scope**: Touches 1-3 related files maximum
- **Time Boxing**: Completable in 15-30 minutes
- **Single Purpose**: One testable outcome per task
- **Specific Files**: Must specify exact files to create/modify
- **Agent-Friendly**: Clear input/output with minimal context switching

## Task Format Guidelines
- Use checkbox format: `- [ ] Task number. Task description`
- **Specify files**: Always include exact file paths to create/modify
- **Include implementation details** as bullet points
- Reference requirements using: `_Requirements: X.Y, Z.A_`
- Reference existing code to leverage using: `_Leverage: path/to/file.ts, path/to/component.tsx_`
- Focus only on coding tasks (no deployment, user testing, etc.)
- **Avoid broad terms**: No "system", "integration", "complete" in task titles

## Good vs Bad Task Examples
❌ **Bad Examples (Too Broad)**:
- "Implement authentication system" (affects many files, multiple purposes)
- "Add user management features" (vague scope, no file specification)
- "Build complete dashboard" (too large, multiple components)

✅ **Good Examples (Atomic)**:
- "Create User model in internal/models/user.go with GORM tags and validation"
- "Add bcrypt password hashing utility in pkg/auth/password.go"
- "Create authentication handler in internal/handlers/auth_handler.go with login endpoint"

## Tasks

### Phase 1: Project Structure and Configuration

- [ ] 1. Create User Management Service directory structure
  - Files: services/user-management/ directory with subdirectories
  - Create cmd/, internal/, pkg/, migrations/ directories
  - Purpose: Establish basic service directory layout
  - _Leverage: Standard Go project layout patterns_
  - _Requirements: 7.1_

- [ ] 2. Initialize User Management Service Go module
  - File: services/user-management/go.mod
  - Initialize Go module with 'go mod init user-management-service'
  - Add initial dependencies: gin, gorm, jwt-go, uuid
  - Purpose: Set up Go module with required dependencies
  - _Leverage: Go module system_
  - _Requirements: 7.1_

- [ ] 3. Create CRM Management Service directory structure
  - Files: services/crm-management/ directory with subdirectories
  - Create cmd/, internal/, pkg/, migrations/ directories
  - Purpose: Establish basic service directory layout
  - _Leverage: Standard Go project layout patterns_
  - _Requirements: 3.1, 4.1, 5.1_

- [ ] 4. Initialize CRM Management Service Go module
  - File: services/crm-management/go.mod
  - Initialize Go module with 'go mod init crm-management-service'
  - Add initial dependencies: gin, gorm, postgresql driver
  - Purpose: Set up Go module with required dependencies
  - _Leverage: Go module system_
  - _Requirements: 3.1, 4.1, 5.1_

- [ ] 5. Create User Management Protocol Buffer definitions
  - File: shared/proto/user_service.proto
  - Define ValidateToken and GetUserPermissions RPC methods
  - Add User and Permission message definitions
  - Purpose: Define gRPC contract for authentication service
  - _Leverage: Protocol Buffers specification_
  - _Requirements: 7.2_

- [ ] 6. Create CRM Management Protocol Buffer definitions
  - File: shared/proto/crm_service.proto
  - Define GetContactData RPC method and Contact message
  - Add Interaction and Lead message definitions
  - Purpose: Define gRPC contract for CRM data access
  - _Leverage: Protocol Buffers specification_
  - _Requirements: 7.2_

- [ ] 7. Generate Go code from Protocol Buffer definitions
  - Files: shared/proto/user_service.pb.go, shared/proto/crm_service.pb.go
  - Run protoc compiler to generate Go structs and gRPC client/server code
  - Add generated files to both service dependencies
  - Purpose: Create type-safe gRPC interfaces for Go services
  - _Leverage: Protocol Buffer compiler, gRPC code generation_
  - _Requirements: 7.2_

### Phase 2: User Management Service - Data Models

- [ ] 8. Create User model in User Management Service
  - File: services/user-management/internal/models/user.go
  - Implement User struct with GORM tags, UUID primary key, tenant isolation
  - Add Role enum constants (Admin, Manager, Sales, Marketing)
  - Include validation tags and JSON serialization
  - Purpose: Define core user data structure with multi-tenant support
  - _Leverage: GORM ORM, UUID package, validation framework_
  - _Requirements: 1.1, 2.1, 6.1_

- [ ] 9. Create Permission model in User Management Service
  - File: services/user-management/internal/models/permission.go
  - Implement Permission struct with role-resource-action mappings
  - Add database indexes for efficient permission lookups
  - Define default permission sets for each role
  - Purpose: Enable fine-grained role-based access control
  - _Leverage: GORM ORM, database indexing strategies_
  - _Requirements: 2.1, 2.2_

- [ ] 10. Create users table migration for User Management Service
  - File: services/user-management/migrations/001_create_users.sql
  - Create users table with UUID primary key, tenant isolation, and indexes
  - Add unique constraint on (tenant_id, email) combination
  - Purpose: Establish users table schema with multi-tenant support
  - _Leverage: PostgreSQL UUID functions, composite indexes_
  - _Requirements: 1.1, 6.1_

- [ ] 11. Create permissions table migration for User Management Service
  - File: services/user-management/migrations/002_create_permissions.sql
  - Create permissions table with role-resource-action mappings
  - Add indexes on role and resource fields for fast lookups
  - Include default permission data for Admin, Manager, Sales, Marketing roles
  - Purpose: Establish RBAC permission system with default data
  - _Leverage: PostgreSQL indexes, data seeding_
  - _Requirements: 2.1, 2.2_

### Phase 3: CRM Management Service - Data Models

- [ ] 12. Create Contact model in CRM Management Service
  - File: services/crm-management/internal/models/contact.go
  - Implement Contact struct with full profile fields and GORM tags
  - Add search-optimized indexes and custom fields JSON support
  - Include relationship definitions for interactions and leads
  - Purpose: Define comprehensive contact data structure with search capabilities
  - _Leverage: GORM ORM, PostgreSQL JSON fields, text search_
  - _Requirements: 3.1, 3.2, 6.1_

- [ ] 13. Create Interaction model in CRM Management Service
  - File: services/crm-management/internal/models/interaction.go
  - Implement Interaction struct with timeline and audit fields
  - Add foreign key relationships to contacts and users
  - Include interaction type enums and outcome tracking
  - Purpose: Enable comprehensive customer interaction tracking
  - _Leverage: GORM ORM, foreign key constraints, enum types_
  - _Requirements: 4.1, 4.2, 6.1_

- [ ] 14. Create Lead model in CRM Management Service
  - File: services/crm-management/internal/models/lead.go
  - Implement Lead struct with status tracking and scoring fields
  - Add status history as JSONB for audit trail
  - Include probability and value fields for sales forecasting
  - Purpose: Establish lead management with conversion pipeline tracking
  - _Leverage: GORM ORM, PostgreSQL JSONB, status enums_
  - _Requirements: 5.1, 5.2, 6.1_

- [ ] 15. Create contacts table migration for CRM Management Service
  - File: services/crm-management/migrations/001_create_contacts.sql
  - Create contacts table with comprehensive profile fields and tenant isolation
  - Add composite indexes on (tenant_id, email) and (tenant_id, company)
  - Purpose: Establish contacts table schema optimized for search
  - _Leverage: PostgreSQL composite indexes, text search_
  - _Requirements: 3.1, 6.1_

- [ ] 16. Create interactions table migration for CRM Management Service
  - File: services/crm-management/migrations/002_create_interactions.sql
  - Create interactions table with foreign keys to contacts and users
  - Add indexes on contact_id, user_id, and created_at for timeline queries
  - Purpose: Establish interaction tracking with optimized timeline access
  - _Leverage: PostgreSQL foreign keys, date-based indexes_
  - _Requirements: 4.1, 6.1_

- [ ] 17. Create leads table migration for CRM Management Service
  - File: services/crm-management/migrations/003_create_leads.sql
  - Create leads table with status tracking and JSONB status history
  - Add indexes on status, assigned_user_id, and expected_close_at
  - Purpose: Establish lead pipeline with status-based queries
  - _Leverage: PostgreSQL JSONB, status-based indexes_
  - _Requirements: 5.1, 5.2, 6.1_

- [ ] 18. Create full-text search indexes for CRM Management Service
  - File: services/crm-management/migrations/004_add_search_indexes.sql
  - Add full-text search indexes on contact name, email, company fields
  - Configure PostgreSQL text search with custom language configuration
  - Purpose: Enable fast fuzzy search capabilities for contact lookup
  - _Leverage: PostgreSQL full-text search, GIN indexes_
  - _Requirements: 3.2_

### Phase 4: Security and Utility Functions

- [ ] 19. Create password hashing utility in User Management Service
  - File: services/user-management/pkg/auth/password.go
  - Implement bcrypt password hashing with cost factor 12
  - Add password validation function with security requirements
  - Include password comparison function for authentication
  - Purpose: Provide secure password handling with industry-standard hashing
  - _Leverage: bcrypt package, crypto/rand for secure randomization_
  - _Requirements: 1.1, 1.2_

- [ ] 20. Create JWT token utility in User Management Service
  - File: services/user-management/pkg/auth/jwt.go
  - Implement JWT token generation with RS256 algorithm
  - Add token validation with expiration and blacklist checking
  - Include refresh token functionality with secure storage
  - Purpose: Enable secure JWT-based authentication with proper token lifecycle
  - _Leverage: jwt-go package, RS256 signing, Redis for token blacklisting_
  - _Requirements: 1.2, 1.4_

- [ ] 21. Create security event logging utility in User Management Service
  - File: services/user-management/pkg/security/audit.go
  - Implement security event logging for authentication failures and violations
  - Add structured logging with correlation IDs and user context
  - Include log level configuration and sensitive data redaction
  - Purpose: Provide comprehensive security audit trail for compliance
  - _Leverage: Structured logging libraries, security event classification_
  - _Requirements: 1.3, 2.3_

- [ ] 22. Create tenant isolation validator in both services
  - File: services/user-management/pkg/security/tenant.go
  - Implement tenant ID validation and automatic filtering functions
  - Add cross-tenant access detection with security violation logging
  - Include middleware for automatic tenant scoping in database queries
  - Purpose: Ensure strict multi-tenant data isolation and security
  - _Leverage: GORM scopes, security violation detection_
  - _Requirements: 6.2, 6.3_

### Phase 5: User Management Service - Business Logic

- [ ] 23. Create User repository in User Management Service
  - File: services/user-management/internal/repository/user_repository.go
  - Implement basic CRUD operations with tenant isolation
  - Add user lookup by email and ID with proper indexing
  - Include automatic tenant scoping for all database queries
  - Purpose: Provide data access layer with automatic multi-tenant filtering
  - _Leverage: GORM ORM, automatic tenant scoping_
  - _Requirements: 1.1, 1.5, 6.2_

- [ ] 24. Add audit logging to User repository
  - File: services/user-management/internal/repository/user_repository.go (extend)
  - Add audit logging for all user data changes (create, update, delete)
  - Include change tracking with before/after values and user attribution
  - Purpose: Maintain complete audit trail for user data modifications
  - _Leverage: Audit logging utility, change detection_
  - _Requirements: 1.5_

- [ ] 25. Create User service layer in User Management Service
  - File: services/user-management/internal/services/user_service.go
  - Implement user registration with validation and role assignment
  - Add authentication logic with password verification and security logging
  - Include basic user management functions (get, update, list)
  - Purpose: Orchestrate core user management business logic
  - _Leverage: User repository, password utilities, validation framework_
  - _Requirements: 1.1, 1.2, 1.3_

- [ ] 26. Add role management to User service layer
  - File: services/user-management/internal/services/user_service.go (extend)
  - Add role assignment and permission validation functions
  - Include permission checking with resource-action combinations
  - Purpose: Enable complete RBAC functionality with permission validation
  - _Leverage: Permission model, role validation logic_
  - _Requirements: 2.1, 2.2, 2.4, 2.5_

### Phase 6: CRM Management Service - Business Logic

- [ ] 27. Create Contact repository in CRM Management Service
  - File: services/crm-management/internal/repository/contact_repository.go
  - Implement basic contact CRUD operations with tenant isolation
  - Add contact lookup by ID and email with automatic tenant scoping
  - Purpose: Provide basic contact data access with multi-tenant security
  - _Leverage: GORM ORM, tenant isolation utilities_
  - _Requirements: 3.1, 6.2_

- [ ] 28. Add contact search functionality to Contact repository
  - File: services/crm-management/internal/repository/contact_repository.go (extend)
  - Implement fuzzy search using PostgreSQL full-text search capabilities
  - Add search by name, email, company with ranking and pagination
  - Purpose: Enable fast contact search with relevance ranking
  - _Leverage: PostgreSQL full-text search, search ranking algorithms_
  - _Requirements: 3.2_

- [ ] 29. Add contact import functionality to Contact repository
  - File: services/crm-management/internal/repository/contact_repository.go (extend)
  - Implement duplicate detection and CSV import handling
  - Add batch processing for large contact imports
  - Purpose: Enable bulk contact import with duplicate prevention
  - _Leverage: CSV processing libraries, batch operations_
  - _Requirements: 3.5_

- [ ] 30. Create Interaction repository in CRM Management Service
  - File: services/crm-management/internal/repository/interaction_repository.go
  - Implement interaction CRUD with timeline sorting and filtering
  - Add contact timeline retrieval with date-based pagination
  - Include interaction metrics aggregation for reporting
  - Purpose: Enable comprehensive interaction tracking and timeline management
  - _Leverage: GORM ORM, date/time filtering, aggregation queries_
  - _Requirements: 4.1, 4.2, 4.5_

- [ ] 31. Add partial interaction handling to Interaction repository
  - File: services/crm-management/internal/repository/interaction_repository.go (extend)
  - Implement storage for incomplete interaction data with flagging
  - Add manual review queue for partial or incomplete interactions
  - Purpose: Handle incomplete interaction data as per requirements
  - _Leverage: Status flagging, review queue patterns_
  - _Requirements: 4.3_

- [ ] 32. Create Lead repository in CRM Management Service
  - File: services/crm-management/internal/repository/lead_repository.go
  - Implement lead CRUD with status transition tracking
  - Add pipeline view with status filtering and metrics
  - Include inactive lead detection and follow-up flagging (30+ days)
  - Purpose: Provide lead management with pipeline visualization and automation
  - _Leverage: GORM ORM, status tracking, date-based queries_
  - _Requirements: 5.1, 5.2, 5.3_

- [ ] 33. Create contact management service layer
  - File: services/crm-management/internal/services/contact_service.go
  - Implement contact management business logic with validation
  - Add contact validation with specific field error handling
  - Include duplicate detection during contact creation
  - Purpose: Orchestrate contact business logic with comprehensive validation
  - _Leverage: Contact repository, validation framework_
  - _Requirements: 3.1, 3.4_

- [ ] 34. Create interaction management service layer
  - File: services/crm-management/internal/services/interaction_service.go
  - Implement interaction logging with automatic timestamp and user attribution
  - Add interaction timeline management with filtering capabilities
  - Purpose: Orchestrate interaction tracking business logic
  - _Leverage: Interaction repository, timeline utilities_
  - _Requirements: 4.1, 4.2_

- [ ] 35. Create lead management service layer
  - File: services/crm-management/internal/services/lead_service.go
  - Implement lead status management with transition logging
  - Add lead scoring foundation and conversion tracking
  - Include automated customer record creation on lead conversion
  - Purpose: Orchestrate lead management with automated workflows
  - _Leverage: Lead repository, status tracking, automation logic_
  - _Requirements: 5.1, 5.2, 5.5_

### Phase 7: API Handlers and HTTP Endpoints

- [ ] 36. Create authentication handlers in User Management Service
  - File: services/user-management/internal/handlers/auth_handler.go
  - Implement login endpoint with credential validation and JWT generation
  - Add proper error responses for invalid credentials with security logging
  - Include rate limiting for authentication attempts
  - Purpose: Provide HTTP API for authentication operations
  - _Leverage: Gin framework, JWT utilities, rate limiting middleware_
  - _Requirements: 1.1, 1.2, 1.3_

- [ ] 37. Add registration and refresh handlers to authentication
  - File: services/user-management/internal/handlers/auth_handler.go (extend)
  - Add user registration endpoint with role assignment
  - Implement token refresh endpoint with validation
  - Purpose: Complete authentication API functionality
  - _Leverage: User service layer, JWT utilities_
  - _Requirements: 1.2, 1.4_

- [ ] 38. Create user management handlers in User Management Service
  - File: services/user-management/internal/handlers/user_handler.go
  - Implement user CRUD endpoints with role-based authorization
  - Add user listing with filtering and pagination
  - Include role assignment endpoints for admin users
  - Purpose: Provide HTTP API for user management operations
  - _Leverage: Gin framework, authorization middleware, pagination utilities_
  - _Requirements: 2.1, 2.2, 2.4, 2.5_

- [ ] 39. Create contact handlers in CRM Management Service
  - File: services/crm-management/internal/handlers/contact_handler.go
  - Implement contact CRUD endpoints with search functionality
  - Add contact search endpoint with fuzzy matching and pagination
  - Include contact timeline endpoint with interaction history
  - Purpose: Provide HTTP API for contact management operations
  - _Leverage: Gin framework, search utilities, pagination_
  - _Requirements: 3.1, 3.2, 3.3_

- [ ] 40. Add contact import handler to contact endpoints
  - File: services/crm-management/internal/handlers/contact_handler.go (extend)
  - Add contact import endpoint with CSV processing
  - Include validation error handling with specific field errors
  - Purpose: Enable bulk contact import via HTTP API
  - _Leverage: CSV processing, validation error formatting_
  - _Requirements: 3.4, 3.5_

- [ ] 41. Create interaction handlers in CRM Management Service
  - File: services/crm-management/internal/handlers/interaction_handler.go
  - Implement interaction logging and timeline endpoints
  - Add interaction filtering and reporting capabilities
  - Include interaction metrics aggregation endpoints
  - Purpose: Provide HTTP API for interaction tracking operations
  - _Leverage: Gin framework, timeline utilities, metrics aggregation_
  - _Requirements: 4.1, 4.2, 4.5_

- [ ] 42. Create lead handlers in CRM Management Service
  - File: services/crm-management/internal/handlers/lead_handler.go
  - Implement lead pipeline endpoints with status management
  - Add lead status transition endpoints with logging
  - Include lead metrics and conversion reporting
  - Purpose: Provide HTTP API for lead management operations
  - _Leverage: Gin framework, status management, pipeline utilities_
  - _Requirements: 5.1, 5.2, 5.4, 5.5_

### Phase 8: gRPC Inter-Service Communication

- [ ] 43. Create gRPC server implementation in User Management Service
  - File: services/user-management/internal/grpc/user_grpc_server.go
  - Implement ValidateToken RPC method with JWT validation
  - Add proper error handling and context management
  - Include request logging and performance monitoring
  - Purpose: Enable inter-service authentication validation
  - _Leverage: gRPC framework, Protocol Buffers, JWT validation_
  - _Requirements: 1.2, 7.2_

- [ ] 44. Add GetUserPermissions RPC to gRPC server
  - File: services/user-management/internal/grpc/user_grpc_server.go (extend)
  - Implement GetUserPermissions RPC method with role-based permission lookup
  - Add permission caching for performance optimization
  - Purpose: Enable inter-service authorization checks
  - _Leverage: Permission validation, Redis caching_
  - _Requirements: 2.2, 7.2_

- [ ] 45. Create gRPC client in CRM Management Service
  - File: services/crm-management/internal/grpc/user_grpc_client.go
  - Implement client for User Management Service gRPC APIs
  - Add connection pooling and retry mechanisms
  - Include circuit breaker for service resilience
  - Purpose: Enable CRM service to authenticate and authorize requests
  - _Leverage: gRPC client libraries, connection pooling, circuit breakers_
  - _Requirements: 7.2_

### Phase 9: HTTP Server Setup and Middleware

- [ ] 46. Create HTTP server for User Management Service
  - File: services/user-management/cmd/server/main.go
  - Initialize Gin router with basic middleware stack
  - Configure route registration and server startup
  - Add graceful shutdown handling
  - Purpose: Bootstrap User Management Service HTTP server
  - _Leverage: Gin framework, server configuration_
  - _Requirements: 7.1, 7.4_

- [ ] 47. Create middleware package for User Management Service
  - File: services/user-management/internal/middleware/auth_middleware.go
  - Implement JWT authentication middleware
  - Add role-based authorization middleware
  - Include request logging and correlation ID middleware
  - Purpose: Provide reusable middleware for authentication and logging
  - _Leverage: Gin middleware, JWT validation, request context_
  - _Requirements: 1.2, 2.2, 7.4_

- [ ] 48. Add rate limiting middleware to User Management Service
  - File: services/user-management/internal/middleware/rate_limit_middleware.go
  - Implement rate limiting for authentication endpoints
  - Add 429 responses with retry-after headers for exceeded limits
  - Include IP-based and user-based rate limiting
  - Purpose: Prevent authentication abuse and DoS attacks
  - _Leverage: Rate limiting libraries, Redis for state storage_
  - _Requirements: 7.3_

- [ ] 49. Create HTTP server for CRM Management Service
  - File: services/crm-management/cmd/server/main.go
  - Initialize Gin router with middleware stack
  - Add authentication via User Management Service integration
  - Configure route registration and server startup
  - Purpose: Bootstrap CRM Management Service HTTP server
  - _Leverage: Gin framework, gRPC client integration, middleware_
  - _Requirements: 7.1, 7.4_

- [ ] 50. Create middleware package for CRM Management Service
  - File: services/crm-management/internal/middleware/auth_middleware.go
  - Implement authentication middleware using User Management gRPC
  - Add tenant isolation middleware for automatic filtering
  - Include request logging and performance monitoring
  - Purpose: Provide authentication and tenant isolation for CRM endpoints
  - _Leverage: gRPC client, tenant context, request middleware_
  - _Requirements: 2.2, 6.2, 7.4_

### Phase 10: Configuration and Database Setup

- [ ] 51. Create configuration management for User Management Service
  - File: services/user-management/internal/config/config.go
  - Implement configuration loading from environment variables
  - Add database connection settings (DATABASE_URL, DB_MAX_CONNECTIONS)
  - Include JWT configuration (JWT_SECRET_KEY, JWT_EXPIRATION)
  - Include Redis connection settings (REDIS_URL, REDIS_PASSWORD)
  - Purpose: Centralize service configuration with environment support
  - _Leverage: Viper configuration library, environment variable loading_
  - _Requirements: 1.1, 1.2, 1.4_

- [ ] 52. Create database connection for User Management Service
  - File: services/user-management/internal/db/connection.go
  - Implement PostgreSQL connection with GORM
  - Add connection pooling and health check functionality
  - Include Redis connection for caching and session management
  - Purpose: Establish database connectivity with performance optimization
  - _Leverage: GORM ORM, PostgreSQL driver, Redis client_
  - _Requirements: 1.1, 6.1_

- [ ] 53. Create configuration management for CRM Management Service
  - File: services/crm-management/internal/config/config.go
  - Implement configuration loading from environment variables
  - Add database connection settings and gRPC client configuration
  - Include Redis connection and search configuration
  - Include User Management Service gRPC endpoint configuration
  - Purpose: Centralize service configuration with environment support
  - _Leverage: Viper configuration library, environment variable loading_
  - _Requirements: 3.1, 7.2_

- [ ] 54. Create database connection for CRM Management Service
  - File: services/crm-management/internal/db/connection.go
  - Implement PostgreSQL connection with GORM
  - Add full-text search configuration and connection pooling
  - Include Redis connection for caching contact search results
  - Purpose: Establish database connectivity optimized for search operations
  - _Leverage: GORM ORM, PostgreSQL full-text search, Redis caching_
  - _Requirements: 3.1, 3.2, 6.1_

### Phase 11: Testing Implementation

- [ ] 55. Create unit tests for User Management Service models
  - File: services/user-management/internal/models/user_test.go
  - Write tests for User model validation and GORM operations
  - Add tests for Role and Permission model functionality
  - Include tests for tenant isolation and data integrity
  - Purpose: Ensure data model correctness and validation logic
  - _Leverage: Testify framework, GORM testing, database mocking_
  - _Requirements: 1.1, 2.1, 6.1_

- [ ] 56. Create unit tests for User Management Service business logic
  - File: services/user-management/internal/services/user_service_test.go
  - Write tests for authentication and authorization logic
  - Add tests for password hashing and JWT token operations
  - Include tests for role management and permission validation
  - Purpose: Ensure business logic correctness and security
  - _Leverage: Testify framework, mocking, security testing_
  - _Requirements: 1.1, 1.2, 2.1, 2.2_

- [ ] 57. Create integration tests for User Management Service API
  - File: services/user-management/tests/integration/auth_test.go
  - Write tests for authentication flow with real database
  - Add tests for user management endpoints with authorization
  - Include tests for gRPC service endpoints
  - Purpose: Ensure API functionality and inter-service communication
  - _Leverage: Testcontainers, HTTP testing, gRPC testing_
  - _Requirements: 1.1, 1.2, 2.1, 7.2_

- [ ] 58. Create unit tests for CRM Management Service models
  - File: services/crm-management/internal/models/contact_test.go
  - Write tests for Contact, Interaction, and Lead model validation
  - Add tests for search functionality and relationship handling
  - Include tests for tenant isolation and data integrity
  - Purpose: Ensure CRM data model correctness and search capabilities
  - _Leverage: Testify framework, GORM testing, search testing_
  - _Requirements: 3.1, 4.1, 5.1, 6.1_

- [ ] 59. Create unit tests for CRM Management Service business logic
  - File: services/crm-management/internal/services/contact_service_test.go
  - Write tests for contact management and search logic
  - Add tests for interaction tracking and timeline functionality
  - Include tests for lead management and status transitions
  - Purpose: Ensure CRM business logic correctness and workflow automation
  - _Leverage: Testify framework, mocking, workflow testing_
  - _Requirements: 3.1, 4.1, 5.1, 5.2_

- [ ] 60. Create integration tests for CRM Management Service API
  - File: services/crm-management/tests/integration/crm_test.go
  - Write tests for contact CRUD operations with authentication
  - Add tests for interaction logging and timeline retrieval
  - Include tests for lead pipeline and status management
  - Purpose: Ensure CRM API functionality with authentication integration
  - _Leverage: Testcontainers, HTTP testing, gRPC client testing_
  - _Requirements: 3.1, 4.1, 5.1, 7.2_

### Phase 12: Docker and Deployment Configuration

- [ ] 61. Create Dockerfile for User Management Service
  - File: services/user-management/Dockerfile
  - Create multi-stage Docker build with golang:1.21-alpine base
  - Add security hardening with non-root user and minimal image
  - Include health check endpoint (/health) configuration
  - Purpose: Containerize User Management Service for deployment
  - _Leverage: Docker multi-stage builds, Go binary optimization_
  - _Requirements: Deployment scalability_

- [ ] 62. Create Dockerfile for CRM Management Service
  - File: services/crm-management/Dockerfile
  - Create multi-stage Docker build with golang:1.21-alpine base
  - Add security hardening with non-root user and minimal image
  - Include health check endpoint (/health) configuration
  - Purpose: Containerize CRM Management Service for deployment
  - _Leverage: Docker multi-stage builds, Go binary optimization_
  - _Requirements: Deployment scalability_

- [ ] 63. Create Kubernetes deployment for User Management Service
  - File: infrastructure/kubernetes/user-management-deployment.yaml
  - Define Deployment with 3 replicas and resource limits (512Mi memory, 500m CPU)
  - Add liveness and readiness probes pointing to /health endpoint
  - Include environment variables from ConfigMap and Secrets
  - Purpose: Enable Kubernetes deployment with proper resource management
  - _Leverage: Kubernetes Deployment patterns_
  - _Requirements: Scalability, reliability_

- [ ] 64. Create Kubernetes Service for User Management Service
  - File: infrastructure/kubernetes/user-management-service.yaml
  - Define Service with ClusterIP type for internal communication
  - Add gRPC port (50051) and HTTP port (8080) exposure
  - Include service discovery labels and selectors
  - Purpose: Enable load balancing and service discovery
  - _Leverage: Kubernetes Service patterns_
  - _Requirements: 7.2, scalability_

- [ ] 65. Create Kubernetes deployment for CRM Management Service
  - File: infrastructure/kubernetes/crm-management-deployment.yaml
  - Define Deployment with 3 replicas and resource limits (512Mi memory, 500m CPU)
  - Add liveness and readiness probes pointing to /health endpoint
  - Include environment variables from ConfigMap and Secrets
  - Purpose: Enable Kubernetes deployment with proper resource management
  - _Leverage: Kubernetes Deployment patterns_
  - _Requirements: Scalability, reliability_

- [ ] 66. Create Kubernetes Service for CRM Management Service
  - File: infrastructure/kubernetes/crm-management-service.yaml
  - Define Service with ClusterIP type for internal communication
  - Add HTTP port (8080) exposure for API access
  - Include service discovery labels and selectors
  - Purpose: Enable load balancing and service discovery
  - _Leverage: Kubernetes Service patterns_
  - _Requirements: Scalability_

- [ ] 67. Create Docker Compose for local development
  - File: docker-compose.yml
  - Define services for User Management and CRM Management services
  - Add PostgreSQL service with environment variables and volume mounts
  - Add Redis service for caching and session storage
  - Include development-friendly volume mounts and port mappings
  - Purpose: Enable complete local development environment
  - _Leverage: Docker Compose service orchestration_
  - _Requirements: Development environment_

### Phase 13: Monitoring and Observability

- [ ] 68. Create logging configuration for User Management Service
  - File: services/user-management/pkg/logger/logger.go
  - Implement structured logging with JSON format using logrus
  - Add correlation ID tracking and security event logging
  - Include log level configuration (DEBUG, INFO, WARN, ERROR) and sensitive data redaction
  - Purpose: Provide comprehensive logging for debugging and auditing
  - _Leverage: Logrus structured logging library_
  - _Requirements: 1.3, 2.3, security compliance_

- [ ] 69. Create metrics collection for User Management Service
  - File: services/user-management/pkg/metrics/metrics.go
  - Implement Prometheus metrics for authentication events
  - Add custom metrics for user registration rates and login success/failure rates
  - Include HTTP request duration and database connection metrics
  - Purpose: Enable monitoring and alerting for service health
  - _Leverage: Prometheus Go client library_
  - _Requirements: Performance monitoring_

- [ ] 70. Create logging configuration for CRM Management Service
  - File: services/crm-management/pkg/logger/logger.go
  - Implement structured logging with JSON format using logrus
  - Add correlation ID tracking and business event logging
  - Include log level configuration and data privacy compliance (PII redaction)
  - Purpose: Provide comprehensive logging for CRM operations
  - _Leverage: Logrus structured logging library_
  - _Requirements: 3.3, 4.3, 5.3, audit compliance_

- [ ] 71. Create metrics collection for CRM Management Service
  - File: services/crm-management/pkg/metrics/metrics.go
  - Implement Prometheus metrics for CRM operations
  - Add custom metrics for contact creation rates, search performance, and interaction frequency
  - Include lead conversion metrics and database query performance
  - Purpose: Enable monitoring and alerting for CRM service health
  - _Leverage: Prometheus Go client library_
  - _Requirements: Performance monitoring_

- [ ] 72. Add health check endpoints to both services
  - Files: services/user-management/internal/handlers/health_handler.go, services/crm-management/internal/handlers/health_handler.go
  - Implement /health endpoint with database connectivity check
  - Add /ready endpoint for Kubernetes readiness probes
  - Include dependency health checks (Redis, gRPC connections)
  - Purpose: Enable proper health monitoring and deployment orchestration
  - _Leverage: Health check patterns, dependency validation_
  - _Requirements: Reliability, deployment automation_

## Implementation Notes

**Task Dependencies:** Tasks are organized in phases with clear dependencies. Phase 1-2 establish structure and models, Phase 3-4 add data schemas and security, Phase 5-6 implement business logic, Phase 7-8 add API layers, Phase 9-10 handle configuration and communication, Phase 11 covers testing, Phase 12 manages deployment, and Phase 13 adds observability.

**Parallel Execution:** Tasks within the same phase can often be executed in parallel, especially between the two services. For example, tasks 8-11 (User Management models) can run parallel to tasks 12-18 (CRM Management models).

**Security Implementation:** Security tasks (19-22) are prioritized early to ensure all subsequent components have proper security foundations including audit logging, tenant isolation, and security event tracking.

**Testing Strategy:** Unit tests focus on individual components (55-56, 58-59), integration tests verify service interactions (57, 60), and the complete test suite ensures multi-tenant isolation and security compliance.

**Quality Gates:** Each phase should be validated before proceeding to the next. Database migrations should be tested, API endpoints should be validated, security features should be verified, and all tests should pass before deployment configuration.