from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, DateTime

from enum import Enum


class EventState(int, Enum):
    NEW = 1
    FISTW_IN = 2
    SECOND_WIN = 3


class Event(Base):
    __tablename__ = "event"

    status: Mapped[EventState]
    koef: Mapped[Numeric] = mapped_column(Numeric(scale=2))
    end_datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=False))

    def __repr__(self):
        return f"<Bet(id={self.id}, koef={self.koef}, status={self.status}, end_datetime={self.end_datetime})>"
