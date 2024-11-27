from fastapi import APIRouter, Depends, HTTPException
from src.db.session import get_db_session

from src.db.cache_session import CacheDependency
from src.schemas.bet import BetCreate, BetState
from src.schemas.event import EventSchema
from src.repositories.bet import BetRepository
from src.dto.bet import BetDto
from src.services import BetService, EventService
from src.config import settings
from src.services.cache import BetCacheService, EventCacheService
from typing import Optional
from datetime import datetime

router = APIRouter()
bet_cache_dep = CacheDependency(BetCacheService(settings.redis.url))
event_cache_dep = CacheDependency(EventCacheService(settings.redis.url))


@router.get("/events", response_model=list[EventSchema])
async def get_events(cache=Depends(event_cache_dep)):
    return await EventService(cache).get_all_events()


@router.post("/bet")
async def register_bet(
    bet: BetCreate, event_cache=Depends(event_cache_dep), cache=Depends(bet_cache_dep), session=Depends(get_db_session)
):
    bet_datetime = datetime.now()
    bet_obj = BetDto(summary=bet.summary, event_id=bet.event_id)
    event: Optional[EventSchema] = await EventService(event_cache).get_event_by_id(bet.event_id)
    if not event or event.status != BetState.NEW or event.end_datetime < bet_datetime:
        raise HTTPException(400, f"There is no new event with {bet.event_id}")
    return await BetService(BetRepository(), cache).register_bet(bet_obj, session)


@router.get("/bets")
async def get_bets(session=Depends(get_db_session), cache=Depends(bet_cache_dep)):
    return await BetService(BetRepository(), cache).get_all_bets(session)
