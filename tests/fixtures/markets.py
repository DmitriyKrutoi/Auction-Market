from decimal import Decimal

import pytest

from app.domain.entities.market import Market

from .events import make_event


def make_market(**overrides) -> Market:
    defaults = dict(event_id=make_event().id, outcome="Team A", odds=Decimal("2.5"))
    return Market(**{**defaults, **overrides})


@pytest.fixture
def closed_market():
    market = make_market()
    market.close()
    return market
