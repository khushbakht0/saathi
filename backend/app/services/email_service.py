from typing import Any

from app.core.logger import logger


class EmailService:
    def classify_email(self, subject: str, body: str) -> dict[str, Any]:
        logger.info("classifying email", extra={"subject": subject})
        return {
            "classification": "timetable",
            "confidence": 0.95,
            "summary": f"Academic email: {subject}",
            "raw_response": {},
            "model": "gpt-4o-mini",
            "prompt_version": "v0.1",
        }
