from json import JSONDecodeError
from src.schemas.event import EventSchema
from src.services.cache.event_cache import EventCacheService
from httpx import AsyncClient, NetworkError
import logging
from src.config import settings
from uuid import UUID
from typing import Optional

logger = logging.getLogger(__name__)


class EventService:
    def __init__(self, cache_service):
        self._cache: EventCacheService = cache_service

    async def get_all_events(self) -> list[EventSchema]:
        cached_events = await self._cache.get_all_events()
        if cached_events:
            return cached_events
        try:
            async with AsyncClient() as client:
                response = await client.get(settings.line_provider.url_events)
                events_json = response.json()
                events = [EventSchema(**event) for event in events_json]
        except JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            raise e
        except NetworkError as e:
            logger.error(f"Failed to fetch events: {e}")
            raise e

        await self._cache.set_all(events)
        return events

    async def get_event_by_id(self, event_id: UUID) -> Optional[EventSchema]:
        try:
            async with AsyncClient() as client:
                response = await client.get(f"{settings.line_provider.url_events}/{event_id}")
                event_json = response.json()
                if event_json:
                    event = EventSchema(**event_json)
                else:
                    return None
        except JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            raise e
        except NetworkError as e:
            logger.error(f"Failed to fetch events: {e}")
            raise e
        return event

    async def update_events(self, event: EventSchema):
        cached_events = await self._cache.get_all_events()
        if cached_events:
            await self._cache.update_event(event)
