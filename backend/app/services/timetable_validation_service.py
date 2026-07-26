from dataclasses import dataclass
from typing import Any

from app.core.logger import logger


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[dict[str, Any]]


class TimetableValidationService:
    def validate(self, records: list[dict[str, Any]]) -> ValidationResult:
        errors: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str, str]] = set()

        for index, record in enumerate(records, start=1):
            if not record.get("day"):
                errors.append({"field": "day", "row": index, "message": "Day is required"})
            if not self._is_valid_time(record.get("time")):
                errors.append({"field": "time", "row": index, "message": "Invalid time format"})
            if not record.get("course_name"):
                errors.append({"field": "course_name", "row": index, "message": "Course name is required"})
            if not record.get("room"):
                errors.append({"field": "room", "row": index, "message": "Room name is required"})

            duplicate_key = (
                str(record.get("day", "")),
                str(record.get("time", "")),
                str(record.get("course_name", "")),
                str(record.get("room", "")),
            )
            if duplicate_key in seen:
                errors.append({"field": "duplicate_rows", "row": index, "message": "Duplicate record detected"})
            seen.add(duplicate_key)

        logger.info("validated timetable records", extra={"record_count": len(records), "error_count": len(errors)})
        return ValidationResult(is_valid=not errors, errors=errors)

    @staticmethod
    def _is_valid_time(value: str | None) -> bool:
        if not value:
            return False
        try:
            start, end = value.split("-")
            for part in (start, end):
                hour, minute = part.split(":")
                if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
                    return False
            return True
        except Exception:
            return False
