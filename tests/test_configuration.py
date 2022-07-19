"""Test all configuration details."""
import logging
import os
import unittest

import sensor_net.backend_driver.stubber
import sensor_net.config
import sensor_net.errors


class TestConfiguration(unittest.TestCase):
    """Tests the configuration reading"""

    def setUp(self):
        """
        Defines configuration files base location
        Prepare StubBackendDriver
        Set logger level to DEBUG
        """
        logging.basicConfig(level=logging.DEBUG)

        self.config_path = os.path.join(os.path.dirname(__file__), "configuration")
        self.backend_driver = sensor_net.backend_driver.stubber.StubBackend()
        self.backend_driver.start()

    def tearDown(self) -> None:
        self.backend_driver.stop()

    def assertNetwork(
            self,
            network: sensor_net.config.NetworkConfig,
            name: str,
            sensor_prefix: str,
            api_port: int,
            api_location: str,
            cron: str,
            ip_count: int,
            first_ip: str,
            last_ip: str,
    ):
        """Test NetworkConfig vs expected parameters"""
        self.assertEqual(network.name, name, "Invalid network name.")
        self.assertEqual(network.sensor_prefix, sensor_prefix, "Invalid sensor prefix.")
        self.assertEqual(network.api_port, api_port, "Invalid API port.")
        self.assertEqual(network.api_location, api_location, "Invalid API location.")
        self.assertEqual(network.cron, cron, "Invalid cron string.")

        first = None
        count = 0
        last = None
        for ip in network.api_endpoints:
            if not first:
                first = ip
            count += 1
            last = ip
        self.assertEqual(first, first_ip, "Invalid first IP address.")
        self.assertEqual(last, last_ip, "Invalid last IP address.")
        self.assertEqual(count, ip_count, "Invalid number of IP addresses.")

    def test_valid_configuration(self):
        """Check all data types are valid, mandatory field are presents."""
        config = sensor_net.config.get_configuration(os.path.join(self.config_path, "valid.yaml"))

        self.assertEqual(
            config.daemon_name,
            "test_valid_config",
            "Daemon names is not as expected.",
        )
        self.assertDictEqual(
            config.backend,
            {"driver": "stubber"},
            "Driver should be stubber.",
        )
        self.assertIsInstance(
            config.driver,
            sensor_net.backend_driver.stubber.StubBackendDriver,
            "Invalid backend driver type."
        )
        self.assertEqual(len(config.network_setup), 3, "3 networks should be present.")
        net_conf = [
            {
                "name": "test_net0",
                "sensor_prefix": "tst0",
                "api_port": 80,
                "api_location": "/",
                "cron": "* * * * * *",
                "first_ip": "127.0.0.1",
                "last_ip": "127.0.0.1",
                "ip_count": 1,
            },
            {
                "name": "test_net1",
                "sensor_prefix": "tst1",
                "api_port": 80,
                "api_location": "/",
                "cron": "* * * * * *",
                "first_ip": "10.0.0.1",
                "last_ip": "10.0.0.254",
                "ip_count": 254,
            },
            {
                "name": "test_net2",
                "sensor_prefix": "tst2",
                "api_port": 80,
                "api_location": "/",
                "cron": "* * * * * *",
                "first_ip": "10.0.1.1",
                "last_ip": "10.0.1.10",
                "ip_count": 10,
            },
        ]
        [self.assertNetwork(n, **e) for n, e in zip(config.network_setup, net_conf)]

    def test_invalid_configuration(self):
        """Test multiple configuration issues, configuration issues should be logged and a
        ConfigurationError should be raised."""
        cfg_list = ("invalid.yaml", "invalid_cron.yaml")

        for cfg in cfg_list:
            self.assertRaises(
                sensor_net.errors.ConfigError,
                sensor_net.config.get_configuration,
                os.path.join(self.config_path, cfg),
            )

    def test_invalid_driver(self):
        """Test driver is invalid. Should log the issue and raise MissingDriverError."""
        self.assertRaises(
            sensor_net.errors.MissingDriverError,
            sensor_net.config.get_configuration,
            os.path.join(self.config_path, "miss_driver.yaml"),
        )

    def test_invalid_driver_configuration(self):
        """
        Test driver configuration is invalid. Should log the issue and raise
        BackendConfigurationError.

        This tests sets the backend driver to raise exceptions.
        """
        self.backend_driver.config_error = True

        self.assertRaises(
            sensor_net.errors.BackendConfigError,
            sensor_net.config.get_configuration,
            os.path.join(self.config_path, "valid.yaml")
        )


if __name__ == '__main__':
    unittest.main()
