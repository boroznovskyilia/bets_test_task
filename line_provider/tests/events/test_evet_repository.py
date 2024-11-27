import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock
from src.repositories.event import EventRepository
from src.schemas.event import EventCreate, EventState
from uuid import uuid4
from decimal import Decimal
from datetime import datetime


@pytest.mark.asyncio
class TestEventRepository:
    @pytest.fixture
    def mock_session(self):
        return MagicMock(spec=AsyncSession)

    async def test_get_all(self, mock_session):
        mock_session.scalars.return_value = [MagicMock(), MagicMock()]
        result = await EventRepository.get_all(mock_session)

        mock_session.scalars.assert_called_once()
        assert len(result) == 2

    async def test_get_by_id(self, mock_session):
        mock_event_id = uuid4()
        mock_event = MagicMock(id=mock_event_id)
        mock_session.scalar.return_value = mock_event

        result = await EventRepository.get_by_id(mock_event_id, mock_session)

        mock_session.scalar.assert_called_once()
        assert result == mock_event

    async def test_create(self, mock_session):
        mock_event_data = EventCreate(koef=Decimal(1), status=EventState.NEW, end_datetime=datetime.now())
        mock_event = MagicMock(id=uuid4(), **mock_event_data.model_dump())
        mock_session.flush = AsyncMock()
        result = await EventRepository.create(mock_event_data, mock_session)
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()
        assert result.end_datetime == mock_event.end_datetime

    async def test_update_status(self, mock_session):
        mock_event_id = uuid4()
        mock_new_status = EventState.SECOND_WIN

        await EventRepository.update_status(mock_event_id, mock_new_status, mock_session)

        mock_session.execute.assert_called_once()