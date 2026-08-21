from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Wallet:
    balance: Decimal = Decimal("0")
    frozen: Decimal = Decimal("0")

    @property
    def available(self) -> Decimal:
        return self.balance - self.frozen

    def freeze(self, amount: Decimal) -> "Wallet":
        if amount > self.available:
            raise ValueError("Недостаточно средств для заморозки")
        return Wallet(balance=self.balance, frozen=self.frozen + amount)

    def unfreeze(self, amount: Decimal) -> "Wallet":
        if amount > self.frozen:
            raise ValueError("Нельзя разморозить больше, чем заморожено")
        return Wallet(balance=self.balance, frozen=self.frozen - amount)

    def withdraw_frozen(self, amount: Decimal) -> "Wallet":
        """Списать замороженные средства (при выигрыше аукциона)."""
        if amount > self.frozen:
            raise ValueError("Недостаточно замороженных средств")
        return Wallet(balance=self.balance - amount, frozen=self.frozen - amount)

    def deposit(self, amount: Decimal) -> "Wallet":
        return Wallet(balance=self.balance + amount, frozen=self.frozen)