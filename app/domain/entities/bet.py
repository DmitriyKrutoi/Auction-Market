from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.exceptions import InvalidOperationError, ValidationError
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
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self._validate()
        self.potential_payout = self.amount * self.odds

    def _validate(self):
        if self.amount < Decimal("100"):
            raise ValidationError("Минимальная ставка — 100")
        if self.odds <= 1:
            raise ValidationError("Коэффициент должен быть > 1")

    def resolve(self, is_winner: bool):
        if self.status != BetStatus.PENDING:
            raise InvalidOperationError(f"Ставка уже разрешена: {self.status}")
        self.status = BetStatus.WON if is_winner else BetStatus.LOST

    def return_bet(self):
        """Возвращает ставку (при отмене события)."""
        if self.status != BetStatus.PENDING:
            raise InvalidOperationError(f"Нельзя вернуть ставку: {self.status}")
        self.status = BetStatus.RETURNED
