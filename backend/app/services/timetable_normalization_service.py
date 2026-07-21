from typing import Any

from app.core.logger import logger


class TimetableNormalizationService:
    def normalize(self, record: dict[str, Any]) -> dict[str, Any]:
        logger.info("normalizing timetable record", extra={"course": record.get("course_name")})

        course_name = str(record.get("course_name", "")).strip()
        course_kind = "Course"
        if "lab" in course_name.lower():
            course_kind = "Lab"

        normalized = dict(record)
        normalized["course_name"] = self._clean_course_name(course_name)
        normalized["course_kind"] = course_kind
        normalized["section"] = str(record.get("section", "")).strip().upper()
        normalized["faculty"] = str(record.get("faculty", "")).strip()
        normalized["room"] = str(record.get("room", "")).strip().upper()
        normalized["building"] = str(record.get("building", "")).strip()
        normalized["batch"] = str(record.get("batch", "")).strip()
        return normalized

    @staticmethod
    def _clean_course_name(course_name: str) -> str:
        cleaned = " ".join(course_name.split())
        return cleaned.title()
