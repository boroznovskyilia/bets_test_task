from aio_pika import connect_robust, ExchangeType
from abc import abstractmethod
from aio_pika.abc import AbstractIncomingMessage
from abc import ABC


class AbstractConsumer(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def callback(self, message: AbstractIncomingMessage) -> None:
        pass

    @abstractmethod
    async def start_consuming(self):
        pass

    @abstractmethod
    async def close_connection(self):
        pass
