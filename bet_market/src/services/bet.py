from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.bet import BetDto
from src.repositories.bet import BetRepository
from src.schemas.bet import BetGet
from src.services.cache import BetCacheService


class BetService:
    def __init__(self, bet_repository, cache_service):
        self._bet_repository: BetRepository = bet_repository
        self._cache: BetCacheService = cache_service

    async def register_bet(self, bet: BetDto, session: AsyncSession):
        return await self._bet_repository.create(bet, session)

    async def get_all_bets(self, session: AsyncSession):
        cached_bets = await self._cache.get("bets")
        if cached_bets:
            return cached_bets
        bets = await self._bet_repository.get_all(session)
        bets_res = [BetGet.model_validate(bet, from_attributes=True) for bet in bets]
        await self._cache.set("bets", bets_res)
        return bets_res
