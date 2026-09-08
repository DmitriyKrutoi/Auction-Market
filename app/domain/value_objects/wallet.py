from dataclasses import dataclass
from decimal import Decimal

from app.domain.exceptions import InsufficientFundsError, InvalidOperationError


@dataclass(frozen=True)
class Wallet:
    balance: Decimal = Decimal("0")
    frozen: Decimal = Decimal("0")

    @property
    def available(self) -> Decimal:
        return self.balance - self.frozen

    def freeze(self, amount: Decimal) -> "Wallet":
        if amount > self.available:
            raise InsufficientFundsError(
                f"Недостаточно средств для заморозки {amount}. Доступно: {self.available}"
            )
        return Wallet(balance=self.balance, frozen=self.frozen + amount)

    def unfreeze(self, amount: Decimal) -> "Wallet":
        if amount > self.frozen:
            raise InvalidOperationError(
                f"Нельзя разморозить {amount}. Заморожено: {self.frozen}"
            )
        return Wallet(balance=self.balance, frozen=self.frozen - amount)

    def withdraw_frozen(self, amount: Decimal) -> "Wallet":
        if amount > self.frozen:
            raise InvalidOperationError(
                f"Недостаточно замороженных средств: {self.frozen}"
            )
        return Wallet(balance=self.balance - amount, frozen=self.frozen - amount)

    def deposit(self, amount: Decimal) -> "Wallet":
        return Wallet(balance=self.balance + amount, frozen=self.frozen)
