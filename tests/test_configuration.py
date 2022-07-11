"""Test all configuration details."""
import unittest


class TestConfiguration(unittest.TestCase):
    """Tests the configuration reading"""
    def test_valid_configuration(self):
        """Check all data types are valid, mandatory field are presents."""
        raise NotImplementedError("Configuration is not implemented.")

    def test_invalid_configuration(self):
        """Test multiple configuration issues, configuration issues should be logged and a
        ConfigurationError should be raised."""
        raise NotImplementedError("Configuration is not implemented.")

    def test_invalid_driver(self):
        """Test driver is invalid. Should log the issue and raise ConfigurationError."""
        raise NotImplementedError("Configuration is not implemented.")

    def test_invalid_driver_configuration(self):
        """Test driver configuration is invalid. Should log the issue and raise
        ConfigurationError."""
        raise NotImplementedError("Configuration is not implemented.")


if __name__ == '__main__':
    unittest.main()
