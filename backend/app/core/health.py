from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.database import check_database_connection
from app.core.logger import logger


async def get_health_payload() -> dict[str, str]:
    if not check_database_connection():
        logger.exception("Database connectivity check failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed.",
        )

    return {
        "status": "ok",
        "version": settings.backend_version,
        "database": "connected",
        "environment": settings.environment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
