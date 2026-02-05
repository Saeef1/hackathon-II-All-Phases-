# Data Model: Frontend Application & API Integration

**Feature**: 2-frontend-api-integration
**Date**: 2026-02-02

## Entity Definitions

### Task Entity (Consumed from Backend API)
The Task entity represents a user's task as consumed from the backend API:

#### Fields
- **id** (string)
  - Type: UUID string
  - Constraints: Not null, Unique
  - Description: Globally unique identifier for the task

- **title** (string)
  - Type: String(255)
  - Constraints: Not null, Length 1-255
  - Description: Task title/description displayed in UI

- **description** (string)
  - Type: String(1000)
  - Constraints: Nullable
  - Description: Optional detailed description of the task

- **completed** (boolean)
  - Type: Boolean
  - Constraints: Not null, Default: false
  - Description: Completion status of the task

- **created_at** (datetime string)
  - Type: ISO 8601 datetime string
  - Constraints: Not null
  - Description: Timestamp when task was created

- **updated_at** (datetime string)
  - Type: ISO 8601 datetime string
  - Constraints: Not null
  - Description: Timestamp when task was last modified

#### Validation Rules
- id: Received from backend, never client-generated
- title: Required, 1-255 characters
- description: Optional, max 1000 characters
- completed: Boolean, defaults to false
- created_at: Server-generated timestamp
- updated_at: Server-generated and updated timestamp

### User Entity (Managed by Better Auth)
The User entity represents the authenticated user managed by Better Auth:

#### Fields
- **id** (string)
  - Type: UUID string
  - Constraints: Not null, Unique
  - Description: Unique identifier for the authenticated user

- **email** (string)
  - Type: Email string
  - Constraints: Not null, Valid email format
  - Description: User's email address for authentication

- **jwtToken** (string)
  - Type: JWT token string
  - Constraints: Not null when authenticated
  - Description: JWT token for authenticating backend API requests

#### Validation Rules
- id: Provided by Better Auth, used for API requests
- email: Validated by Better Auth
- jwtToken: Validated by Better Auth, attached to API requests

### Session Entity (Managed by Better Auth)
The Session entity represents the user's authentication state:

#### Fields
- **userId** (string)
  - Type: User ID string
  - Constraints: Not null when authenticated
  - Description: Links session to user

- **expiresAt** (datetime string)
  - Type: ISO 8601 datetime string
  - Constraints: Not null when authenticated
  - Description: Expiration time for the session

- **accessToken** (string)
  - Type: JWT access token string
  - Constraints: Not null when authenticated
  - Description: Token for authenticating API requests

#### Validation Rules
- userId: Matches authenticated user
- expiresAt: Checked before making API requests
- accessToken: Attached to all backend API requests

## API Representation

### Task JSON Format (from backend API)
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

### Frontend Task Format (internal representation)
```typescript
interface FrontendTask {
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```

## State Management

### Local State Structure
The frontend maintains local state synchronized with the backend:

#### Task List State
```typescript
interface TaskListState {
  tasks: FrontendTask[];
  loading: boolean;
  error: string | null;
  filters: {
    completed: 'all' | 'completed' | 'pending';
  };
}
```

#### Current User State
```typescript
interface CurrentUserState {
  user: {
    id: string;
    email: string;
  } | null;
  isAuthenticated: boolean;
  loading: boolean;
}
```

## Security Considerations

### Data Isolation
- All API requests use JWT token from Better Auth session
- User context derived from auth state, not client input
- No user_id exposed as editable input in forms
- Backend enforces user data isolation at API level

### Session Management
- Session expiration handled by Better Auth
- Automatic redirect to sign-in on token expiration
- Secure storage of JWT tokens in Better Auth session
- No sensitive data stored in browser localStorage

### API Communication
- All API requests include Authorization: Bearer <token> header
- 401 responses trigger session cleanup and redirect to sign-in
- 403 responses show access denied messages
- Error states properly handled in UI components