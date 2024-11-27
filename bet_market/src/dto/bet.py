from uuid import UUID
from pydantic import BaseModel, Field
from decimal import Decimal
from src.models.bet import BetState


class BetDto(BaseModel):
    event_id: UUID
    status: BetState = BetState.NEW
    summary: Decimal = Field(gt=0, decimal_places=2)
