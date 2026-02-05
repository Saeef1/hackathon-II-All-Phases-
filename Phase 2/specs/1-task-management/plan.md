# Implementation Plan: Backend Task Management API

**Feature**: 1-task-management
**Created**: 2026-02-02
**Status**: Draft
**Plan Version**: 1.0.0

## Technical Context

### Known Elements
- **Backend Framework**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT verification via shared secret
- **API Style**: REST
- **Required Endpoints**:
  - GET    /api/{user_id}/tasks
  - POST   /api/{user_id}/tasks
  - GET    /api/{user_id}/tasks/{id}
  - PUT    /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
  - PATCH  /api/{user_id}/tasks/{id}/complete

### Key Entities
- **Task**: id, user_id, title, description, completed, created_at, updated_at
- **User**: Identified by user_id from JWT token
- **JWT Token**: Contains user identity, validated with shared secret

### Architecture Components
1. **Database Layer**: Neon PostgreSQL with SQLModel
2. **Authentication Layer**: JWT verification middleware
3. **Authorization Layer**: User ownership validation
4. **API Layer**: REST endpoints with proper HTTP responses
5. **Data Access Layer**: User-scoped queries

## Constitution Check

### Compliance Verification
- ✅ Security-First Design: JWT signature verification on every request
- ✅ Deterministic Behavior: User identity from JWT claims only
- ✅ Spec-Driven Development: Following approved spec
- ✅ Identity Propagation: URL user_id matches JWT user identity
- ✅ Backend Framework: FastAPI (Python) as required
- ✅ Statelessness: No backend session storage
- ✅ JWT Expiration: Will enforce expiration validation
- ✅ Endpoint Protection: All endpoints require authentication

### Potential Violations
None identified - all requirements align with constitution.

## Phase 0: Research & Resolution

### Research Requirements
1. FastAPI JWT authentication middleware implementation
2. SQLModel best practices for Neon PostgreSQL
3. Task entity relationship patterns with user ownership
4. Proper HTTP status code handling in FastAPI
5. JWT token validation with shared secret in Python

## Phase 1: Design & Contracts

### Data Model: data-model.md

#### Task Entity
- **id**: UUID primary key, auto-generated
- **user_id**: UUID foreign key, references authenticated user from JWT
- **title**: String(255), required, non-empty
- **description**: String(1000), optional, nullable
- **completed**: Boolean, default False
- **created_at**: DateTime, auto-generated
- **updated_at**: DateTime, auto-generated and updated

#### Relationships
- Each Task belongs to exactly one User (via user_id from JWT)
- Users can have zero or many Tasks
- Data isolation enforced at database query level

#### Validation Rules
- title must be 1-255 characters
- user_id must match authenticated user from JWT
- completed must be boolean
- created_at and updated_at are server-controlled timestamps

### API Contracts

#### Authentication Contract
- All endpoints require `Authorization: Bearer <JWT_TOKEN>` header
- JWT must be valid and not expired
- User identity extracted from JWT claims
- URL `{user_id}` must match user_id in JWT

#### GET /api/{user_id}/tasks
- **Method**: GET
- **Auth Required**: Yes
- **Path Params**: user_id (must match JWT user_id)
- **Query Params**: None
- **Response**: 200 OK with array of Task objects
- **Errors**: 401 Unauthorized, 403 Forbidden
- **Behavior**: Returns all tasks for authenticated user

#### POST /api/{user_id}/tasks
- **Method**: POST
- **Auth Required**: Yes
- **Path Params**: user_id (must match JWT user_id)
- **Body**: { title: string, description?: string }
- **Response**: 201 Created with created Task object
- **Errors**: 400 Bad Request, 401 Unauthorized, 403 Forbidden
- **Behavior**: Creates new task for authenticated user

#### GET /api/{user_id}/tasks/{id}
- **Method**: GET
- **Auth Required**: Yes
- **Path Params**: user_id (must match JWT user_id), id (task id)
- **Response**: 200 OK with Task object
- **Errors**: 401 Unauthorized, 403 Forbidden, 404 Not Found
- **Behavior**: Returns specific task for authenticated user

#### PUT /api/{user_id}/tasks/{id}
- **Method**: PUT
- **Auth Required**: Yes
- **Path Params**: user_id (must match JWT user_id), id (task id)
- **Body**: { title: string, description?: string, completed?: boolean }
- **Response**: 200 OK with updated Task object
- **Errors**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
- **Behavior**: Updates entire task for authenticated user

#### DELETE /api/{user_id}/tasks/{id}
- **Method**: DELETE
- **Auth Required**: Yes
- **Path Params**: user_id (must match JWT user_id), id (task id)
- **Response**: 204 No Content
- **Errors**: 401 Unauthorized, 403 Forbidden, 404 Not Found
- **Behavior**: Deletes specific task for authenticated user

#### PATCH /api/{user_id}/tasks/{id}/complete
- **Method**: PATCH
- **Auth Required**: Yes
- **Path Params**: user_id (must match JWT user_id), id (task id)
- **Body**: { completed: boolean }
- **Response**: 200 OK with updated Task object
- **Errors**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
- **Behavior**: Toggles completion status for authenticated user's task

### Quickstart Guide: quickstart.md

#### Setup Instructions
1. Install dependencies: `pip install fastapi sqlmodel psycopg2-binary python-jose[cryptography] python-multipart`
2. Set environment variables:
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `JWT_SECRET_KEY`: Shared secret for JWT verification
   - `ALGORITHM`: JWT algorithm (recommended: HS256)
3. Initialize database: `python init_db.py`
4. Start server: `uvicorn main:app --reload`

#### Configuration
- JWT token validation using shared secret
- Database connection pooling for Neon
- CORS middleware for frontend integration
- Logging for debugging and monitoring

## Phase 2: Implementation Strategy

### Component Breakdown
1. **Database Models** (Day 1)
   - Task model with proper constraints
   - Database session management
   - Connection initialization for Neon

2. **Authentication Middleware** (Day 1)
   - JWT verification utility
   - User identity extraction
   - Authentication dependency

3. **Authorization Logic** (Day 1)
   - User ownership validation
   - Cross-user access prevention

4. **API Routes** (Day 2)
   - Implement all 6 required endpoints
   - Proper request validation
   - Response formatting

5. **Data Access Layer** (Day 2)
   - User-scoped queries
   - Error handling
   - Transaction management

6. **Testing** (Day 3)
   - Unit tests for authentication
   - Integration tests for all endpoints
   - Security tests for data isolation

### Risk Mitigation
- **JWT Validation**: Implement robust token validation with proper error handling
- **Data Isolation**: Enforce user scoping at both application and database levels
- **Performance**: Implement proper indexing and query optimization
- **Security**: Validate all inputs and sanitize outputs

### Success Criteria Verification
- All 6 endpoints implemented and tested
- JWT authentication working correctly
- User data isolation verified
- Proper HTTP status codes returned
- Persistence working with Neon PostgreSQL
- Performance meeting requirements (<500ms response time)

## Dependencies

### External Services
- Neon Serverless PostgreSQL
- Better Auth (for JWT generation - frontend responsibility)

### Libraries
- FastAPI: Web framework
- SQLModel: ORM and database modeling
- python-jose: JWT handling
- uvicorn: ASGI server

### Environment Variables
- `DATABASE_URL`: Neon PostgreSQL connection string
- `JWT_SECRET_KEY`: Shared secret for JWT verification
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time