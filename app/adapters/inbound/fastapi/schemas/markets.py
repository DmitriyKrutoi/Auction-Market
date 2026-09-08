from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class PlaceBetRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)


class BetResponse(BaseModel):
    bet_id: uuid4
    status: str
    potential_payout: Decimal


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


class ResolveEventRequest(BaseModel):
    winning_outcome: str
