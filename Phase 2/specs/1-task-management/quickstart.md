# Quickstart Guide: Task Management API

**Feature**: 1-task-management
**Date**: 2026-02-02

## Prerequisites

- Python 3.8+
- pip package manager
- Neon Serverless PostgreSQL database
- JWT secret key for token validation

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi sqlmodel psycopg2-binary python-jose[cryptography] python-multipart uvicorn
```

### 4. Environment Configuration
Create a `.env` file with the following variables:

```env
DATABASE_URL=postgresql://username:password@host:port/database_name
JWT_SECRET_KEY=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Initialize Database
Create a database initialization script:

```python
# init_db.py
from sqlmodel import SQLModel, create_engine
from models import Task  # Import your Task model

def init_db():
    engine = create_engine("postgresql://username:password@host:port/database_name")
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
```

Run the initialization:
```bash
python init_db.py
```

## Running the Server

### Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Usage Examples

### Authentication Headers
All requests must include a valid JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token-here>
```

### Example Requests

#### Create a Task
```bash
curl -X POST \
  http://localhost:8000/api/user123/tasks \
  -H 'Authorization: Bearer your-jwt-token' \
  -H 'Content-Type: application/json' \
  -d '{"title": "Complete project", "description": "Finish the backend API"}'
```

#### Get All Tasks
```bash
curl -X GET \
  http://localhost:8000/api/user123/tasks \
  -H 'Authorization: Bearer your-jwt-token'
```

#### Update a Task
```bash
curl -X PUT \
  http://localhost:8000/api/user123/tasks/task456 \
  -H 'Authorization: Bearer your-jwt-token' \
  -H 'Content-Type: application/json' \
  -d '{"title": "Updated task", "description": "Updated description", "completed": false}'
```

#### Toggle Task Completion
```bash
curl -X PATCH \
  http://localhost:8000/api/user123/tasks/task456/complete \
  -H 'Authorization: Bearer your-jwt-token' \
  -H 'Content-Type: application/json' \
  -d '{"completed": true}'
```

## Testing the API

### Verify Authentication
Test that endpoints reject unauthorized requests:

```bash
curl -X GET http://localhost:8000/api/user123/tasks
# Should return 401 Unauthorized
```

### Verify User Isolation
Test that users cannot access other users' tasks:

```bash
# Authenticate as user A
# Try to access user B's tasks using user A's token
# Should return 403 Forbidden
```

## Configuration Options

### JWT Settings
- `JWT_SECRET_KEY`: Secret key for signing/verifying JWTs
- `ALGORITHM`: Algorithm for JWT (recommended: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Database Settings
- `DATABASE_URL`: Connection string for Neon PostgreSQL
- Connection pooling is configured automatically

### Server Settings
- Port: 8000 (default)
- Host: 0.0.0.0 (accessible from network)
- Reload: Enabled in development mode

## Troubleshooting

### Common Issues
1. **500 Internal Server Error**: Check server logs for detailed error messages
2. **401 Unauthorized**: Verify JWT token is valid and properly formatted
3. **403 Forbidden**: Ensure the user_id in URL matches the user_id in JWT token
4. **503 Service Unavailable**: Check database connectivity

### Logs
Server logs will show:
- Request details
- Authentication status
- Database errors
- Performance metrics