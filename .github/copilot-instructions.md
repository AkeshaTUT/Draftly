# Professional Teletype.in Analog

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a modern blog platform project built with FastAPI (Python) backend and Next.js (TypeScript) frontend.

## Project Structure
- `backend/` - FastAPI application with SQLAlchemy, PostgreSQL, Redis
- `frontend/` - Next.js 14 application with TypeScript, Tailwind CSS
- Uses modern patterns: async/await, dependency injection, type safety
- Security-first approach with JWT, rate limiting, input validation

## Key Technologies
- **Backend**: FastAPI, SQLAlchemy, Pydantic v2, PostgreSQL, Redis, Celery
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, Shadcn/UI
- **Auth**: JWT tokens, OAuth2, bcrypt password hashing
- **DevOps**: Docker, Docker Compose, GitHub Actions

## Development Guidelines
- Follow async/await patterns for database operations
- Use Pydantic models for request/response validation
- Implement proper error handling and logging
- Write comprehensive tests for both backend and frontend
- Use TypeScript strictly, avoid `any` types
- Follow REST API conventions and OpenAPI documentation
- Implement proper security measures (CORS, CSRF, XSS protection)

## Features to Implement
- User authentication and profiles
- Article creation with Markdown editor
- Real-time comments and reactions
- File uploads and image handling
- Email notifications and Telegram bot
- PWA functionality
- SEO optimization and social media previews
