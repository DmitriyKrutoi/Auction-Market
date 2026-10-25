from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID, uuid4

from pydantic import UUID4, BaseModel, Field


class CreateMarketRequest(BaseModel):
    event_id: UUID4
    outcome: str
    odds: Decimal = Field(..., gt=1)


class MarketResponse(BaseModel):
    id: UUID4
    event_id: UUID4
    outcome: str
    odds: Decimal
    status: str
    total_bets_amount: Decimal


class BetRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)


class ResolveMarketRequest(BaseModel):
    winning_outcome: bool


class ResolveMarketResponse(BaseModel):
    resolved_bets: int
    winners: int
    losers: int


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
