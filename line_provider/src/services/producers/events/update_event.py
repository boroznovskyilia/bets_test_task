from src.services.producers.base import RabbitMQProducer
import json
from aio_pika import Message


class UpdateEventMQProducer(RabbitMQProducer):
    async def publish(self, message: dict):
        """Publish message to exchange with routing key."""
        if not self.exchange:
            raise ConnectionError("Connection to RabbitMQ is not established. Call 'connect' first.")

        message_body = json.dumps(message).encode()
        await self.exchange.publish(Message(body=message_body), routing_key=self.routing_key)
