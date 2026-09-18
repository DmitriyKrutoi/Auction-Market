from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest

from app.domain.exceptions import InvalidOperationError, MarketClosedError
from app.domain.value_objects.enums import MarketStatus
from tests.fixtures.markets import make_market


class TestMarketInitialization:
    def test_generates_unique_id(self):
        market1 = make_market()
        market2 = make_market()
        assert isinstance(market1.id, UUID)
        assert market1.id != market2.id

    def test_status_defaults_to_open(self):
        market = make_market()
        assert market.status == MarketStatus.OPEN

    def test_total_bets_defaults_to_zero(self):
        market = make_market()
        assert market.total_bets_amount == Decimal("0")

    def test_created_at_is_datetime(self):
        market = make_market()
        assert isinstance(market.created_at, datetime)

    def test_stores_provided_fields(self):
        event_id = UUID("12345678-1234-5678-1234-567812345678")
        market = make_market(
            event_id=event_id,
            outcome="Team A",
            odds=Decimal("3.5"),
        )
        assert market.event_id == event_id
        assert market.outcome == "Team A"
        assert market.odds == Decimal("3.5")


class TestMarketClose:
    def test_close_changes_status_to_closed(self):
        market = make_market()  # OPEN
        market.close()
        assert market.status == MarketStatus.CLOSED

    def test_cannot_close_already_closed_market(self, closed_market):
        with pytest.raises(MarketClosedError, match="Рынок уже закрыт"):
            closed_market.close()


class TestMarketValidation:
    def test_rejects_odds_below_or_equal_one(self):
        with pytest.raises(InvalidOperationError, match="Коэффициент"):
            make_market(odds=Decimal("1"))

    def test_rejects_empty_outcome(self):
        with pytest.raises(InvalidOperationError, match="Исход"):
            make_market(outcome="")

    def test_rejects_whitespace_outcome(self):
        with pytest.raises(InvalidOperationError, match="Исход"):
            make_market(outcome="   ")


class TestMarketUpdateTotalBets:
    def test_rejects_zero_amount(self):
        market = make_market()
        with pytest.raises(InvalidOperationError, match="положительной"):
            market.update_total_bets(Decimal("0"))

    def test_rejects_negative_amount(self):
        market = make_market()
        with pytest.raises(InvalidOperationError, match="положительной"):
            market.update_total_bets(Decimal("-100"))

    def test_cannot_update_closed_market(self, closed_market):
        with pytest.raises(MarketClosedError, match="закрытый"):
            closed_market.update_total_bets(Decimal("100"))
