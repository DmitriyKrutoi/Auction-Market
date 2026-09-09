from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass
class BetPlaced:
    bet_id: UUID
    market_id: UUID
    user_id: UUID
    amount: Decimal
    timestamp: datetime = datetime.utcnow()
