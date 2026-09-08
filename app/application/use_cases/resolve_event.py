from app.application.dto.events import EventResponse, ResolveEventCommand
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.exceptions import (ForbiddenError, InvalidOperationError,
                                   NotFoundError)
from app.domain.value_objects.enums import EventStatus


class ResolveEvent:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, command: ResolveEventCommand) -> EventResponse:
        async with self.uow:
            # Проверяем права
            admin = await self.uow.users.get_by_id(command.admin_id)
            if not admin or not admin.is_admin:
                raise ForbiddenError("Только администратор может разрешать события")

            # Получаем событие
            event = await self.uow.events.get_by_id(command.event_id)
            if not event:
                raise NotFoundError(f"Событие с id {command.event_id} не найдено")

            if event.status != EventStatus.OPEN:
                raise InvalidOperationError(f"Событие уже разрешено: {event.status}")

            # Разрешаем событие
            event.resolve(command.winning_outcome)

            # Сохраняем
            await self.uow.events.save(event)
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
