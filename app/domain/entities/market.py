from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.exceptions import InvalidOperationError, MarketClosedError
from app.domain.value_objects.enums import MarketStatus


@dataclass
class Market:
    event_id: UUID
    outcome: str
    odds: Decimal  # коэффициент, например 2.5
    id: UUID = field(default_factory=uuid4)
    status: MarketStatus = MarketStatus.OPEN
    total_bets_amount: Decimal = Decimal("0")
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if self.event_id is None:
            raise InvalidOperationError("event_id обязателен")
        if not self.outcome or not self.outcome.strip():
            raise InvalidOperationError("Исход не может быть пустым")
        if self.odds <= Decimal("1"):
            raise InvalidOperationError("Коэффициент должен быть больше 1")
        if self.total_bets_amount < Decimal("0"):
            raise InvalidOperationError("Сумма ставок не может быть отрицательной")

    def close(self):
        """Закрывает рынок (после разрешения события)."""
        if self.status != MarketStatus.OPEN:
            raise MarketClosedError(f"Рынок уже закрыт: {self.status}")
        self.status = MarketStatus.CLOSED

    def update_total_bets(self, amount: Decimal):
        """Обновляет общую сумму ставок."""
        self.total_bets_amount += amount
