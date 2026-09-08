from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass(frozen=True)
class CreateEventCommand:
    title: str
    description: str
    category: str
    outcomes: List[str]
    admin_id: UUID


@dataclass(frozen=True)
class EventResponse:
    id: UUID
    title: str
    description: str
    category: str
    status: str
    outcomes: List[str]
    resolved_outcome: str | None
    created_at: datetime
    resolved_at: datetime | None


@dataclass(frozen=True)
class ResolveEventCommand:
    event_id: UUID
    winning_outcome: str
    admin_id: UUID
