from typing import Any

from app.core.logger import logger


class GmailService:
    def sync_messages(self) -> dict[str, Any]:
        logger.info("syncing Gmail messages")
        return {"count": 0, "messages": []}
