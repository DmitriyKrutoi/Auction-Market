# app/adapters/outbound/persistence/models.py
from sqlalchemy import String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from decimal import Decimal


class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    frozen: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)