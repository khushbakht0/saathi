# Backend

## Purpose

This backend contains the API, service layer, repository layer, models, schemas, parsers, and configuration needed to power the AI Student Assistant MVP.

## Structure

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

## Notes

- Logging is centralized in `app/core/logger.py`.
- All API errors use structured `HTTPException` responses.
- Avoid business logic inside routes.
- Keep services injectable and reusable.
