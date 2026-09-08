from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.outbound.persistence.models import MarketModel
from app.application.ports.repositories import MarketRepository
from app.domain.entities.market import Market


class PostgresMarketRepository(MarketRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, market_id: UUID) -> Market | None:
        result = await self.session.get(MarketModel, market_id)
        return self._to_domain(result) if result else None

    async def add(self, market: Market) -> None:
        model = MarketModel(
            id=market.id,
            event_id=market.event_id,
            outcome=market.outcome,
            odds=market.odds,
            status=(
                market.status.value
                if hasattr(market.status, "value")
                else market.status
            ),
            total_bets_amount=market.total_bets_amount,
            created_at=market.created_at,
        )
        self.session.add(model)
        await self.session.flush()

    async def list_by_event(self, event_id: UUID) -> list[Market]:
        stmt = select(MarketModel).where(MarketModel.event_id == event_id)
        result = await self.session.scalars(stmt)
        return [self._to_domain(m) for m in result]

    def _to_domain(self, model: MarketModel) -> Market:
        from decimal import Decimal

        return Market(
            id=model.id,
            event_id=model.event_id,
            outcome=model.outcome,
            odds=Decimal(str(model.odds)),
            status=model.status,
            total_bets_amount=Decimal(str(model.total_bets_amount)),
            created_at=model.created_at,
        )
