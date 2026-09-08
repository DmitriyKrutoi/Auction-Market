# app/domain/services/wallet_updater.py
from app.application.dto.bet_summary import UserBetSummary
from app.domain.entities.user import User


class WalletUpdater:
    @staticmethod
    def update_winners(user: User, summary: UserBetSummary) -> User:
        """Обновляет кошелёк победителя."""
        wallet = user.wallet
        wallet = wallet.unfreeze(summary.total_amount)
        profit = summary.total_payout - summary.total_amount
        wallet = wallet.deposit(profit)

        # Создаём нового пользователя с обновлённым кошельком
        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            wallet=wallet,
            is_admin=user.is_admin,
            created_at=user.created_at,
        )

    @staticmethod
    def update_losers(user: User, summary: UserBetSummary) -> User:
        """Обновляет кошелёк проигравшего."""
        wallet = user.wallet
        wallet = wallet.withdraw_frozen(summary.total_amount)

        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            wallet=wallet,
            is_admin=user.is_admin,
            created_at=user.created_at,
        )
