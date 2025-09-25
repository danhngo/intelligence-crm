# Analytics Service

A comprehensive analytics service for the CRM platform that provides real-time analytics, metrics aggregation, and dashboard capabilities.

## Features

- **Event Tracking**: Real-time event collection and processing
- **Message Analytics**: Sentiment analysis, intent detection, and response time tracking
- **Conversation Analytics**: Aggregated conversation metrics and insights
- **Channel Analytics**: Channel performance and health monitoring
- **Dashboard Metrics**: Real-time dashboard with key performance indicators
- **Multi-tenant Support**: Tenant-isolated analytics and metrics
- **Caching**: Redis-powered caching for high-performance analytics
- **Time-series Data**: Hourly and daily aggregated metrics

## Technology Stack

- **FastAPI**: Modern async web framework
- **PostgreSQL**: Primary database for analytics data
- **Redis**: Caching and real-time metrics
- **SQLAlchemy**: Async ORM with modern type hints
- **Pydantic**: Data validation and serialization
- **Docker**: Containerization and deployment

## API Endpoints

### Events
- `POST /api/v1/analytics/events` - Create analytics event
- `POST /api/v1/analytics/events/bulk` - Create multiple events

### Message Analytics
- `POST /api/v1/analytics/messages/analytics` - Process message analytics

### Conversation Analytics
- `GET /api/v1/analytics/conversations/{id}/analytics` - Get conversation analytics

### Channel Analytics
- `GET /api/v1/analytics/channels/{id}/analytics` - Get channel analytics

### Dashboard
- `GET /api/v1/analytics/dashboard` - Get dashboard metrics

### Health
- `GET /health` - Health check endpoint

## Quick Start

1. **Environment Setup**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start Services**:
   ```bash
   docker-compose up -d
   ```

3. **Access API Documentation**:
   ```
   http://localhost:8004/docs
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `DEBUG` | Debug mode | `false` |
| `ANALYTICS_PORT` | Service port | `8004` |

## Data Models

### Event
Tracks individual events with type, data, and metadata.

### MessageAnalytics
Per-message analytics including sentiment, intent, and response time.

### ConversationAnalytics
Aggregated conversation metrics and performance data.

### ChannelAnalytics
Channel-level performance and health metrics.

## Usage Examples

### Track an Event
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8004/api/v1/analytics/events",
        json={
            "event_type": "message_sent",
            "event_data": {"channel_id": "123", "user_id": "456"},
            "tenant_id": "tenant-1"
        },
        params={"tenant_id": "tenant-1"}
    )
```

### Get Dashboard Metrics
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(
        "http://localhost:8004/api/v1/analytics/dashboard",
        params={"tenant_id": "tenant-1", "period": "day"}
    )
```

## Integration with Communication Hub

The analytics service integrates seamlessly with the communication hub service:

1. **Automatic Event Tracking**: Messages automatically generate analytics events
2. **Real-time Processing**: Events are processed and cached for immediate availability
3. **Webhook Support**: Communication hub can send analytics data via webhooks
4. **Batch Processing**: Bulk event creation for high-volume scenarios

## Performance Considerations

- **Caching Strategy**: Redis caching for frequently accessed metrics
- **Time-series Optimization**: Partitioned tables for time-series data
- **Batch Processing**: Bulk operations for high-volume analytics
- **Connection Pooling**: Optimized database and Redis connections

## Monitoring and Health Checks

- **Health Endpoint**: `/health` for service health monitoring
- **Database Connectivity**: Automatic database connection health checks
- **Cache Connectivity**: Redis connection monitoring
- **Resource Metrics**: CPU and memory usage tracking

## Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
black app/
isort app/
flake8 app/
```

### Database Migrations
```bash
alembic upgrade head
```

## Production Deployment

### Docker Compose Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment
See `k8s/` directory for Kubernetes manifests.

### Environment-specific Configurations
- Development: Local PostgreSQL and Redis
- Staging: Cloud-managed databases with connection pooling
- Production: Highly available setup with read replicas

## License

MIT License - see LICENSE file for details.
