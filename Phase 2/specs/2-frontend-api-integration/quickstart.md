# Quickstart Guide: Frontend Application & API Integration

**Feature**: 2-frontend-api-integration
**Date**: 2026-02-02

## Development Setup

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to backend API (Task Management API)
- Better Auth credentials

### Installation Steps

1. **Clone or create the Next.js project**
   ```bash
   npx create-next-app@latest frontend-app
   cd frontend-app
   ```

2. **Install required dependencies**
   ```bash
   npm install next react react-dom @better-auth/react better-auth axios
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

3. **Configure Tailwind CSS**
   Update `tailwind.config.js`:
   ```javascript
   /** @type {import('tailwindcss').Config} */
   module.exports = {
     content: [
       './pages/**/*.{js,ts,jsx,tsx,mdx}',
       './components/**/*.{js,ts,jsx,tsx,mdx}',
       './app/**/*.{js,ts,jsx,tsx,mdx}',
     ],
     theme: {
       extend: {},
     },
     plugins: [],
   }
   ```

4. **Set up environment variables**
   Create `.env.local` file:
   ```env
   NEXTAUTH_URL=http://localhost:3000
   BACKEND_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
   ```

5. **Initialize Tailwind CSS**
   Update `app/globals.css`:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

## Project Structure

```
frontend-app/
├── app/
│   ├── (auth)/
│   │   ├── signin/page.tsx
│   │   └── signup/page.tsx
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   ├── tasks/
│   │   │   ├── page.tsx
│   │   │   ├── new/page.tsx
│   │   │   └── [id]/page.tsx
│   │   └── layout.tsx
│   ├── layout.tsx
│   ├── page.tsx
│   └── providers.tsx
├── components/
│   ├── auth/
│   │   ├── SignInForm.tsx
│   │   └── SignUpForm.tsx
│   ├── tasks/
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   └── TaskCompletionToggle.tsx
│   ├── ui/
│   │   ├── Navbar.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── ErrorMessage.tsx
│   └── providers/
│       └── AuthProvider.tsx
├── lib/
│   ├── auth.ts
│   ├── api-client.ts
│   └── types.ts
└── public/
```

## Configuration

### Better Auth Setup
Create `lib/auth.ts`:
```typescript
import { betterAuth } from 'better-auth';
import { reactClient } from '@better-auth/react';

export const auth = betterAuth({
  app: {
    name: 'Todo App',
    baseUrl: process.env.NEXTAUTH_URL || 'http://localhost:3000',
  },
  socialProviders: {
    // Add social providers if needed
  },
});

export const authClient = reactClient({
  baseURL: process.env.NEXTAUTH_URL || 'http://localhost:3000',
  signInMethods: ['email'],
});
```

### API Client Setup
Create `lib/api-client.ts`:
```typescript
import axios from 'axios';

const BACKEND_API_URL = process.env.BACKEND_API_URL || 'http://localhost:3000';

const apiClient = axios.create({
  baseURL: BACKEND_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('better-auth-session-token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to sign-in on 401
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

## Running the Application

1. **Start the development server**
   ```bash
   npm run dev
   ```

2. **Open your browser**
   Navigate to `http://localhost:3000`

3. **Verify functionality**
   - Sign up for a new account
   - Sign in with your credentials
   - Create and manage tasks
   - Verify protected routes are inaccessible when not authenticated

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| NEXTAUTH_URL | Application base URL | http://localhost:3000 |
| BACKEND_API_URL | Backend API base URL | http://localhost:8000 |
| BETTER_AUTH_SECRET | Secret for JWT signing | your-super-secret-key |

## Common Commands

```bash
# Development
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Lint code
npm run lint

# Run tests
npm test
```

## Integration Testing

1. **Verify API integration**
   - Create a task and verify it appears in the list
   - Update a task and verify changes persist
   - Delete a task and verify it's removed

2. **Verify authentication**
   - Try accessing /tasks without signing in (should redirect)
   - Sign in and verify access to protected routes
   - Sign out and verify loss of access to protected routes

3. **Verify data isolation**
   - Log in as different users and verify separate task lists
   - Attempt to access other users' tasks (should fail)