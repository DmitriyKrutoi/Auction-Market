from decimal import Decimal

from app.domain.entities.market import Market

from .events import EventFactory


class MarketFactory:
    @staticmethod
    def make_market(**overrides) -> Market:
        defaults = dict(
            event_id=EventFactory.make_event().id, outcome="Team A", odds=Decimal("2.5")
        )
        return Market(**{**defaults, **overrides})
