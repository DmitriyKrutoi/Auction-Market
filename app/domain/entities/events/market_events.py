from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class MarketResolved:
    market_id: UUID
    winners: int
    losers: int
    timestamp: datetime = datetime.now()
