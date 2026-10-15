from app.application.dto.auth_principal import AuthPrincipal
from app.application.dto.events import CreateEventCommand, EventResponse
from app.application.policies.auth import require_admin
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.entities.event import Event


class CreateEvent:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, command: CreateEventCommand, actor: AuthPrincipal) -> EventResponse:
        async with self.uow:
            # Проверяем права администратора
            require_admin(actor)

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
