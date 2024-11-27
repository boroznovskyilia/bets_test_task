from src.services.cache.cache import CacheService
import json
from typing import Optional
from src.schemas.event import EventSchema


class EventCacheService(CacheService):
    def __init__(self, url: str):
        super().__init__(url)
        self.EVENT_HASH_KEY = "events"
        self.EVENT_FIELD_NAME = "event:{event_id}"

    async def get(self, key: str) -> Optional[str]:
        if self._redis:
            serialized_value = await self._redis.get(key)
            if serialized_value:
                events = json.loads(serialized_value)
                return [EventSchema(**json.loads(event)) for event in events]
        return []

    async def set_all(self, events: list[EventSchema]):
        if self._redis:
            pipe = self._redis.pipeline()
            for event in events:
                event_data = json.dumps(event.model_dump())
                field_name = self.EVENT_FIELD_NAME.format(event_id=event.id)
                pipe.hset(self.EVENT_HASH_KEY, field_name, event_data)
            await pipe.execute()
            await self._redis.expire(self.EVENT_HASH_KEY, 10)

    async def update_event(self, event: EventSchema):
        event_data = json.dumps(event.model_dump())
        await self._redis.hset(self.EVENT_HASH_KEY, self.EVENT_FIELD_NAME.format(event_id=event.id), event_data)
        # in case when cache from set_all expires and this hset imediatly add one event to cache
        await self._redis.expire(self.EVENT_HASH_KEY, 0.0001, nx=True)

    async def get_event_by_id(self, event_id: str):
        raw_event = await self._redis.hget(self.EVENT_HASH_KEY, self.EVENT_FIELD_NAME.format(event_id))
        return EventSchema(**json.loads(raw_event)) if raw_event else None

    async def get_all_events(self):
        raw_events = await self._redis.hgetall(self.EVENT_HASH_KEY)
        return [EventSchema(**json.loads(value)) for value in raw_events.values()]
