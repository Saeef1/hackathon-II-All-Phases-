# Data Model: Task Management API

**Feature**: 1-task-management
**Date**: 2026-02-02

## Entity Definitions

### Task Entity
The Task entity represents a user's task with the following attributes:

#### Fields
- **id** (UUID, Primary Key)
  - Type: UUID (auto-generated)
  - Constraints: Not null, Unique
  - Description: Globally unique identifier for the task

- **user_id** (UUID, Foreign Key)
  - Type: UUID
  - Constraints: Not null, Indexed
  - Description: References the authenticated user from JWT token
  - Note: Value comes from JWT claims, not client input

- **title** (String)
  - Type: String(255)
  - Constraints: Not null, Length 1-255
  - Description: Task title/description

- **description** (String)
  - Type: String(1000)
  - Constraints: Nullable
  - Description: Optional detailed description of the task

- **completed** (Boolean)
  - Type: Boolean
  - Constraints: Not null, Default: false
  - Description: Completion status of the task

- **created_at** (DateTime)
  - Type: DateTime (UTC)
  - Constraints: Not null, Auto-generated
  - Description: Timestamp when task was created

- **updated_at** (DateTime)
  - Type: DateTime (UTC)
  - Constraints: Not null, Auto-updated
  - Description: Timestamp when task was last modified

#### Indexes
- Primary Index: id
- User Query Index: user_id (for efficient user-scoped queries)

#### Constraints
- All tasks must belong to a valid user_id (from JWT)
- Title must be 1-255 characters
- user_id must match the authenticated user from JWT token

### Relationships
- Each Task belongs to exactly one User (identified by user_id from JWT)
- One User can have many Tasks (0 or more)
- No direct User entity needed since user identity comes from JWT

## Database Schema

### SQL Definition
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index for user-scoped queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

## Validation Rules

### Field Validation
- id: Auto-generated, never client-provided
- user_id: Must match authenticated user from JWT (never client-provided)
- title: Required, 1-255 characters
- description: Optional, max 1000 characters
- completed: Boolean, defaults to false
- created_at: Server-generated timestamp
- updated_at: Server-generated and updated timestamp

### Business Rules
- Tasks can only be accessed by the user who owns them
- User identity is validated against JWT claims
- No cross-user access allowed at any level
- Updates must preserve user_id integrity

## State Transitions

### Task States
- **Pending**: completed = false (default)
- **Completed**: completed = true

### Operations
- **Create**: New task with completed = false
- **Update**: Modify any field except user_id and id
- **Toggle Completion**: Change completed status via PATCH
- **Delete**: Remove task permanently

## API Representation

### JSON Format
```json
{
  "id": "uuid-string",
  "user_id": "user-uuid-from-jwt",
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "created_at": "2026-02-02T10:00:00Z",
  "updated_at": "2026-02-02T10:00:00Z"
}
```

## Security Considerations

### Data Isolation
- All queries must filter by user_id from JWT
- Never trust client-provided user_id
- Database-level enforcement through application logic
- Validation at both API and database layers

### Access Control
- Read: Only tasks belonging to authenticated user
- Write: Only tasks belonging to authenticated user
- Delete: Only tasks belonging to authenticated user
- No global or cross-user queries allowed