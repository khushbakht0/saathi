from typing import Any

from app.services.parsers.base import BaseParser


class ExcelTimetableParser(BaseParser):
    """Generic parser placeholder for Excel-based timetable files."""

    def parse(self, payload: Any) -> list[dict[str, Any]]:
        if not isinstance(payload, dict):
            raise ValueError("Excel parser expects a dictionary-like workbook payload.")

        rows: list[dict[str, Any]] = []
        for row in payload.get("rows", []):
            rows.append(
                {
                    "day_of_week": int(row.get("day_of_week", 0)),
                    "start_time": row.get("start_time", "09:00"),
                    "end_time": row.get("end_time", "10:00"),
                    "subject": row.get("subject", "Unknown"),
                    "room": row.get("room"),
                    "source_type": "excel",
                    "source_ref": row.get("source_ref"),
                }
            )
        return rows
