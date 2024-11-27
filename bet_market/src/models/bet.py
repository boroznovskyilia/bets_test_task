from uuid import UUID

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric

from enum import Enum


class BetState(Enum):
    NEW = 1
    FISTW_IN = 2
    SECOND_WIN = 3


class Bet(Base):
    __tablename__ = "bet"

    event_id: Mapped[UUID]
    status: Mapped[BetState]
    summary: Mapped[Numeric] = mapped_column(Numeric(scale=2))

    def __repr__(self):
        return f"<Bet(id={self.id}, event_id={self.event_id}, status={self.status}, summary={self.summary})>"
