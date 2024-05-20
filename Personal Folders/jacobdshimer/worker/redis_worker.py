from ingest_queue.redis_queue import RedisQueue
from .base import Worker

import asyncio
from logging import getLogger
from typing import Awaitable, Callable

MessageProcessFunc = Callable[[str], Awaitable[None]]
logger = getLogger('worker.redis')


class RedisWorker(Worker):
    def __init__(self, queue: RedisQueue, process_func: MessageProcessFunc, timeout: int | None = 10):
        self.queue = queue
        self.process_message = process_func
        self.timeout = timeout

    async def work(self, source: str):
        wip_queue = f'{source}_wip'
        while True:
            try:
                search_url = await self.queue.dequeue(source, timeout=self.timeout, wip_queue=wip_queue)
                if search_url:
                    logger.info('Processing message...')
                    await self.process_message(search_url)
                    logger.info('Deleting from the wip queue')
                    await self.queue.delete(wip_queue, search_url)
                else:
                    logger.info(f'No message received in {self.timeout}')
            except asyncio.CancelledError:
                # Handle cancellation
                print(f'Task for {source} cancelled.')
                break
