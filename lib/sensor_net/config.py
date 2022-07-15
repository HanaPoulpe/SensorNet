"""Base configuration manager."""
import dataclasses
import re
from typing import Callable, Iterable

from .drivers import BackendDriver


class _EndpointWalker:
    """
    Iterable of endpoint from ip list.

    List of IPs like:
    - 0.0.0.0
    - 0.0.0.0/32
    - 0.0.0.1 - 0.0.0.20
    """

    def __init__(self, ip_list: list[str]):
        """
        Prepare the endpoint walker.

        :param ip_list: List of IP  to walk
        """
        self._list: list[Callable[[], Iterable[str]]] = []
        (self._append_group(ip) for ip in ip_list)

    def _append_group(self, ip: str):
        single_ip = r"^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$"
        ip_mask = r"^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}/\\d{1,2}$"
        ip_list = ("^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3} - "
                   "\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$")
        if re.match(single_ip, ip):
            self._list.append(lambda: (ip, ))
            return

        if re.match(ip_mask, ip):
            raise NotImplementedError("IP with mask is not implemented.")

        if re.match(ip_list, ip):
            raise NotImplementedError("IP list is not implemented.")

    def __iter__(self):
        raise NotImplementedError("IP iteration is not implemented.")

    def __next__(self) -> str:
        raise NotImplementedError("IP iteration is not implemented.")


@dataclasses.dataclass
class NetworkConfig:
    """Network configuration class."""

    name: str
    api_endpoints: Iterable[str] = dataclasses.field(init=False, repr=False)
    ip_addresses: list[str]
    sensor_prefix: str
    cron: str
    api_port: int = dataclasses.field(default=80)
    api_location: str = dataclasses.field(default="/")

    def __post_init__(self):
        """Completes dataclasses initialization."""
        self.api_endpoints = _EndpointWalker(self.ip_addresses)


@dataclasses.dataclass
class ApplicationConfig:
    """Application configuration class."""

    daemon_name: str
    backend: dict
    driver: BackendDriver = dataclasses.field(init=False)
    networks: list[dict]
    network_setup: list[NetworkConfig] = dataclasses.field(init=False)

    def __post_init__(self):
        """Complete dataclass initialization."""
        raise NotImplementedError("Application configuration is not implemented.")


def get_configuration(filename: str | None) -> ApplicationConfig:
    """
    Retrieve configuration from file.

    :param filename: [Optional] Configuration YAML file
    :return: Application configuration
    """
    raise NotImplementedError("Configuration is not implemented.")
