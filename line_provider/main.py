import logging
from contextlib import asynccontextmanager
from time import time

from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse

from src.config import settings
from src.routers.router import router
from src.services.producers.events.update_event import UpdateEventMQProducer

logging.basicConfig(
    level=settings.logging.level,
    datefmt=settings.logging.date_format,
    format=settings.logging.format,
)

logger = logging.getLogger(__name__)

update_producer = UpdateEventMQProducer(
    rabbitmq_host=settings.rabbitmq.host,
    rabbitmq_port=settings.rabbitmq.port,
    rabbitmq_login=settings.rabbitmq.user,
    rabbitmq_password=settings.rabbitmq.password,
    # queue_name="update_queue",
    exchange_name="events_state",
    routing_key="update",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting RabbitMQ producer...")

    yield


openapi_url = "/openapi.json"

app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    # middleware=MIDDLEWARES,
    openapi_url=openapi_url,
)


@app.middleware("http")
async def log_request(request: Request, call_next):
    start_request: float = time()
    body = await request.body()
    response: Response = await call_next(request)
    logger.info(
        f"Request path: {request.url.path} "
        f"status code: {response.status_code} "
        f"duration: {round(time() - start_request, 3)} s "
        f"request body: {body.decode('utf-8')}",
    )
    return response


app.include_router(router)
