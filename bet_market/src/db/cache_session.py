from collections.abc import AsyncGenerator
from src.services.cache.cache import CacheService


class CacheDependency:
    def __init__(self, cache_service: CacheService = None):
        self.cache_service = cache_service

    async def __call__(self) -> AsyncGenerator[CacheService, None]:
        self.cache_service = self.cache_service
        await self.cache_service.open()
        try:
            yield self.cache_service
        finally:
            await self.cache_service.close()
