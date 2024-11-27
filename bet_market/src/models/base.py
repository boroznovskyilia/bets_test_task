from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime
import uuid
import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    created = Column(DateTime, default=func.now())

    updated = Column(DateTime, default=func.now(), onupdate=func.now())
