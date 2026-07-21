from typing import Any

from app.core.logger import logger
from app.schemas.timetable import TimetableEntryCreate


class TimetableService:
    def normalize_entries(self, payload: dict[str, Any]) -> list[TimetableEntryCreate]:
        logger.info("normalizing timetable payload", extra={"rows": len(payload.get("rows", []))})
        entries = []
        for row in payload.get("rows", []):
            entries.append(
                TimetableEntryCreate(
                    day_of_week=int(row.get("day_of_week", 0)),
                    start_time=str(row.get("start_time", "09:00")),
                    end_time=str(row.get("end_time", "10:00")),
                    subject=str(row.get("subject", "Unknown")),
                    room=row.get("room"),
                    source_type=str(row.get("source_type", "excel")),
                    source_ref=row.get("source_ref"),
                )
            )
        return entries
