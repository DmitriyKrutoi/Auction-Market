import pytest

from app.domain.entities.event import Event


class EventFactory:
    @staticmethod
    def make_event(**overrides) -> Event:
        defaults = dict(
            title="Test Event",
            description="Test Description",
            category="sports",
            outcomes=["Team A", "Team B", "Draw"],
        )
        return Event(**{**defaults, **overrides})


class EventFixtures:
    @pytest.fixture
    def open_event() -> Event:
        return EventFactory.make_event()

    @pytest.fixture
    def resolved_event() -> Event:
        event = EventFactory.make_event()
        event.resolve("Team A")
        return event
