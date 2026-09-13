from decimal import Decimal

import pytest

from app.domain.entities.user import User
from tests.fixtures.wallets import make_wallet

from .wallets import WalletFactory


class UserFactory:
    @staticmethod
    def make_user(**overrides) -> User:
        defaults = dict(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password",
            wallet=WalletFactory.make_wallet(),  # ← переиспользуем фабрику
            is_admin=False,
        )
        return User(**{**defaults, **overrides})


class UserFixtures:
    @pytest.fixture
    def valid_user() -> User:
        return WalletFactory.make_user()

    @pytest.fixture
    def admin_user() -> User:
        return UserFactory.make_user(username="admin", is_admin=True)

    @pytest.fixture
    def poor_user() -> User:
        return UserFactory.make_user(wallet=make_wallet(balance=Decimal("0")))
