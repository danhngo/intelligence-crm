# CRM Platform Postman Collections

This directory contains comprehensive Postman collections for all microservices in the CRM platform. You can import these JSON files into Postman to test and interact with all APIs.

## 📁 Available Collections

### Individual Service Collections
1. **`00-combined-all-services.json`** - 🌟 **RECOMMENDED** - Complete collection with all services in one file
2. **`01-communication-hub-api.json`** - Email templates, campaigns, messages (Port 8003)
3. **`02-crm-core-api.json`** - Contact management (Port 8000)
4. **`03-user-management-api.json`** - Authentication and user management (Port 8002)
5. **`04-analytics-service-api.json`** - Analytics, metrics, and reporting (Port 8004)
6. **`05-ai-orchestration-api.json`** - AI/ML workflows and predictions (Port 8005)
7. **`06-workflow-engine-api.json`** - Business process automation (Port 8001)

## 🚀 Quick Start

### 1. Import Collections
- Open Postman
- Click **Import** button
- Drag and drop the JSON files or select them
- **Recommended**: Start with `00-combined-all-services.json` for everything in one collection

### 2. Set Environment Variables
The collections use variables for flexibility. You can either:
- Use the default localhost URLs (works if running services locally)
- Create a Postman environment with custom values

**Default Variables:**
```
crmCoreUrl = http://localhost:8000
workflowEngineUrl = http://localhost:8001  
userManagementUrl = http://localhost:8002
communicationHubUrl = http://localhost:8003
analyticsUrl = http://localhost:8004
aiOrchestrationUrl = http://localhost:8005
auth_token = test-auth-token-123
```

### 3. Authentication
Most endpoints require authentication. The collections include:
- **Bearer Token Authentication** (pre-configured with test token)
- **Login endpoint** to get real tokens
- **Registration endpoint** for new users

**Test Authentication:**
1. Use the login request in the Authentication folder (uses form data format)
2. Default test credentials: `test@example.com` / `test12345`
3. Copy the returned `access_token` from the response
4. Update the `auth_token` variable or collection auth settings

## 📋 Service Overview

### 🔐 User Management (Port 8002)
- **Authentication**: Login, register, logout, password reset
- **User Management**: CRUD operations, roles, activation
- **Authorization**: Token validation, current user info

### 👥 CRM Core (Port 8000) 
- **Contact Management**: Create, read, update, delete contacts
- **Search & Filter**: Advanced contact search and filtering
- **Bulk Operations**: Import/export contacts in batch
- **Data Enrichment**: Custom fields, tags, notes

### 📧 Communication Hub (Port 8003)
- **Email Templates**: Template management with variables
- **Campaigns**: Email campaign creation and management  
- **Messages**: Direct message sending
- **Channels**: Communication channel management
- **Analytics Integration**: Campaign performance tracking

### 📈 Analytics Service (Port 8004)
- **Dashboard Metrics**: Real-time KPIs and metrics
- **Campaign Analytics**: Email performance, engagement rates
- **Contact Analytics**: Contact growth, segmentation
- **Event Tracking**: Custom event logging and analysis
- **Reports**: Automated report generation

### 🤖 AI Orchestration (Port 8005)
- **AI Workflows**: Automated AI-driven processes
- **Model Management**: Deploy and manage ML models
- **Predictions**: Real-time and batch predictions
- **Training**: Model training and retraining
- **Lead Scoring**: Automated lead qualification

### ⚡ Workflow Engine (Port 8001)
- **Workflow Management**: Create complex automation workflows
- **Triggers**: Event-based workflow activation
- **Execution Tracking**: Monitor workflow runs
- **Testing**: Dry-run workflows before deployment
- **Statistics**: Performance analytics for workflows

## 🏗️ API Architecture

### Service Ports
- **CRM Core**: 8000 - Customer data management
- **Workflow Engine**: 8001 - Process automation  
- **User Management**: 8002 - Authentication & users
- **Communication Hub**: 8003 - Email & messaging
- **Analytics**: 8004 - Metrics & reporting
- **AI Orchestration**: 8005 - Machine learning

### Common Patterns
- **Health Checks**: `/health` endpoint on all services
- **API Versioning**: `/api/v1/` prefix for all endpoints
- **Authentication**: Bearer token in Authorization header
- **Pagination**: `skip` and `limit` parameters
- **Filtering**: Query parameters for search and filter
- **CORS**: Enabled for web application integration

## 📝 Example Usage Workflows

### 1. Complete User Onboarding
```
1. Register User (User Management)
2. Create Contact (CRM Core) 
3. Create Welcome Template (Communication Hub)
4. Create Welcome Campaign (Communication Hub)
5. Create Automation Workflow (Workflow Engine)
6. Track Engagement Events (Analytics)
```

### 2. Campaign Management
```
1. Create Email Template (Communication Hub)
2. Create Campaign with Template (Communication Hub)
3. Start Campaign (Communication Hub)
4. Track Campaign Events (Analytics)
5. Analyze Campaign Performance (Analytics)
```

### 3. AI-Powered Lead Scoring
```
1. Create Lead Scoring Model (AI Orchestration)
2. Create Scoring Workflow (AI Orchestration)
3. Trigger Predictions (AI Orchestration)
4. Update Contact Scores (CRM Core)
5. Analyze Results (Analytics)
```

## 🔧 Troubleshooting

### Common Issues
1. **401 Unauthorized**: Update the `auth_token` variable with a valid token
2. **Connection Refused**: Ensure services are running on the correct ports
3. **404 Not Found**: Check if the API endpoint exists and service is running
4. **422 Validation Error**: Verify request body matches the expected schema

### Service Dependencies
- All services require their respective databases (PostgreSQL)
- Analytics service requires Redis for caching
- AI Orchestration requires both PostgreSQL and Redis
- Services communicate via HTTP APIs

### Development Setup
```bash
# Start all services
docker-compose up -d

# Check service health
curl http://localhost:8000/health  # CRM Core
curl http://localhost:8001/health  # Workflow Engine  
curl http://localhost:8002/health  # User Management
curl http://localhost:8003/health  # Communication Hub
curl http://localhost:8004/health  # Analytics
curl http://localhost:8005/health  # AI Orchestration
```

## 📚 Additional Resources

- **API Documentation**: Each service provides OpenAPI docs at `/api/v1/docs`
- **Health Monitoring**: Use the health check requests to monitor service status
- **Database Schema**: Check the `migrations/` folder in each service
- **Environment Variables**: See `docker-compose.yml` for configuration options

## 🤝 Contributing

When adding new API endpoints:
1. Update the corresponding service collection
2. Add examples to the combined collection
3. Update this README with new functionality
4. Test all requests before committing

---

**Happy API Testing! 🚀**