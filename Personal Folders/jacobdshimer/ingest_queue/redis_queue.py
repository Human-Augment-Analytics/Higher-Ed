from .base import BaseQueue

from redis.asyncio import Redis


class RedisQueue(BaseQueue):
    def __init__(self, host: str, port: str = '6379', db: int = 0, password: str | None = None) -> None:
        self.conn = Redis(
            host=host,
            port=port,
            db=db,
            password=password
        )

    async def healthcheck(self):
        await self.conn.ping()

    async def enqueue(self, source: str, search: str):
        await self.conn.lpush(source, search)

    async def dequeue(self, source: str, **kwargs) -> tuple[str, str]:
        timeout: int | None = kwargs.get('timeout')
        wip_queue: str = kwargs.get('wip_queue')
        search_url: str = await self.conn.blmove(source, wip_queue, timeout)
        return search_url

    async def delete(self, wip_queue: str, url: str):
        await self.conn.lrem(wip_queue, 1, url)
