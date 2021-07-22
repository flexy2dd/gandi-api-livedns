"""Provides the Gandi.net live DNS access API."""
import asyncio
import aiohttp
import logging
from aiohttp.hdrs import AUTHORIZATION
import async_timeout

from .const import (
    DEFAULT_TIMEOUT,
    DEFAULT_TTL,
    DEFAULT_TYPE,
    DEFAULT_IPV6,
    GANDI_LIVEDNS_API_URL,
    IPV4_PROVIDER_URL,
    IPV6_PROVIDER_URL
)

class GandiApiLiveDNS:
    """Representation of a Gandi.net API."""

    def __init__(self, 
                 domain = '', 
                 apikey = '', 
                 rrname = '', 
                 rrtype = DEFAULT_TYPE, 
                 rrttl = DEFAULT_TTL, 
                 ipv6 = DEFAULT_IPV6, 
                 timeout = DEFAULT_TIMEOUT, 
                 logger=None) -> None:
        """Initialize a Gandi.net API."""
        
        if logger==None:
            self._logger = logging.getLogger(__name__)
        else:
            self._logger = logger

        self.domain = domain
        self.apikey = apikey
        self.rrname = rrname
        self.rrtype = rrtype
        self.rrttl = rrttl
        self.ipv6 = ipv6
        self.timeout = timeout

    async def getRealIP(self):
        """Get real external IP."""

        self._logger.debug("Get real ip...")

        url = IPV4_PROVIDER_URL

        if self.ipv6:
            url = IPV6_PROVIDER_URL

        self._logger.debug("Get real ip from %s", url)

        try:
            with async_timeout.timeout(self.timeout):
                async with aiohttp.ClientSession() as session:    
                    resp = await session.get(url)
                    body = await resp.text()
                    self._logger.debug("Real IP: %s - %s", resp.status, body)
                    if resp.status == 200:
                        return body
                    else:
                        return False

        except aiohttp.ClientError:
            self._logger.warning("Can't connect for getting real ip")

        except asyncio.TimeoutError:
            self._logger.warning("Timeout from real ip getting")

        return False

    async def getDNSRecord(self):
        """Get the rrset_values entry in Gandi.net API."""

        error = None
        record = None

        url_params = {
            "domain": self.domain,
            "rrname": self.rrname,
            "rrtype": self.rrtype,
        }

        url = GANDI_LIVEDNS_API_URL.format(**url_params)
        headers = {AUTHORIZATION: f"Apikey {self.apikey}"}

        self._logger.debug("Request url: %s", url)

        try:
            with async_timeout.timeout(self.timeout):
                async with aiohttp.ClientSession() as session:
                    resp = await session.get(url, headers=headers)
                    body = await resp.json()

                    self._logger.debug("Getting %s: (%s) %s", url, resp.status, body)
                    
                    if resp.status == 200:
                        record = body["rrset_values"][0]
                    elif resp.status == 404:
                        self._logger.debug("Not found")
                        error = "record_notfound"
                    else:
                        self._logger.debug(
                            "Getting %s failed: (%s) %s", url, resp.status, body
                        )
                        error = "cannot_connect"

        except aiohttp.ClientError:
            error = "cannot_connect"
            self._logger.warning("Can't connect to API")

        except asyncio.TimeoutError:
            error = "timeout_connect"
            self._logger.warning("Timeout from API for: %s", url)

        return record, error

    async def updateDNSRecord(self):
        """Update the rrset_values and rrset_ttl entry in Gandi.net API."""

        error = None
        record = None

        self._logger.debug("Getting current real ip")
        current_ip = await self.getRealIP()
        if not current_ip:
            self._logger.warning("Can't get the real ip")
            return record, "cannot_get_realip"

        self._logger.debug("Getting current DNS record ip")
        current_gandi_ip, error = await self.getDNSRecord()
        if not current_gandi_ip:
            self._logger.warning("Can't get the current dns ip")
            return record, error

        self._logger.debug("Check if needed update")
        if current_gandi_ip == current_ip:
            self._logger.debug("No need update dns")
            return current_gandi_ip, error

        url_params = {
            "domain": self.domain,
            "rrname": self.rrname,
            "rrtype": self.rrtype,
        }

        url = GANDI_LIVEDNS_API_URL.format(**url_params)
        json = {"rrset_ttl": self.rrttl, "rrset_values": [current_ip]}
        headers = {AUTHORIZATION: f"Apikey {self.apikey}"}

        self._logger.debug("Update DNS record")
        try:
            with async_timeout.timeout(self.timeout):
                async with aiohttp.ClientSession() as session:
                    resp = await session.put(url, json=json, headers=headers)
                    body = await resp.text()
                    
                    if resp.status == 201:
                        self._logger.info(
                            "Record updated with ttl: %s ip: %s", self.rrttl, current_ip
                        )
                        record = current_ip
                    else:
                        self._logger.warning(
                            "Updating %s failed: (%s) %s", url, resp.status, body
                        )
                        error = "update_failed"

        except aiohttp.ClientError:
            error = "cannot_connect"
            self._logger.warning("Can't connect to API")

        except asyncio.TimeoutError:
            error = "timeout_connect"
            self._logger.warning("Timeout from API for: %s", self.domain)

        return record, error
