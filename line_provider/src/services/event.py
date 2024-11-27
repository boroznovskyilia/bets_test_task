from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.event import EventRepository
from src.schemas.event import EventGet, EventCreate, EventState
from src.services.producers.events.update_event import UpdateEventMQProducer
from uuid import UUID
from fastapi import HTTPException


class EventService:
    def __init__(self, event_repository, producer):
        self._event_repository: EventRepository = event_repository
        self._producer: UpdateEventMQProducer = producer

    async def register_event(self, event: EventCreate, session: AsyncSession):
        new_event = await self._event_repository.create(event, session)
        await self._producer.publish(EventGet.model_validate(new_event, from_attributes=True).model_dump())
        return new_event

    async def get_all_events(self, session: AsyncSession):
        events = await self._event_repository.get_all(session)
        events_res = [EventGet.model_validate(event, from_attributes=True) for event in events]
        return events_res

    async def get_by_id(self, id, session: AsyncSession):
        event = await self._event_repository.get_by_id(id, session)
        return EventGet.model_validate(event, from_attributes=True) if event else None

    async def update_event_status(self, event_id: UUID, event_status: EventState, session: AsyncSession):
        event = await self._event_repository.get_by_id(event_id, session)
        if event:
            await self._event_repository.update_status(event_id, event_status, session)
            await self._producer.publish(EventGet.model_validate(event, from_attributes=True).model_dump())
            return EventGet.model_validate(event, from_attributes=True)
        else:
            # TODO: создать касотомную Ошибку EventNotFoundException и
            # сделать raise HTTPExeption from эта кастомная ошибка в router
            raise HTTPException(400, f"There is no event with {event_id} to update status")
