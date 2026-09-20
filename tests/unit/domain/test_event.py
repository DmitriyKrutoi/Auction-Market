from datetime import datetime
from uuid import UUID

import pytest

from app.domain.exceptions import EventNotOpenError, InvalidOperationError, ValidationError
from app.domain.value_objects.enums import EventStatus
from tests.fixtures.events import make_event


class TestEventInitialization:
    """Тесты инициализации Event."""

    def test_generates_unique_id(self):
        event1 = make_event()
        event2 = make_event()
        assert isinstance(event1.id, UUID)
        assert event1.id != event2.id

    def test_status_defaults_to_open(self):
        event = make_event()
        assert event.status == EventStatus.OPEN

    def test_resolved_outcome_defaults_to_none(self):
        event = make_event()
        assert event.resolved_outcome is None

    def test_resolved_at_defaults_to_none(self):
        event = make_event()
        assert event.resolved_at is None

    def test_created_at_is_datetime(self):
        event = make_event()
        assert isinstance(event.created_at, datetime)

    def test_stores_provided_fields(self):
        event = make_event(
            title="Custom Title",
            description="Custom Description",
            category="politics",
            outcomes=["Yes", "No"],
        )
        assert event.title == "Custom Title"
        assert event.description == "Custom Description"
        assert event.category == "politics"
        assert event.outcomes == ["Yes", "No"]

    def test_stores_multiple_outcomes(self):
        event = make_event(outcomes=["A", "B", "C", "D"])
        assert len(event.outcomes) == 4
        assert "C" in event.outcomes


class TestEventValidation:
    """Тесты валидации полей Event."""

    def test_rejects_empty_title(self):
        with pytest.raises(ValidationError, match="Название"):
            make_event(title="")

    def test_rejects_whitespace_title(self):
        with pytest.raises(ValidationError, match="Название"):
            make_event(title="   ")

    def test_rejects_empty_outcomes(self):
        with pytest.raises(ValidationError, match="минимум 2 исхода"):
            make_event(outcomes=[])

    def test_rejects_single_outcome(self):
        with pytest.raises(ValidationError, match="минимум 2 исхода"):
            make_event(outcomes=["Only One"])

    def test_rejects_duplicate_outcomes(self):
        with pytest.raises(ValidationError, match="дубликат"):
            make_event(outcomes=["Team A", "Team A"])

    def test_accepts_valid_outcomes(self):
        event = make_event(outcomes=["Team A", "Team B"])
        assert event.outcomes == ["Team A", "Team B"]


class TestEventResolve:
    """Тесты метода resolve."""

    def test_resolve_sets_status_resolved(self, open_event):
        open_event.resolve("Team A")
        assert open_event.status == EventStatus.RESOLVED

    def test_resolve_sets_resolved_outcome(self, open_event):
        open_event.resolve("Team A")
        assert open_event.resolved_outcome == "Team A"

    def test_resolve_sets_resolved_at(self, open_event):
        open_event.resolve("Team A")
        assert isinstance(open_event.resolved_at, datetime)

    def test_cannot_resolve_with_invalid_outcome(self, open_event):
        with pytest.raises(InvalidOperationError, match="Неверный исход"):
            open_event.resolve("Nonexistent Outcome")

    def test_cannot_resolve_already_resolved_event(self, resolved_event):
        with pytest.raises(EventNotOpenError, match="не открыто"):
            resolved_event.resolve("Team B")

    def test_cannot_resolve_cancelled_event(self, cancelled_event):
        with pytest.raises(EventNotOpenError, match="не открыто"):
            cancelled_event.resolve("Team A")


class TestEventCancel:
    """Тесты метода cancel."""

    def test_cancel_sets_status_cancelled(self, open_event):
        open_event.cancel()
        assert open_event.status == EventStatus.CANCELLED

    def test_cancel_does_not_set_resolved_outcome(self, open_event):
        open_event.cancel()
        assert open_event.resolved_outcome is None

    def test_cannot_cancel_resolved_event(self, resolved_event):
        with pytest.raises(EventNotOpenError, match="не открыто"):
            resolved_event.cancel()

    def test_cannot_cancel_already_cancelled_event(self, cancelled_event):
        with pytest.raises(EventNotOpenError, match="не открыто"):
            cancelled_event.cancel()
