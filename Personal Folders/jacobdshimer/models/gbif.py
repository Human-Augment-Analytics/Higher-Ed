import json
from logging import getLogger

logger = getLogger('models.gbif')


async def process_ingest_request(ingest_data):
    try:
        data = json.loads(ingest_data)
    except Exception:
        logger.exception('Failed to parse the data from the ingest queue')
