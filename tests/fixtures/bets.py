from decimal import Decimal

import pytest

from app.domain.entities.bet import Bet

from .markets import make_market
from .users import make_user


def make_bet(**overrides) -> Bet:
    defaults = dict(
        market_id=make_market().id,
        user_id=make_user().id,
        amount=Decimal("100"),
        odds=Decimal("2.5"),
    )
    return Bet(**{**defaults, **overrides})


@pytest.fixture
def pending_bet() -> Bet:
    return make_bet()


@pytest.fixture
def winning_bet() -> Bet:
    bet = make_bet()
    bet.resolve(is_winner=True)
    return bet


@pytest.fixture
def losing_bet() -> Bet:
    bet = make_bet()
    bet.resolve(is_winner=False)
    return bet


@pytest.fixture
def returned_bet() -> Bet:
    bet = make_bet()
    bet.return_bet()
    return bet
