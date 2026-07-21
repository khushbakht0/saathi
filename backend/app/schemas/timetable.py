from typing import Optional

from pydantic import BaseModel, Field


class TimetableEntryCreate(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: str = Field(..., pattern=r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    end_time: str = Field(..., pattern=r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    subject: str = Field(..., min_length=1)
    room: Optional[str] = None
    source_type: str = Field(default="excel")
    source_ref: Optional[str] = None


class TimetableEntryRead(TimetableEntryCreate):
    id: int
