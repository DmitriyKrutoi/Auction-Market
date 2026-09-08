from typing import List
from uuid import UUID

from app.application.dto.markets import BetResponse
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.exceptions import NotFoundError


class ListMarketBets:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, market_id: UUID) -> List[BetResponse]:
        async with self.uow:
            market = await self.uow.markets.get_by_id(market_id)
            if not market:
                raise NotFoundError(f"Рынок с id {market_id} не найден")

            bets = await self.uow.bets.list_by_market(market_id)

            return [
                BetResponse(
                    id=bet.id,
                    market_id=bet.market_id,
                    user_id=bet.user_id,
                    amount=bet.amount,
                    odds=bet.odds,
                    status=bet.status.value,
                    potential_payout=bet.potential_payout,
                    created_at=bet.created_at,
                )
                for bet in bets
            ]
