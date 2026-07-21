from typing import Any

from app.services.parsers.base import BaseParser


class IngestionPipeline:
    def __init__(self, parser: BaseParser):
        self.parser = parser

    def process(self, payload: Any) -> list[dict[str, Any]]:
        raw_entries = self.parser.parse(payload)
        normalized = [self.validate_entry(entry) for entry in raw_entries]
        return normalized

    @staticmethod
    def validate_entry(entry: dict[str, Any]) -> dict[str, Any]:
        required = {"day_of_week", "start_time", "end_time", "subject"}
        missing = required.difference(entry.keys())
        if missing:
            raise ValueError(f"Missing required timetable fields: {sorted(missing)}")
        return entry
