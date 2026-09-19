from decimal import Decimal

import pytest

from app.domain.entities.user import User

from .wallets import make_wallet


def make_user(**overrides) -> User:
    defaults = dict(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        wallet=make_wallet(),  # ← переиспользуем фабрику
        is_admin=False,
    )
    return User(**{**defaults, **overrides})


@pytest.fixture
def valid_user() -> User:
    return make_user()


@pytest.fixture
def admin_user() -> User:
    return make_user(username="admin", is_admin=True)


@pytest.fixture
def poor_user() -> User:
    return make_user(wallet=make_wallet(balance=Decimal("0")))
