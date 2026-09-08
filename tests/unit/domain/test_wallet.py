from decimal import Decimal

import pytest

from app.domain.value_objects.wallet import Wallet


class TestWallet:
    def test_initial_wallet(self):
        wallet = Wallet()
        assert wallet.balance == Decimal("0")
        assert wallet.frozen == Decimal("0")
        assert wallet.available == Decimal("0")

    def test_deposit(self):
        wallet = Wallet()
        wallet = wallet.deposit(Decimal("100"))
        assert wallet.balance == Decimal("100")
        assert wallet.available == Decimal("100")

    def test_freeze_success(self):
        wallet = Wallet(balance=Decimal("100"))
        wallet = wallet.freeze(Decimal("30"))
        assert wallet.balance == Decimal("100")
        assert wallet.frozen == Decimal("30")
        assert wallet.available == Decimal("70")

    def test_freeze_insufficient(self):
        wallet = Wallet(balance=Decimal("50"))
        with pytest.raises(ValueError, match="Недостаточно средств"):
            wallet.freeze(Decimal("100"))

    def test_unfreeze_success(self):
        wallet = Wallet(balance=Decimal("100"), frozen=Decimal("40"))
        wallet = wallet.unfreeze(Decimal("25"))
        assert wallet.frozen == Decimal("15")
        assert wallet.available == Decimal("85")

    def test_unfreeze_too_much(self):
        wallet = Wallet(balance=Decimal("100"), frozen=Decimal("10"))
        with pytest.raises(ValueError, match="Нельзя разморозить больше"):
            wallet.unfreeze(Decimal("20"))
