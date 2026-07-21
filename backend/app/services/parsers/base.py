from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):
    @abstractmethod
    def parse(self, payload: Any) -> list[dict[str, Any]]:
        """Return normalized timetable entries from a given source payload."""
