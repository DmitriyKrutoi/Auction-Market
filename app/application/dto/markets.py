from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class CreateMarketCommand:
    event_id: UUID
    outcome: str
    odds: Decimal


@dataclass(frozen=True)
class MarketResponse:
    id: UUID
    event_id: UUID
    outcome: str
    odds: Decimal
    status: str
    total_bets_amount: Decimal


@dataclass(frozen=True)
class PlaceBetCommand:
    market_id: UUID
    user_id: UUID
    amount: Decimal


@dataclass(frozen=True)
class BetResponse:
    id: UUID
    market_id: UUID
    user_id: UUID
    amount: Decimal
    odds: Decimal
    status: str
    potential_payout: Decimal
    created_at: datetime


@dataclass(frozen=True)
class ResolveMarketCommand:
    market_id: UUID
    winning_outcome: bool
    admin_id: UUID


@dataclass(frozen=True)
class ResolveMarketResponse:
    resolved_bets: int
    winners: int
    losers: int
