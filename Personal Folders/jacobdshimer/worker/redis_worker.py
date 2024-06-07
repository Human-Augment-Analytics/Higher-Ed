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
        self.input = process_func
        # TODO: Define this as the output
        self.output = None
        self.timeout = timeout

    async def work(self, source: str):
        wip_queue = f'{source}_wip'
        ingest_queue = f'{source}_ingest'
        while True:
            try:
                search_string = await self.queue.dequeue(source, timeout=self.timeout, wip_queue=wip_queue)
                if search_string:
                    logger.info('Processing message...')
                    results = await self.input(search_string)
                    logger.info(f'Processing message returned {len(results)} from the search')
                    logger.info('Deleting from the wip queue')
                    await self.queue.delete(wip_queue, search_string)
                    # TODO: Use the output function
                    logger.info(f'Queueing the results to {ingest_queue}')
                    with open('test.json', 'w+') as outfile:
                        import json
                        json.dump(results, outfile, indent=4)
                    await self.queue.enqueue(ingest_queue, results)
                    logger.info('DONE')
                else:
                    logger.info(f'No message received in {self.timeout}')
            except asyncio.CancelledError:
                # Handle cancellation
                print(f'Task for {source} cancelled.')
                break
