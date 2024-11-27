from aio_pika import connect_robust, ExchangeType
from abc import abstractmethod
from aio_pika.abc import AbstractIncomingMessage
from src.services.consumers import AbstractConsumer


class RabbitMQConsumer(AbstractConsumer):
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
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_login = rabbitmq_login
        self.rabbitmq_password = rabbitmq_password
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.connection = None
        self.channel = None

    async def connect(self):
        """Establish connection and channel."""
        self.connection = await connect_robust(
            host=self.rabbitmq_host, port=self.rabbitmq_port, login=self.rabbitmq_login, password=self.rabbitmq_password
        )
        self.channel = await self.connection.channel()

        exchange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.DIRECT, durable=True)
        queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await queue.bind(exchange, routing_key=self.routing_key)

        return queue

    @abstractmethod
    async def callback(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            print(" [x] %r:%r" % (message.routing_key, message.body))

    async def start_consuming(self):
        """Start consuming messages."""
        if not self.connection or not self.channel:
            queue = await self.connect()
        else:
            queue = await self.channel.get_queue(self.queue_name)

        print(f"Started consuming on queue: {self.queue_name}")

        await queue.consume(callback=self.callback)

    async def close_connection(self):
        """Close connection."""
        if self.connection:
            await self.connection.close()
