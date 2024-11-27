from pydantic import Field, field_validator, field_serializer, BaseModel, model_serializer
from uuid import UUID
from decimal import Decimal
from src.models.bet import BetState


class BetCreate(BaseModel):
    event_id: UUID
    summary: Decimal = Field(gt=0, decimal_places=2)

    @field_validator("event_id", mode="before")
    def convert_uuid(cls, v):
        if isinstance(v, str):
            return UUID(v)
        return v

    @field_serializer("event_id")
    def serialize_uuid(cls, v):
        return str(v)


class BetGet(BetCreate):
    id: UUID
    status: BetState

    @model_serializer(mode="plain")
    def serialize_model(self):
        serialized_data = {}

        serialized_data["status"] = self.status.name
        serialized_data["summary"] = float(self.summary)
        serialized_data["id"] = str(self.id)
        serialized_data["event_id"] = str(self.event_id)
        return serialized_data
