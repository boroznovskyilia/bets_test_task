from src.services.cache.cache import CacheService
import json
from typing import Optional
from src.schemas.bet import BetGet


class BetCacheService(CacheService):
    async def get(self, key: str) -> Optional[str]:
        if self._redis:
            serialized_value = await self._redis.get(key)
            if serialized_value:
                bets = json.loads(serialized_value)
                return [BetGet(**json.loads(bet)) for bet in bets]
        return []

    async def set(self, key: str, bets: list[BetGet], expire: int = 5):
        if self._redis:
            value = json.dumps([bet.model_dump_json() for bet in bets])
            await self._redis.set(key, value, ex=expire)
