from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ResolveMarketCommand:
    market_id: UUID
    winning_outcome: bool  # True если этот исход выиграл


@dataclass(frozen=True)
class ResolveMarketResponse:
    resolved_bets: int
    winners: int
    losers: int
