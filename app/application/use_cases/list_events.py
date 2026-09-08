from typing import List

from app.application.dto.events import EventResponse
from app.application.ports.unit_of_work import UnitOfWork


class ListEvents:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self) -> List[EventResponse]:
        async with self.uow:
            events = await self.uow.events.list_all()

            return [
                EventResponse(
                    id=event.id,
                    title=event.title,
                    description=event.description,
                    category=event.category,
                    status=event.status.value,
                    outcomes=event.outcomes,
                    resolved_outcome=event.resolved_outcome,
                    created_at=event.created_at,
                    resolved_at=event.resolved_at,
                )
                for event in events
            ]
