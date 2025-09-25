# User Management Service

This service provides user authentication, authorization, and management capabilities for the CRM platform.

## Features

- User authentication with JWT tokens
- Role-based access control (RBAC)
- User management (CRUD operations)
- Permission management
- Password hashing with bcrypt
- Email verification
- Session management with Redis
- PostgreSQL database with async support
- API documentation with OpenAPI/Swagger

## Getting Started

### Prerequisites

- Python 3.11+
- Poetry
- PostgreSQL
- Redis

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   poetry install
   ```

3. Set up environment variables in `.env` file
4. Run database migrations:
   ```bash
   poetry run alembic upgrade head
   ```

### Running the Service

```bash
poetry run uvicorn app.main:app --reload
```

The service will be available at `http://localhost:8000`.
API documentation is available at `http://localhost:8000/docs`.

### Running with Docker

```bash
docker-compose up -d
```

## API Documentation

### Authentication Endpoints

- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/register` - Register new user

### User Management Endpoints

- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users` - List all users (admin only)
- `POST /api/v1/users` - Create user (admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user (admin only)
- `DELETE /api/v1/users/{user_id}` - Delete user (admin only)

## Testing

```bash
poetry run pytest
```

## License

MIT
