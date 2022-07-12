"""Backend driver Stub package"""
import sensor_net
import sensor_net.errors


def _get_driver(name: str, config: dict):
    raise RuntimeError("StubBackend is not available.")


get_driver = _get_driver


class StubBackendDriver:
    """Stub backend driver."""

    def __init__(self, name: str, parent: 'StubBackend'):
        """
        :param parent: StubBackend attached to this backend driver.
        """
        self.__parent = parent
        self.__name = name
        self.__parent.register_driver(name, self)

    def write(
            self,
            network_name: str,
            network_prefix: str,
            sensor_address: str,
            data: list[sensor_net.SensorData]
    ):
        """
        Register writes to the stub backend
        :param network_name: Network name, not used
        :param network_prefix: Network prefix, not used
        :param sensor_address: Sensor address, not used
        :param data: Sensor data, stored in the stub backend writes
        """
        self.__parent.register_write(
            self.__name,
            data
        )


class StubBackend:
    """
    Complete backend stub.

    >>> import datetime
    >>> stub = StubBackend()
    >>> stub.start()
    >>> backend_driver = get_driver("stub", {})
    >>> backend_driver.write("stub_net", "stb", "0.0.0.0",
    >>>     [sensor_net.SensorData("heartbeat", 0, datetime.datetime.utcnow())])
    >>> assert len(stub.writes) == 1
    >>> stub.stop()

    :attribute writes: List of tuples (driver name, write call attributes)
    :attribute drivers: List of drivers name registered
    :attribute config_error: get_driver will raise a BackendConfigError if True
    :attribute write_error: write will raise a BackendWriteError if True
    """

    def __init__(self, config_error: bool = False, write_error: bool = False):
        """
        Creates a new StubBackend

        :param config_error: get_driver will raise a BackendConfigError if True
        :param write_error: write will raise a BackendWriteError if True
        """
        self.config_error = config_error
        self.write_error = write_error
        self._drivers: dict[str, StubBackendDriver] = {}
        self._writes: list[tuple[str, sensor_net.SensorData]] = []

    def start(self):
        """Begin the stub of backend driver."""
        global get_driver
        get_driver = self

    def __enter__(self):
        self.start()

    @staticmethod
    def stop():
        global get_driver
        get_driver = _get_driver

    def __exit__(self, exc_type, exc_val, exc):
        self.stop()

    def __call__(self, name: str, configuration: dict) -> StubBackendDriver:
        """Replaces get_config while stubbing"""
        if self.config_error:
            raise sensor_net.errors.BackendConfigError(name, "Stub sets to raise an exception.")
        return StubBackendDriver(name, self)

    def register_driver(self, name: str, driver: StubBackendDriver):
        """
        Registers a new driver

        :param name: Driver name
        :param driver: Driver instance
        """
        self._drivers[name] = driver

    def register_write(self, name: str, write: list[sensor_net.SensorData]):
        """
        Registers write to the backend driver.

        :param name: Driver name
        :param write: list of sensor data
        """
        if self.write_error:
            raise sensor_net.errors.BackendWriteError(name, "Stub sets to raise an exception.")

        [self._writes.append((name, d,)) for d in write]

    @property
    def drivers(self) -> dict[str, StubBackendDriver]:
        """Maps to driver_name -> driver"""
        return self._drivers

    @property
    def writes(self) -> list[tuple[str, sensor_net.SensorData]]:
        """List of all writes send to this stub"""
        return self._writes
