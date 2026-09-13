from decimal import Decimal

import pytest

from app.domain.value_objects.wallet import Wallet


class WalletFactory:
    @staticmethod
    def make_wallet(**overrides) -> Wallet:
        defaults = dict(
            balance=Decimal("1000"),
            frozen=Decimal("0"),
        )
        return Wallet(**{**defaults, **overrides})


class WalletFixtures:
    @pytest.fixture
    def empty_wallet() -> Wallet:
        return WalletFactory.make_wallet(balance=Decimal("0"))

    @pytest.fixture
    def rich_wallet() -> Wallet:
        return Wallet.make_wallet(balance=Decimal("10000"))
