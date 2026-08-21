import ipaddress
from urllib.parse import urlparse

from pydantic_core import PydanticCustomError

BLOCKED_HOSTS = {"localhost", "0.0.0.0"}


def validate_monitor_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise PydanticCustomError("url_scheme", "Only http:// and https:// URLs are allowed")
    if not parsed.hostname:
        raise PydanticCustomError("url_host", "URL must include a host")
    host = parsed.hostname.lower()
    if host in BLOCKED_HOSTS or host.endswith(".localhost"):
        raise PydanticCustomError("url_host_blocked", "Local/internal hosts are not allowed")
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return parsed.geturl()
    if any(
        (
            ip.is_private,
            ip.is_loopback,
            ip.is_link_local,
            ip.is_unspecified,
            ip.is_reserved,
            ip.is_multicast,
        )
    ):
        raise PydanticCustomError("url_host_blocked", "Local/internal IPs are not allowed")
    return parsed.geturl()
