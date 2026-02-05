# Implementation Plan: Frontend Application & API Integration (Next.js App Router)

**Feature**: 2-frontend-api-integration
**Created**: 2026-02-02
**Status**: Draft
**Plan Version**: 1.0.0

## Technical Context

### Known Elements
- **Frontend Framework**: Next.js 16+ (App Router)
- **Authentication**: Better Auth
- **API Communication**: REST over HTTP
- **Auth Mechanism**: JWT via Authorization header
- **Responsive Design**: Mobile-first approach
- **Required Pages**:
  - `/signin` - User sign-in page
  - `/signup` - User sign-up page
  - `/tasks` - Task list view
  - `/tasks/new` - Task creation form
  - `/tasks/[id]` - Individual task view/edit

### Key Entities
- **User**: Authenticated user managed by Better Auth
- **Task**: User's task data retrieved from backend API
- **JWT Token**: Stored in Better Auth session, attached to API requests

### Architecture Components
1. **Routing Layer**: Next.js App Router with public/protected routes
2. **Authentication Layer**: Better Auth integration and session management
3. **API Client Layer**: Centralized API client with JWT attachment
4. **State Management Layer**: React state and data synchronization
5. **UI Components Layer**: Reusable, responsive components
6. **Security Layer**: Route guards and data isolation

## Constitution Check

### Compliance Verification
- ✅ Security-First Design: JWT token validation and attachment to all API requests
- ✅ Deterministic Behavior: Consistent auth state management across the application
- ✅ Spec-Driven Development: Following approved frontend integration spec
- ✅ Identity Propagation: User context derived from auth state, not client input
- ✅ Frontend Framework: Next.js 16+ (App Router) as required
- ✅ Statelessness: No local session storage, relying on Better Auth
- ✅ JWT Handling: Proper token attachment to API requests
- ✅ Access Control: Route guards preventing unauthenticated access

### Potential Violations
None identified - all requirements align with constitution.

## Phase 0: Research & Resolution

### Research Requirements
1. Better Auth integration with Next.js App Router implementation
2. Next.js App Router protected route patterns and middleware
3. Centralized API client patterns with JWT token handling
4. Responsive UI component design with Tailwind CSS
5. Task data synchronization between local state and backend

## Phase 1: Design & Contracts

### Data Model: data-model.md

#### Task Entity (consumed from backend)
- **id**: Unique identifier from backend API
- **title**: String, required, displayed in UI
- **description**: String, optional, displayed in UI
- **completed**: Boolean, indicates completion status
- **created_at**: DateTime, displayed for user reference
- **updated_at**: DateTime, displayed for user reference

#### User Entity (managed by Better Auth)
- **email**: User's email address for authentication
- **id**: User ID from auth system (used for API requests)
- **session**: JWT token for API authentication

### API Contracts

#### Authentication Contract
- `/signin` and `/signup` pages accessible to unauthenticated users
- Protected routes require valid Better Auth session
- JWT token automatically attached to backend API requests
- Session expiration redirects to sign-in page

#### Task API Integration Contract
- **GET `/api/{user_id}/tasks`**: Retrieve user's tasks (authenticated)
- **POST `/api/{user_id}/tasks`**: Create new task (authenticated)
- **GET `/api/{user_id}/tasks/{id}`**: Retrieve specific task (authenticated)
- **PUT `/api/{user_id}/tasks/{id}`**: Update task (authenticated)
- **DELETE `/api/{user_id}/tasks/{id}`**: Delete task (authenticated)
- **PATCH `/api/{user_id}/tasks/{id}/complete`**: Toggle completion (authenticated)

### Quickstart Guide: quickstart.md

#### Setup Instructions
1. Install dependencies: `npm install next react react-dom @better-auth/react @better-auth/adapter-drizzle`
2. Configure Better Auth in `src/lib/auth.ts`
3. Set environment variables:
   - `NEXTAUTH_URL`: Application base URL
   - `BETTER_AUTH_SECRET`: Secret for JWT signing
   - `BACKEND_API_URL`: Backend API base URL
4. Initialize project: `npm run dev`
5. Start development server: `npm run dev`

#### Configuration
- Better Auth session management
- API client with JWT token attachment
- Responsive design with Tailwind CSS
- Component-based architecture

## Phase 2: Implementation Strategy

### Component Breakdown
1. **Authentication Setup** (Day 1)
   - Better Auth configuration
   - Session provider setup
   - Sign-in and sign-up pages
   - Route protection middleware

2. **API Client Layer** (Day 1)
   - Centralized API client module
   - JWT token attachment logic
   - Error handling implementation
   - Request/response interceptors

3. **Routing Layer** (Day 1)
   - Public routes (signin, signup)
   - Protected routes (tasks, task detail)
   - Route guard implementation
   - Navigation components

4. **UI Components** (Day 2)
   - Task list component
   - Task item component
   - Task form components
   - Loading and error state components
   - Responsive layout components

5. **Page Implementation** (Day 2-3)
   - Tasks list page
   - Task creation page
   - Task detail/edit page
   - Authentication pages
   - Error boundary implementation

6. **State Management & Integration** (Day 3)
   - Task data fetching and caching
   - Optimistic UI updates
   - State synchronization with backend
   - Form validation and submission

### Risk Mitigation
- **Auth Integration**: Thoroughly test session management and token handling
- **API Integration**: Implement robust error handling and retry mechanisms
- **Responsiveness**: Test across multiple device sizes and orientations
- **Security**: Validate all auth checks and data isolation measures
- **Performance**: Optimize data fetching and component rendering

### Success Criteria Verification
- All required pages implemented and accessible
- Better Auth integration working correctly
- Task CRUD operations functional with backend API
- Protected routes properly secured
- Responsive design working across devices
- Error handling implemented appropriately
- Performance meeting requirements (<3s initial load, <1s interaction)

## Dependencies

### External Services
- Backend Task Management API
- Better Auth service (for authentication)

### Libraries
- Next.js: Frontend framework with App Router
- React: UI component library
- Better Auth: Authentication system
- Tailwind CSS: Styling framework
- Axios/Fetch: HTTP client for API requests

### Environment Variables
- `NEXTAUTH_URL`: Application base URL
- `BETTER_AUTH_SECRET`: Secret for JWT signing
- `BACKEND_API_URL`: Backend API base URL for integration