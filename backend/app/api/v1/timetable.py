from fastapi import APIRouter, status

from app.core.exceptions import raise_http_error
from app.core.logger import logger
from app.services.timetable_service import TimetableService

router = APIRouter(prefix="/api", tags=["timetable"])


@router.post("/timetable")
def create_timetable(payload: dict):
    logger.info("POST /api/timetable called")
    service = TimetableService()
    try:
        entries = service.normalize_entries(payload)
        return {
            "message": "Timetable payload normalized successfully.",
            "entries": [entry.model_dump() for entry in entries],
        }
    except Exception as exc:
        logger.exception("timetable normalization failed")
        raise_http_error(status.HTTP_422_UNPROCESSABLE_ENTITY, "Timetable payload could not be normalized", {"error": str(exc)})
