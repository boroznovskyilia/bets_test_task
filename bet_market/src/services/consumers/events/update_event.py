from src.services.consumers.events import RabbitMQConsumer
from aio_pika.abc import AbstractIncomingMessage
from src.services.event import EventService
from src.services.cache.event_cache import EventCacheService
from src.config import settings
import json
from src.schemas.event import EventSchema
from src.db.cache_session import CacheDependency


event_cache_dep = CacheDependency(EventCacheService(settings.redis.url))


class UpdateEventMQConsumer(RabbitMQConsumer):
    def __init__(
        self,
        rabbitmq_host: str,
        rabbitmq_port: int,
        rabbitmq_login: str,
        rabbitmq_password: str,
        queue_name: str,
        exchange_name: str,
        routing_key: str,
    ):
        super().__init__(
            rabbitmq_host, rabbitmq_port, rabbitmq_login, rabbitmq_password, queue_name, exchange_name, routing_key
        )
        self.event_service = EventService(EventCacheService(settings.redis.url))

    async def callback(
        self,
        message: AbstractIncomingMessage,
    ) -> None:
        async with message.process():
            event = EventSchema(**json.loads(message.body))
            await self.event_service._cache.open()
            await self.event_service.update_events(event)
            await self.event_service._cache.close()
            await message.ack()
