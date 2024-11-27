import pytest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.repositories.bet import BetRepository
from src.models import Bet
from src.dto.bet import BetDto, BetState
from uuid import uuid4
from decimal import Decimal
from datetime import datetime


@pytest.mark.asyncio
class TestBetRepository:
    @pytest.fixture
    def mock_session(self):
        return MagicMock(spec=AsyncSession)

    async def test_get_all(self, mock_session):
        mock_bets = [MagicMock(), MagicMock()]
        mock_session.scalars.return_value = mock_bets

        result = await BetRepository.get_all(mock_session)
        
        assert result == mock_bets

    async def test_get_by_id(self, mock_session):
        mock_bet_id = uuid4()
        mock_bet = MagicMock(id=mock_bet_id)
        mock_session.scalar.return_value = mock_bet

        result = await BetRepository.get_by_id(mock_bet_id, mock_session)

        assert result == mock_bet

    async def test_create(self, mock_session):
        mock_bet_data = BetDto(event_id=uuid4(), status=BetState.NEW, summary=Decimal(1))
        mock_bet_id = uuid4()
        mock_bet = MagicMock(id=None, **mock_bet_data.model_dump())

        def add_side_effect(bet):
            bet.id = mock_bet_id

        mock_session.add = MagicMock(side_effect=add_side_effect)
        mock_session.flush = AsyncMock()

        result = await BetRepository.create(mock_bet, mock_session)

        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()

        assert result == mock_bet_id