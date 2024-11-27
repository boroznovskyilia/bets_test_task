from aio_pika import connect_robust, ExchangeType, Message
import json
from abc import abstractmethod


class RabbitMQProducer:
    def __init__(
        self,
        rabbitmq_host: str,
        rabbitmq_port: int,
        rabbitmq_login: str,
        rabbitmq_password: str,
        exchange_name: str,
        routing_key: str,
    ):
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_login = rabbitmq_login
        self.rabbitmq_password = rabbitmq_password
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        """Establish connection and channel."""
        self.connection = await connect_robust(
            host=self.rabbitmq_host,
            port=self.rabbitmq_port,
            login=self.rabbitmq_login,
            password=self.rabbitmq_password,
        )
        self.channel = await self.connection.channel()

        # Declare exchange
        self.exchange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.DIRECT, durable=True)

    @abstractmethod
    async def publish(self, message: dict):
        """Publish message to exchange with routing key."""
        if not self.exchange:
            raise ConnectionError("Connection to RabbitMQ is not established. Call 'connect' first.")

        message_body = json.dumps(message).encode()
        await self.exchange.publish(Message(body=message_body), routing_key=self.routing_key)
        print(f" [x] Sent message to {self.exchange_name} with key {self.routing_key}")

    async def close_connection(self):
        """Close connection."""
        if self.connection:
            await self.connection.close()
