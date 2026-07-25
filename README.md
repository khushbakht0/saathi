# AI Student Assistant

Version: v0.1

## Overview

AI Student Assistant is a production-oriented SaaS-style platform for university students that ingests academic emails and timetable sources, classifies content with AI, and stores normalized academic data for future dashboard features.

## MVP scope

- Authentication
- Gmail integration
- Timetable ingestion
- Dashboard
- PostgreSQL
- AI email classification

## Architecture

This repository follows a clean architecture-style separation:

- backend/
  - api/
  - services/
  - repositories/
  - models/
  - schemas/
  - parsers/
  - config/
  - core/
  - utils/
  - tests/
  - docs/
- frontend/
  - components/
  - app/
  - hooks/
  - lib/
  - types/
  - styles/

## Naming conventions

- Components: PascalCase, e.g. `EmailCard.tsx`
- Services: camelCase, e.g. `emailService.py`
- Files: snake_case, e.g. `email_parser.py`
- API routes: REST style, e.g. `/api/emails`, `/api/timetable`

## Deployment architecture

- Frontend: Vercel
- Backend: Railway
- Database: Railway PostgreSQL

  ## why we made it?

  -so students can be facilitated with optimized use of gmail,gcr and university study groups.
  
