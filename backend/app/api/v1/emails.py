from fastapi import APIRouter, HTTPException, status

from app.core.exceptions import raise_http_error
from app.core.logger import logger
from app.services.email_service import EmailService

router = APIRouter(prefix="/api", tags=["emails"])


@router.get("/emails")
def get_emails():
    logger.info("GET /api/emails called")
    service = EmailService()
    try:
        return {
            "items": [],
            "classification": service.classify_email("CS101 Lecture", "Please review the timetable"),
        }
    except Exception as exc:
        logger.exception("email listing failed")
        raise_http_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to list emails", {"error": str(exc)})
