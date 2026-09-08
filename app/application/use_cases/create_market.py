from app.application.dto.markets import CreateMarketCommand, MarketResponse
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.entities.market import Market
from app.domain.exceptions import InvalidOperationError, NotFoundError
from app.domain.value_objects.enums import EventStatus


class CreateMarket:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, command: CreateMarketCommand) -> MarketResponse:
        async with self.uow:
            # Проверяем, что событие существует и открыто
            event = await self.uow.events.get_by_id(command.event_id)
            if not event:
                raise NotFoundError(f"Событие с id {command.event_id} не найдено")

            if event.status != EventStatus.OPEN:
                raise InvalidOperationError(f"Событие закрыто: {event.status}")

            # Проверяем, что исход существует в событии
            if command.outcome not in event.outcomes:
                raise InvalidOperationError(
                    f"Исход '{command.outcome}' не найден в событии"
                )

            # Создаём рынок
            market = Market(
                event_id=command.event_id, outcome=command.outcome, odds=command.odds
            )

            # Сохраняем
            await self.uow.markets.add(market)
            await self.uow.commit()

            return MarketResponse(
                id=market.id,
                event_id=market.event_id,
                outcome=market.outcome,
                odds=market.odds,
                status=market.status.value,
                total_bets_amount=market.total_bets_amount,
            )
