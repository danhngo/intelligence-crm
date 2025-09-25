#!/bin/bash

# CRM Platform Startup Script
echo "🚀 Starting CRM Platform..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ Docker Compose is not installed."
    exit 1
fi

# Create network if it doesn't exist
echo "📡 Creating Docker network..."
docker network create crm-network 2>/dev/null || true

# Build and start all services
echo "🔧 Building and starting services..."
echo "   This may take a few minutes on first run..."

docker-compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🔍 Checking service status..."

services=(
    "crm-frontend:3000"
    "crm-core-api:8000"
    "workflow-engine-api:8001"
    "user-management-api:8002"
    "communication-hub-api:8003"
    "analytics-service-api:8004"
    "ai-orchestration-api:8005"
)

echo "📊 Service Status:"
for service in "${services[@]}"; do
    name=$(echo $service | cut -d':' -f1)
    port=$(echo $service | cut -d':' -f2)
    
    if docker ps --filter "name=$name" --filter "status=running" | grep -q "$name"; then
        echo "  ✅ $name - Running on port $port"
    else
        echo "  ❌ $name - Not running"
    fi
done

echo ""
echo "🎉 CRM Platform is starting up!"
echo ""
echo "📱 Access Points:"
echo "   Frontend:     http://localhost:3000"
echo "   CRM Core:     http://localhost:8000"
echo "   Workflow:     http://localhost:8001"
echo "   User Mgmt:    http://localhost:8002"
echo "   Messages:     http://localhost:8003"
echo "   Analytics:    http://localhost:8004"
echo "   AI Services:  http://localhost:8005"
echo ""
echo "📋 Useful Commands:"
echo "   View logs:    docker-compose logs -f"
echo "   Stop all:     docker-compose down"
echo "   Restart:      docker-compose restart"
echo ""
echo "🔍 Check service health:"
echo "   docker-compose ps"
