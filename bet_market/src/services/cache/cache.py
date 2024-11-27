from redis import asyncio as redis
from typing import Optional


class CacheService:
    def __init__(self, url: str):
        self._url = url
        self._redis = None

    async def open(self):
        self._redis = await redis.from_url(self._url, decode_responses=True)

    async def close(self):
        if self._redis:
            await self._redis.close()

    async def get(self, key: str) -> Optional[str]:
        if self._redis:
            return await self._redis.get(key)
        return None

    async def set(self, key: str, value: str, expire: int = 30):
        if self._redis:
            await self._redis.set(key, value, ex=expire)

    async def delete(self, key: str):
        if self._redis:
            await self._redis.delete(key)
