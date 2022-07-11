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
