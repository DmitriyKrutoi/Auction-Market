from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class CreateEventRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = ""
    category: str = ""
    outcomes: List[str] = Field(..., min_items=2)


class EventResponse(BaseModel):
    id: UUID
    title: str
    description: str
    category: str
    status: str
    outcomes: List[str]
    resolved_outcome: str | None
    created_at: datetime
    resolved_at: datetime | None


class ResolveEventRequest(BaseModel):
    winning_outcome: str
