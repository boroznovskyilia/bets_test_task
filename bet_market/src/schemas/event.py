from pydantic import Field, BaseModel, model_validator, model_serializer
from uuid import UUID
from decimal import Decimal
from src.models.bet import BetState
from datetime import datetime


class EventSchema(BaseModel):
    id: UUID
    status: BetState
    koef: Decimal = Field(gt=0, decimal_places=2)
    end_datetime: datetime

    @model_validator(mode="before")
    def convert_fields(cls, data: dict) -> dict:
        if isinstance(data.get("id"), str):
            try:
                data["id"] = UUID(data["id"])
            except ValueError:
                raise ValueError(f"Invalid UUID: {data['id']}")

        if isinstance(data.get("status"), str):
            try:
                data["status"] = BetState[data["status"]]
            except KeyError:
                raise ValueError(f"Invalid status name: {data['status']}")

        if "koef" in data:
            data["koef"] = Decimal(data["koef"]).quantize(Decimal("0.01"))

        if isinstance(data.get("end_datetime"), str):
            data["end_datetime"] = datetime.fromisoformat(data["end_datetime"])

        return data

    @model_serializer(mode="plain")
    def serialize_model(self):
        serialized_data = {}

        serialized_data["status"] = self.status.name
        serialized_data["koef"] = float(self.koef)
        serialized_data["end_datetime"] = self.end_datetime.isoformat()
        serialized_data["id"] = str(self.id)
        return serialized_data
