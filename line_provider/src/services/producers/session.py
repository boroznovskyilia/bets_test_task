from collections.abc import AsyncGenerator
from src.services.producers import UpdateEventMQProducer


class UpdateMQDependency:
    def __init__(self, mq_service: UpdateEventMQProducer = None):
        self.mq_service = mq_service

    async def __call__(self) -> AsyncGenerator[UpdateEventMQProducer, None]:
        self.mq_service = self.mq_service
        await self.mq_service.connect()
        try:
            yield self.mq_service
        finally:
            await self.mq_service.close_connection()
