# ADR 0001: Use Clean Architecture for the MVP Backend

## Status
Accepted

## Context

The core product will eventually include Gmail ingestion, AI classification, timetable parsing, dashboard views, notifications, and future university integrations. The system must remain maintainable and extensible without major rewrites.

## Decision

We will organize the backend using a clean architecture-style structure:

- API
- Services
- Repositories
- Models
- Schemas
- Parsers
- Config
- Core
- Utils

## Consequences

### Positive
- Business logic stays out of routes.
- Services can be replaced or extended without changing API contracts.
- Database and parser concerns remain isolated.
- Easier long-term maintainability.

### Negative
- More folders and abstractions than a minimal script-based app.
- Slightly more upfront structure.
