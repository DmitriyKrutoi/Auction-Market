from typing import List
from uuid import UUID

from app.application.dto.markets import MarketResponse
from app.application.ports.unit_of_work import UnitOfWork


class ListMarkets:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, event_id: UUID | None = None) -> List[MarketResponse]:
        async with self.uow:
            if event_id:
                markets = await self.uow.markets.list_by_event(event_id)
            else:
                markets = await self.uow.markets.list_open()

            return [
                MarketResponse(
                    id=market.id,
                    event_id=market.event_id,
                    outcome=market.outcome,
                    odds=market.odds,
                    status=market.status.value,
                    total_bets_amount=market.total_bets_amount,
                )
                for market in markets
            ]
