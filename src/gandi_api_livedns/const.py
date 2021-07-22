"""Constants for the gandi_api_livedns."""

DEFAULT_TIMEOUT = 15  # in seconds
DEFAULT_TTL = 3600
DEFAULT_TYPE = "A"
DEFAULT_IPV6 = False

AVAILABLE_TYPE = [
    "A",
    "AAAA",
    "MX",
]

IPV4_PROVIDER_URL = "https://api.ipify.org"
IPV6_PROVIDER_URL = "https://api6.ipify.org"

GANDI_LIVEDNS_API_URL = (
    "https://api.gandi.net/v5/livedns/domains/{domain}/records/{rrname}/{rrtype}"
)

