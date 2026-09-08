import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import JSON, Boolean, Text


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    frozen: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    is_admin = mapped_column(Boolean, default=False)  # Добавляем
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class EventModel(Base):
    __tablename__ = "events"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = mapped_column(String(255))
    description = mapped_column(Text, default="")
    category = mapped_column(String(100), default="")
    status = mapped_column(String(50), default="open")
    outcomes = mapped_column(JSON, default=list)  # список строк
    resolved_outcome = mapped_column(String(255), nullable=True)
    created_at = mapped_column(DateTime, default=datetime.now)
    resolved_at = mapped_column(DateTime, nullable=True)


class MarketModel(Base):
    __tablename__ = "markets"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = mapped_column(UUID(as_uuid=True), ForeignKey("events.id"))
    outcome = mapped_column(String(255))
    odds = mapped_column(Numeric(5, 2))
    status = mapped_column(String(50), default="open")
    total_bets_amount = mapped_column(Numeric(12, 2), default=0)
    created_at = mapped_column(DateTime, default=datetime.now)


class BetModel(Base):
    __tablename__ = "bets"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    market_id = mapped_column(UUID(as_uuid=True), ForeignKey("markets.id"))
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    amount = mapped_column(Numeric(12, 2))
    odds = mapped_column(Numeric(5, 2))
    status = mapped_column(String(50), default="pending")
    potential_payout = mapped_column(Numeric(12, 2))
    created_at = mapped_column(DateTime, default=datetime.now)
