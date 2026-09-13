from decimal import Decimal

from app.domain.entities.market import Market


class MarketFactory:
    @staticmethod
    def make_market(**overrides) -> Market:
        defaults = dict(event_id=67, outcome="Team A", odds=Decimal("2.5"))
        return Market(**{**defaults, **overrides})
