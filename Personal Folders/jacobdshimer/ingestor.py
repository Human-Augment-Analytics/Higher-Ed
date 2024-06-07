import asyncio
import logging
import signal

from endpoint.gbif import gbif_search
from ingest_queue import RedisQueue
from worker import RedisWorker

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def main():
    queue = RedisQueue('localhost')
    await queue.healthcheck()
    workers = [
        ('gbif', RedisWorker(queue, gbif_search))
    ]

    tasks = [
        asyncio.create_task(worker.work(source))
        for source, worker in workers
    ]

    loop = asyncio.get_running_loop()
    stop = loop.create_future()

    def shutdown():
        print('Received stop signal, shutting down...')
        stop.set_result(None)

    loop.add_signal_handler(signal.SIGINT, shutdown)
    loop.add_signal_handler(signal.SIGTERM, shutdown)

    # Wait for the stop signal
    await stop

    # Cancel all tasks
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    await queue.conn.aclose()

if __name__ == '__main__':
    asyncio.run(main())
