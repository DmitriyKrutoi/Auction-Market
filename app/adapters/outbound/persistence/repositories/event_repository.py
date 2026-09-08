from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.outbound.persistence.models import EventModel
from app.application.ports.repositories import EventRepository
from app.domain.entities.event import Event
from app.domain.value_objects.enums import EventStatus


class PostgresEventRepository(EventRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, event_id: UUID) -> Event | None:
        result = await self.session.get(EventModel, event_id)
        return self._to_domain(result) if result else None

    async def add(self, event: Event) -> None:
        model = EventModel(
            id=event.id,
            title=event.title,
            description=event.description,
            category=event.category,
            status=(
                event.status.value
                if hasattr(event.status, "value")
                else str(event.status)
            ),
            outcomes=event.outcomes,
            resolved_outcome=event.resolved_outcome,
            created_at=event.created_at,
            resolved_at=event.resolved_at,
        )
        self.session.add(model)
        await self.session.flush()

    async def save(self, event: Event) -> None:
        """Обновляет существующее событие."""
        model = await self.session.get(EventModel, event.id)
        if not model:
            raise ValueError(f"Event with id {event.id} not found")

        model.title = event.title
        model.description = event.description
        model.category = event.category
        model.status = (
            event.status.value if hasattr(event.status, "value") else str(event.status)
        )
        model.outcomes = event.outcomes
        model.resolved_outcome = event.resolved_outcome
        model.resolved_at = event.resolved_at
        await self.session.flush()

    async def list_open(self) -> list[Event]:
        stmt = select(EventModel).where(EventModel.status == "open")
        result = await self.session.scalars(stmt)
        return [self._to_domain(model) for model in result]

    async def list_all(self) -> list[Event]:
        stmt = select(EventModel).order_by(EventModel.created_at.desc())
        result = await self.session.scalars(stmt)
        return [self._to_domain(model) for model in result]

    def _to_domain(self, model: EventModel) -> Event:
        return Event(
            id=model.id,
            title=model.title,
            description=model.description,
            category=model.category,
            status=EventStatus(model.status),
            outcomes=list(model.outcomes) if model.outcomes else [],
            resolved_outcome=model.resolved_outcome,
            created_at=model.created_at,
            resolved_at=model.resolved_at,
        )
