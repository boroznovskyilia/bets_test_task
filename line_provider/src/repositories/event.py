from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from src.models import Event
from src.schemas.event import EventCreate, EventState


class EventRepository(BaseRepository):
    model = Event

    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = select(cls.model)
        return await session.scalars(query)

    @classmethod
    async def get_by_id(cls, id, session: AsyncSession) -> Event:
        query = select(cls.model).where(cls.model.id == id)
        return await session.scalar(query)

    @classmethod
    async def create(self, data: EventCreate, session: AsyncSession):
        new_event = Event(**data.model_dump())
        session.add(new_event)
        await session.flush()
        return new_event

    @classmethod
    async def update_status(cls, id: int, new_status: EventState, session: AsyncSession):
        stmt = update(Event).where(Event.id == id).values(status=new_status)
        await session.execute(stmt)
