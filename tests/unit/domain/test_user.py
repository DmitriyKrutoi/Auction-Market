import uuid
from decimal import Decimal

from app.domain.entities.user import User
from app.domain.value_objects.wallet import Wallet


class TestUser:
    def test_initial_user(self):
        user = User(
            username="testuser", email="test@example.com", hashed_password="hashed"
        )
        assert user.username == "testuser"
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed"
        assert isinstance(user.id, uuid.UUID)
        assert user.wallet.balance == Decimal("0")
        assert user.wallet.frozen == Decimal("0")

    def test_wallet_properties(self):
        user = User(wallet=Wallet(balance=Decimal("500"), frozen=Decimal("100")))
        assert user.wallet.available == Decimal("400")
