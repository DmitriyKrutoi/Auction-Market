from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest

from app.domain.exceptions import InvalidOperationError
from app.domain.value_objects.enums import BetStatus
from tests.fixtures.bets import make_bet


class TestBetInitialization:
    """Тесты инициализации Bet."""

    def test_creates_bet_with_pending_status(self):
        bet = make_bet()
        assert bet.status == BetStatus.PENDING

    def test_generates_unique_id(self):
        bet1 = make_bet()
        bet2 = make_bet()
        assert isinstance(bet1.id, UUID)
        assert bet1.id != bet2.id

    def test_sets_created_at(self):
        bet = make_bet()
        assert isinstance(bet.created_at, datetime)

    def test_stores_market_and_user_ids(self):
        market_id = UUID("12345678-1234-5678-1234-567812345678")
        user_id = UUID("87654321-4321-8765-4321-876543218765")

        bet = make_bet(market_id=market_id, user_id=user_id)

        assert bet.market_id == market_id
        assert bet.user_id == user_id

    def test_stores_amount_and_odds(self):
        bet = make_bet(amount=Decimal("200"), odds=Decimal("3.0"))
        assert bet.amount == Decimal("200")
        assert bet.odds == Decimal("3.0")

    def test_calculates_potential_payout(self):
        bet = make_bet(amount=Decimal("100"), odds=Decimal("2.5"))
        assert bet.potential_payout == Decimal("250")

    def test_calculates_potential_payout_with_fractional_odds(self):
        bet = make_bet(amount=Decimal("100"), odds=Decimal("1.5"))
        assert bet.potential_payout == Decimal("150")


class TestBetValidation:
    """Тесты валидации полей Bet."""

    def test_rejects_amount_below_minimum(self):
        with pytest.raises(InvalidOperationError, match="Минимальная ставка"):
            make_bet(amount=Decimal("50"))

    def test_rejects_zero_amount(self):
        with pytest.raises(InvalidOperationError, match="Минимальная ставка"):
            make_bet(amount=Decimal("0"))

    def test_rejects_negative_amount(self):
        with pytest.raises(InvalidOperationError, match="Минимальная ставка"):
            make_bet(amount=Decimal("-100"))

    def test_accepts_exact_minimum_amount(self):
        bet = make_bet(amount=Decimal("100"))
        assert bet.amount == Decimal("100")

    def test_accepts_amount_above_minimum(self):
        bet = make_bet(amount=Decimal("100.01"))
        assert bet.amount == Decimal("100.01")

    def test_rejects_odds_equal_to_one(self):
        with pytest.raises(InvalidOperationError, match="Коэффициент"):
            make_bet(odds=Decimal("1"))

    def test_rejects_odds_below_one(self):
        with pytest.raises(InvalidOperationError, match="Коэффициент"):
            make_bet(odds=Decimal("0.5"))

    def test_accepts_odds_above_one(self):
        bet = make_bet(odds=Decimal("1.01"))
        assert bet.odds == Decimal("1.01")


class TestBetResolve:
    """Тесты метода resolve."""

    def test_resolve_as_winner_sets_status_won(self, pending_bet):
        pending_bet.resolve(is_winner=True)
        assert pending_bet.status == BetStatus.WON

    def test_resolve_as_loser_sets_status_lost(self, pending_bet):
        pending_bet.resolve(is_winner=False)
        assert pending_bet.status == BetStatus.LOST

    def test_cannot_resolve_already_won_bet(self, winning_bet):
        with pytest.raises(InvalidOperationError, match="Ставка уже разрешена"):
            winning_bet.resolve(is_winner=True)

    def test_cannot_resolve_already_lost_bet(self, losing_bet):
        with pytest.raises(InvalidOperationError, match="Ставка уже разрешена"):
            losing_bet.resolve(is_winner=False)

    def test_cannot_resolve_returned_bet(self, returned_bet):
        with pytest.raises(InvalidOperationError, match="Ставка уже разрешена"):
            returned_bet.resolve(is_winner=True)


class TestBetReturn:
    """Тесты метода return_bet."""

    def test_return_pending_bet_sets_status_returned(self, pending_bet):
        pending_bet.return_bet()
        assert pending_bet.status == BetStatus.RETURNED

    def test_cannot_return_already_won_bet(self, winning_bet):
        with pytest.raises(InvalidOperationError, match="Нельзя вернуть"):
            winning_bet.return_bet()

    def test_cannot_return_already_lost_bet(self, losing_bet):
        with pytest.raises(InvalidOperationError, match="Нельзя вернуть"):
            losing_bet.return_bet()

    def test_cannot_return_already_returned_bet(self, returned_bet):
        with pytest.raises(InvalidOperationError, match="Нельзя вернуть"):
            returned_bet.return_bet()
