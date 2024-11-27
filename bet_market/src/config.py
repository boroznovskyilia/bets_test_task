from enum import IntEnum, unique
from typing import Annotated

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


@unique
class LoggingLevel(IntEnum):
    CRITICAL: int = 50
    ERROR: int = 40
    WARNING: int = 30
    INFO: int = 20
    DEBUG: int = 10


class LoggingSettings(BaseModel):
    level: int = LoggingLevel.WARNING
    format: str = "%(asctime)s %(name)s %(levelname)s: %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"


class AppSettings(BaseModel):
    host: str
    port: int


class RedisSettings(BaseModel):
    url: str


class Rabbitmq(BaseModel):
    host: str
    port: int
    user: str
    password: str
    management_port: int


class LineProvider(BaseModel):
    url_events: str


class DatabaseSettings(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str
    pool_size: int
    log_level: int
    ssl: bool = False

    @property
    def url(self) -> Annotated[str, PostgresDsn]:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}" f"/{self.name}"


class CORSSettings(BaseModel):
    credentials: bool = False
    headers_as_string: str
    methods_as_string: str
    origins_as_string: str

    @staticmethod
    def _prepare_parameters_to_list(parameter: str) -> list[str]:
        return [value.strip() for value in parameter.split(",")]

    @property
    def headers(self) -> list[str]:
        return self._prepare_parameters_to_list(self.headers_as_string)

    @property
    def methods(self) -> list[str]:
        return self._prepare_parameters_to_list(self.methods_as_string)

    @property
    def origins(self) -> list[str]:
        return self._prepare_parameters_to_list(self.origins_as_string)


class PaginationParams(BaseModel):
    offset: int
    limit: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(".env",),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_ignore_empty=True,
        extra="ignore",
    )

    app: AppSettings
    cors: CORSSettings
    db: DatabaseSettings
    redis: RedisSettings
    rabbitmq: Rabbitmq
    logging: LoggingSettings = LoggingSettings()
    pagination: PaginationParams
    line_provider: LineProvider


settings = Settings()
