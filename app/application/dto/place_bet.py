from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class PlaceBetCommand:
    market_id: UUID
    user_id: UUID
    amount: Decimal


@dataclass(frozen=True)
class PlaceBetResponse:
    bet_id: UUID
    status: str
    potential_payout: Decimal
