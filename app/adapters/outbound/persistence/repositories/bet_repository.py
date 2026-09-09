from decimal import Decimal
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.outbound.persistence.models import BetModel
from app.application.dto.bet_summary import UserBetSummary
from app.application.ports.repositories import BetRepository
from app.domain.entities.bet import Bet
from app.domain.value_objects.enums import BetStatus


class PostgresBetRepository(BetRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, bet_id: UUID) -> Bet | None:
        result = await self.session.get(BetModel, bet_id)
        return self._to_domain(result) if result else None

    async def add(self, bet: Bet) -> None:
        model = BetModel(
            id=bet.id,
            market_id=bet.market_id,
            user_id=bet.user_id,
            amount=bet.amount,
            odds=bet.odds,
            status=(
                bet.status.value if hasattr(bet.status, "value") else str(bet.status)
            ),
            potential_payout=bet.potential_payout,
            created_at=bet.created_at,
        )
        self.session.add(model)
        await self.session.flush()

    async def save(self, bet: Bet) -> None:
        """Обновляет существующую ставку."""
        model = await self.session.get(BetModel, bet.id)
        if not model:
            raise ValueError(f"Bet with id {bet.id} not found")

        model.market_id = bet.market_id
        model.user_id = bet.user_id
        model.amount = bet.amount
        model.odds = bet.odds
        model.status = (
            bet.status.value if hasattr(bet.status, "value") else str(bet.status)
        )
        model.potential_payout = bet.potential_payout
        await self.session.flush()

    async def list_by_user(self, user_id: UUID) -> list[Bet]:
        stmt = select(BetModel).where(BetModel.user_id == user_id)
        result = await self.session.scalars(stmt)
        return [self._to_domain(model) for model in result]

    async def list_by_market(self, market_id: UUID) -> list[Bet]:
        stmt = select(BetModel).where(BetModel.market_id == market_id)
        result = await self.session.scalars(stmt)
        return [self._to_domain(model) for model in result]

    async def list_pending_by_market(self, market_id: UUID) -> list[Bet]:
        stmt = select(BetModel).where(
            BetModel.market_id == market_id, BetModel.status == "pending"
        )
        result = await self.session.scalars(stmt)
        return [self._to_domain(model) for model in result]

    def _to_domain(self, model: BetModel) -> Bet:
        return Bet(
            id=model.id,
            market_id=model.market_id,
            user_id=model.user_id,
            amount=Decimal(str(model.amount)),
            odds=Decimal(str(model.odds)),
            status=BetStatus(model.status),
            potential_payout=Decimal(str(model.potential_payout)),
            created_at=model.created_at,
        )

    async def get_winners_summary(self, market_id: UUID) -> list[UserBetSummary]:
        """Получает агрегированную информацию по ставкам."""
        stmt = (
            select(
                BetModel.user_id,
                func.sum(BetModel.amount).label("total_amount"),
                func.sum(BetModel.potential_payout).label("total_payout"),
                func.count(BetModel.id).label("bets_count"),
            )
            .where(and_(BetModel.market_id == market_id, BetModel.status == "pending"))
            .group_by(BetModel.user_id)
        )
        result = await self.session.execute(stmt)

        return [
            UserBetSummary(
                user_id=row.user_id,
                total_amount=Decimal(str(row.total_amount)),
                total_payout=Decimal(str(row.total_payout)),
                bets_count=row.bets_count,
            )
            for row in result
        ]
