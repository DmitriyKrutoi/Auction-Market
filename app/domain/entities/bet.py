from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.exceptions import InvalidOperationError
from app.domain.value_objects.enums import BetStatus


@dataclass
class Bet:
    market_id: UUID
    user_id: UUID
    amount: Decimal
    odds: Decimal  # фиксируем коэффициент на момент ставки
    id: UUID = field(default_factory=uuid4)
    status: BetStatus = BetStatus.PENDING
    potential_payout: Decimal = Decimal("0")
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Вычисляем потенциальный выигрыш при создании."""
        self.potential_payout = self.amount * self.odds

    def resolve(self, is_winner: bool):
        if self.status != BetStatus.PENDING:
            raise InvalidOperationError(f"Ставка уже разрешена: {self.status}")
        self.status = BetStatus.WON if is_winner else BetStatus.LOST

    def return_bet(self):
        """Возвращает ставку (при отмене события)."""
        if self.status != BetStatus.PENDING:
            raise ValueError("Bet is already resolved")
        self.status = BetStatus.RETURNED
