"""Errors package"""


class BackendError(Exception):
    """Backend Error"""

    def __init__(self, backend_name: str, message: str, *args):
        """
        Backend error are raised when an error occurs in the backend.

        :param backend_name: Name of the backend
        :param message: Error message
        :param args: other arguments
        """
        super().__init__(backend_name + ":" + message, *args)
        self.backend_name = backend_name
        self.message = message


class BackendWriteError(BackendError):
    """Backend Write Error"""

    pass


class SensorError(Exception):
    """Error while accessing sensor API."""

    def __init__(self, sensor_address: str, message: str, *args):
        """
        Sensor error are raised when an error occurs while accessing sensor API.

        :param sensor_address: Address of the sensor
        :param message: Error message
        :param args: other arguments
        """
        super().__init__(sensor_address + ":" + message, *args)
        self.sensor_address = sensor_address
        self.message = message


class SensorReadError(SensorError):
    """Sensor Read Error."""

    pass


class SensorDataTypeError(SensorError):
    """Sensor Data Type Error."""

    pass
