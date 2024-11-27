from fastapi import APIRouter, Depends
from src.db.session import get_db_session


from src.schemas.event import EventGet, EventCreate, EventState
from src.services import EventService
from src.services.producers import UpdateEventMQProducer
from src.services.producers.session import UpdateMQDependency
from src.config import settings
from src.repositories.event import EventRepository
from uuid import UUID
from typing import Optional


router = APIRouter()

update_producer = UpdateEventMQProducer(
    rabbitmq_host=settings.rabbitmq.host,
    rabbitmq_port=settings.rabbitmq.port,
    rabbitmq_login=settings.rabbitmq.user,
    rabbitmq_password=settings.rabbitmq.password,
    exchange_name="events_state",
    routing_key="update",
)
update_producer_dep = UpdateMQDependency(update_producer)


@router.get("/events", response_model=list[EventGet])
async def get_events(producer=Depends(update_producer_dep), session=Depends(get_db_session)):
    return await EventService(EventRepository(), producer).get_all_events(session)


@router.post("/events", response_model=EventGet)
async def create_event(event: EventCreate, producer=Depends(update_producer_dep), session=Depends(get_db_session)):
    return await EventService(EventRepository(), producer).register_event(event, session)


@router.get("/events/{event_id}", response_model=Optional[EventGet])
async def get_event(event_id: UUID, producer=Depends(update_producer_dep), session=Depends(get_db_session)):
    return await EventService(EventRepository(), producer).get_by_id(event_id, session)


@router.patch("/events/{event_id}/{event_status}", response_model=EventGet)
async def update_event_status(
    event_id: UUID, event_status: EventState, producer=Depends(update_producer_dep), session=Depends(get_db_session)
):
    return await EventService(EventRepository(), producer).update_event_status(event_id, event_status, session)
