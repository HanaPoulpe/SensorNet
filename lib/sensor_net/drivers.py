"""Defines drivers protocols."""
import typing

from .types import SensorData


class BackendDriver(typing.Protocol):
    """Basic backend driver."""

    def write(self, datas: typing.Iterable[SensorData]):
        """
        Writes datas to the backend.

        :param datas: Collection of sensor data to write to the backend.
        :raise BackendWriteError: if writes fails.
        """
        ...


get_driver: typing.TypeAlias = typing.Callable[[str, dict], BackendDriver]


class SensorDriver(typing.Protocol):
    """Basic sensor driver."""

    def read(self, url: str) -> typing.Iterable[SensorData]:
        """
        Reads sensor data from the driver.

        :param url: Sensor complete URL "http://host:port/api_location
        :return: Collection of sensor data.
        :raise APIReadError: if reads fails.
        """
        ...


get_sensor_driver: typing.TypeAlias = typing.Callable[[str, dict], SensorDriver]
