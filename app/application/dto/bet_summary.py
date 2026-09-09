from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class UserBetSummary:
    user_id: UUID
    total_amount: Decimal
    total_payout: Decimal
    bets_count: int
