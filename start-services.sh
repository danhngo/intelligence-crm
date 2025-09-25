#!/bin/bash

# CRM Platform Service Startup Script
echo "🚀 Starting CRM Platform Services..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

echo -e "${BLUE}📡 Creating Docker network...${NC}"
docker network create crm-network 2>/dev/null || true

echo ""
echo -e "${YELLOW}🔧 Step 1: Starting Database Services...${NC}"

# Start User Management DB & Redis
echo "   → Starting User Management infrastructure..."
cd /Users/admin/2.learning/5.ai_ml/langchain/claude-code-langchain/services/user-management
docker-compose up -d db redis

# Start Analytics DB & Redis  
echo "   → Starting Analytics infrastructure..."
cd /Users/admin/2.learning/5.ai_ml/langchain/claude-code-langchain/services/analytics-service
docker-compose up -d db redis

# Start CRM Core DB & Redis
echo "   → Starting CRM Core infrastructure..."
cd /Users/admin/2.learning/5.ai_ml/langchain/claude-code-langchain/services/crm-core
docker-compose up -d db redis

echo ""
echo -e "${YELLOW}🔧 Step 2: Waiting for databases to be ready...${NC}"
sleep 15

echo ""
echo -e "${YELLOW}🔧 Step 3: Starting Backend Services...${NC}"

# Start User Management API
echo "   → Starting User Management API..."
cd /Users/admin/2.learning/5.ai_ml/langchain/claude-code-langchain/services/user-management
docker-compose up -d app

# Start Analytics Service API
echo "   → Starting Analytics Service API..."
cd /Users/admin/2.learning/5.ai_ml/langchain/claude-code-langchain/services/analytics-service
docker-compose up -d analytics

# Start CRM Core API
echo "   → Starting CRM Core API..."
cd /Users/admin/2.learning/5.ai_ml/langchain/claude-code-langchain/services/crm-core
docker-compose up -d crm

echo ""
echo -e "${YELLOW}🔧 Step 4: Waiting for services to initialize...${NC}"
sleep 10

echo ""
echo -e "${GREEN}🎉 Services Started! Here's the status:${NC}"
echo ""

# Check service health
services=(
    "user-management-api:8002"
    "analytics-service-api:8004" 
    "crm-postgres:5432"
    "user-postgres:5434"
    "analytics-postgres:5435"
)

echo -e "${BLUE}📊 Service Status:${NC}"
for service_info in "${services[@]}"; do
    name=$(echo $service_info | cut -d':' -f1)
    port=$(echo $service_info | cut -d':' -f2)
    
    if docker ps --filter "name=$name" --filter "status=running" | grep -q "$name"; then
        echo -e "  ${GREEN}✅ $name${NC} - Running on port $port"
    else
        echo -e "  ${RED}❌ $name${NC} - Not running"
    fi
done

echo ""
echo -e "${GREEN}📱 Access Points:${NC}"
echo -e "   ${BLUE}Frontend:${NC}      http://localhost:3001"
echo -e "   ${BLUE}User API:${NC}      http://localhost:8002"
echo -e "   ${BLUE}Analytics:${NC}     http://localhost:8004"
echo ""
echo -e "${YELLOW}📋 Useful Commands:${NC}"
echo "   View logs:         docker-compose logs -f <service>"
echo "   Stop all:          docker stop \$(docker ps -aq)"
echo "   Restart service:   docker-compose restart <service>"
echo ""
echo -e "${GREEN}🔍 Next Steps:${NC}"
echo "   1. Visit http://localhost:3001 for the frontend"
echo "   2. Check API health at http://localhost:8002/health"
echo "   3. View service logs if needed: docker-compose logs -f"

# Return to original directory
cd /Users/admin/2.learning/5.ai_ml/langchain/claude-code-langchain
