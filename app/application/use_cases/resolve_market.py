from app.application.dto.resolve_market import (ResolveMarketCommand,
                                                ResolveMarketResponse)
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.services.wallet_updater import WalletUpdater


class ResolveMarket:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, command: ResolveMarketCommand) -> ResolveMarketResponse:
        async with self.uow:
            # 1. Проверка прав и состояния
            await self._validate(command)

            # 2. Получение агрегированных данных
            user_summaries = await self.uow.bets.get_winners_summary(command.market_id)

            # 3. Массовое обновление ставок
            updated_count = await self._bulk_update_bets(command)

            # 4. Обновление кошельков
            await self._update_wallets(user_summaries, command.winning_outcome)

            # 5. Закрытие рынка
            market = await self.uow.markets.get_by_id(command.market_id)
            market.close()
            await self.uow.markets.save(market)

            await self.uow.commit()

            # 6. Публикация события
            await self._publish_event(command, updated_count)

            return ResolveMarketResponse(
                resolved_bets=updated_count,
                winners=updated_count if command.winning_outcome else 0,
                losers=0 if command.winning_outcome else updated_count,
            )

    async def _update_wallets(self, user_summaries, winning_outcome: bool):
        """Обновляет кошельки пользователей."""
        for summary in user_summaries:
            user = await self.uow.users.get_by_id(summary.user_id)
            if not user:
                continue

            # Используем доменный сервис
            if winning_outcome:
                user = WalletUpdater.update_winners(user, summary)
            else:
                user = WalletUpdater.update_losers(user, summary)

            await self.uow.users.save(user)
