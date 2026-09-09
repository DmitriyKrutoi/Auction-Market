# app/application/use_cases/place_bet.py
from app.application.dto.place_bet import PlaceBetCommand, PlaceBetResponse
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.entities.bet import Bet
from app.domain.exceptions import (InsufficientFundsError, MarketClosedError,
                                   NotFoundError)
from app.domain.value_objects.enums import MarketStatus


class PlaceBet:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, command: PlaceBetCommand) -> PlaceBetResponse:
        async with self.uow:
            market = await self.uow.markets.get_by_id(command.market_id)
            if not market:
                raise NotFoundError(f"Рынок с id {command.market_id} не найден")
            if market.status != MarketStatus.OPEN:
                raise MarketClosedError(f"Рынок закрыт: {market.status}")

            user = await self.uow.users.get_by_id(command.user_id)
            if not user:
                raise NotFoundError(f"Пользователь с id {command.user_id} не найден")

            if user.wallet.available < command.amount:
                raise InsufficientFundsError(
                    f"""Недостаточно средств.
                    Доступно: {user.wallet.available},
                    требуется: {command.amount}"""
                )

            # Создаём ставку
            bet = Bet(
                market_id=command.market_id,
                user_id=command.user_id,
                amount=command.amount,
                odds=market.odds,
            )

            # Замораживаем деньги
            user.wallet = user.wallet.freeze(command.amount)

            # Сохраняем
            await self.uow.bets.add(bet)
            await self.uow.users.add(user)  # обновляем кошелёк
            market.update_total_bets(command.amount)
            await self.uow.markets.save(market)

            await self.uow.commit()

            return PlaceBetResponse(
                bet_id=bet.id,
                status=bet.status.value,
                potential_payout=bet.potential_payout,
            )
