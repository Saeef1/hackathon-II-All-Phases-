# Todo Full-Stack Web Application - Authentication System

This project implements a secure authentication system using Better Auth and JWT tokens for identity verification between the Next.js frontend and FastAPI backend.

## Architecture Overview

### Frontend Authentication Layer (Next.js + Better Auth)
- Configured Better Auth with JWT plugin and shared secret
- Implemented user signup and signin flows
- Securely manages session (Better Auth managed)
- Exposes JWT access for API calls

### Frontend API Client Layer
- Centralized API client module (`frontend/src/services/api.js`)
- Automatic attachment of Authorization: Bearer <JWT> headers
- Handles auth errors (redirect on 401, clears invalid sessions)
- Ensures no API call is made without token

### Backend Authentication Middleware (FastAPI)
- Middleware extracts Authorization header
- Validates JWT signature using shared secret
- Verifies token expiration
- Decodes user claims (user_id, email)
- Rejects invalid or missing tokens with 401

### Identity Enforcement Layer
- Compares authenticated user_id (from JWT) with user_id in API route
- Rejects mismatches with 403 Forbidden
- Ensures identity comes only from token, never client input

### Cross-Service Secret Management
- BETTER_AUTH_SECRET stored as environment variable
- Same secret configured in Next.js and FastAPI runtimes
- No hardcoded secrets in code

## Key Files

### Backend
- `backend/src/models/auth.py` - User model and authentication schemas
- `backend/src/services/auth.py` - Authentication service layer
- `backend/src/api/deps.py` - Authentication dependencies/middleware
- `backend/src/api/auth.py` - Authentication API endpoints
- `backend/src/api/todos.py` - Todo API with user identity enforcement
- `backend/src/core/security.py` - Password hashing utilities

### Frontend
- `frontend/src/lib/auth.js` - Better Auth configuration
- `frontend/src/services/api.js` - API client with JWT handling
- `frontend/src/components/auth/AuthProvider.jsx` - Authentication context provider
- `frontend/src/components/auth/ProtectedRoute.jsx` - Route protection component
- `frontend/pages/auth/sign-in.js` - Sign in page
- `frontend/pages/auth/sign-up.js` - Sign up page
- `frontend/pages/_app.js` - App wrapper with auth context

## Security Features

1. **Stateless Authentication**: Uses JWT tokens for stateless authentication
2. **Identity Verification**: Backend verifies user identity from token, not client input
3. **Cross-User Access Prevention**: Backend enforces that users can only access their own data
4. **Token Expiration**: JWT tokens have configurable expiration times
5. **Secure Password Storage**: Passwords are hashed using bcrypt

## Setup Instructions

1. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

3. Copy the environment variables:
```bash
cp .env.example .env
```

4. Update the environment variables with your actual values, especially:
   - `BETTER_AUTH_SECRET`: A strong secret key for JWT signing
   - `NEON_DATABASE_URL`: Your Neon PostgreSQL connection string

## Running the Application

1. Start the backend:
```bash
cd backend
uvicorn src.main:app --reload
```

2. Start the frontend:
```bash
cd frontend
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login user and get JWT token
- `GET /api/v1/auth/me` - Get current user info from JWT token

### Todos
- `GET /api/v1/todos/` - Get todos for current user
- `POST /api/v1/todos/` - Create a new todo for current user
- `GET /api/v1/todos/{todo_id}` - Get a specific todo
- `PUT /api/v1/todos/{todo_id}` - Update a specific todo
- `DELETE /api/v1/todos/{todo_id}` - Delete a specific todo

All todo endpoints require authentication and enforce user identity.