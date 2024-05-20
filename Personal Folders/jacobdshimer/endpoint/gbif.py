import httpx
from logging import getLogger

logger = getLogger('endpoint.gbif')


async def gbif_search(url) -> None:
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == 200:
            try:
                data = r.json()
                logger.info(data)
            except Exception:
                logger.exception('Failed to parse the response to json')
        else:
            logger.error(f'URL: {url} responded with something other then 200: {r.status_code}, {r.text}')
