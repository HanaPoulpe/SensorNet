"""Contains all common modules required for sensornet to work."""
from . import _version
from .types import SensorData, sensor_data_guard
from .cmdline import main

__version__ = _version.get_versions()['version']
__all__ = ['SensorData', 'sensor_data_guard', 'main']

if __name__ == '__main__':
    main()
