from pydantic import BaseModel, Field, model_serializer
from uuid import UUID
from decimal import Decimal
from src.models.event import EventState
from datetime import datetime


class EventCreate(BaseModel):
    status: EventState
    koef: Decimal = Field(gt=0, decimal_places=2)
    end_datetime: datetime = Field(default=datetime.now())


class EventGet(EventCreate):
    id: UUID

    @model_serializer(mode="plain")
    def serialize_model(self):
        serialized_data = {}

        serialized_data["status"] = self.status.name
        serialized_data["koef"] = float(self.koef)
        serialized_data["end_datetime"] = self.end_datetime.isoformat()
        serialized_data["id"] = str(self.id)
        return serialized_data
