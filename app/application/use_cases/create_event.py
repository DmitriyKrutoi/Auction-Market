from app.application.dto.events import CreateEventCommand, EventResponse
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.entities.event import Event
from app.domain.exceptions import ForbiddenError


class CreateEvent:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, command: CreateEventCommand) -> EventResponse:
        async with self.uow:
            # Проверяем права администратора
            admin = await self.uow.users.get_by_id(command.admin_id)
            if not admin or not admin.is_admin:
                raise ForbiddenError("Только администратор может создавать события")

            # Создаём событие
            event = Event(
                title=command.title,
                description=command.description,
                category=command.category,
                outcomes=command.outcomes,
            )

            # Сохраняем
            await self.uow.events.add(event)
            await self.uow.commit()

            return EventResponse(
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
