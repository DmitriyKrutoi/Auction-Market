from decimal import Decimal

import pytest

from app.domain.entities.bet import Bet

from .markets import MarketFactory
from .users import UserFactory


class BetFactory:
    @staticmethod
    def make_bet(**overrides) -> Bet:
        defaults = dict(
            market_id=MarketFactory.make_market().id,
            user_id=UserFactory.make_user().id,
            amount=Decimal("100"),
            odds=Decimal("2.5"),
        )
        return Bet(**{**defaults, **overrides})


class BetFixtures:
    @pytest.fixture
    def pending_bet() -> Bet:
        return BetFactory.make_bet()

    @pytest.fixture
    def winning_bet() -> Bet:
        bet = BetFactory.make_bet()
        bet.resolve(is_winner=True)
        return bet
