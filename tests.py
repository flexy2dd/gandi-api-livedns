import logging
import aiohttp
import asyncio
from src.gandi_api_livedns import GandiApiLiveDNS

_LOGGER = logging.getLogger(__name__)

gandiApiLiveDNS = GandiApiLiveDNS(
    {
        'pochot.com',
        'CONF_API_KEY',
        'hass',
        'A',
        3600,
        False,
        10,
    },
    _LOGGER,
)


gandiApiLiveDNS.domain = 'pochot.com'

#session = await aiohttp.ClientSession()

async def update_records():
  await gandiApiLiveDNS.getRealIP()

loop = asyncio.get_event_loop()
loop.run_until_complete(gandiApiLiveDNS.getDNSRecord())


