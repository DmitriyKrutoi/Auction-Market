import pytest

from app.domain.entities.event import Event


def make_event(**overrides) -> Event:
    defaults = dict(
        title="Test Event",
        description="Test Description",
        category="sports",
        outcomes=["Team A", "Team B", "Draw"],
    )
    return Event(**{**defaults, **overrides})


@pytest.fixture
def open_event() -> Event:
    return make_event()


@pytest.fixture
def resolved_event() -> Event:
    event = make_event()
    event.resolve("Team A")
    return event


@pytest.fixture
def cancelled_event() -> Event:
    event = make_event()
    event.cancel()
    return event
