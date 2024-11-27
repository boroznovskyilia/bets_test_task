from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from src.models import Bet
from src.dto.bet import BetDto


class BetRepository(BaseRepository):
    model = Bet

    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = select(cls.model)
        return await session.scalars(query)

    @classmethod
    async def get_by_id(cls, id, session: AsyncSession):
        query = select(cls.model).where(cls.model.id == id)
        return await session.scalar(query)

    @classmethod
    async def create(self, data: BetDto, session: AsyncSession):
        bet = Bet(**data.model_dump())
        session.add(bet)
        await session.flush()
        return bet.id
