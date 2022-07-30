"""Test the polling tool execution overall."""
import logging
import os.path
import unittest

import urllib3.exceptions
import urllib3_mock

import src.sensor_net.backend_driver.stubber as stubber
import src.sensor_net.cmdline as cmdline


class TestSensorNet(unittest.TestCase):
    """Tests the data poller."""

    def setUp(self) -> None:
        """
        -> Setup logging
        -> Setup arguments values
        -> Setup API Call mocking
        """
        config_file = os.path.join(os.path.dirname(__file__), 'configuration/cmdline.yaml')
        self.argv = [
            f"--config={config_file}",
            "--debug",
        ]

        self.backend_driver = stubber.StubBackend()
        self.backend_driver.start()

        self.responses = urllib3_mock.Responses()
        self.responses.start()

    def tearDown(self) -> None:
        self.responses.stop()
        self.backend_driver.stop()

    def set_response(self, content: str | Exception, status: int = 200):
        """Defines HTTP response."""
        self.responses.add(
            "GET", "/", body=content, status=status,
            content_type="application/json",
        )

    def test_poll_no_issues(self):
        """Should send data to the backend, and log the polling to INFO log."""
        self.set_response('{"data":[{"name":"heartbeat","value":1,"epoch":1234567890}]}')

        with self.assertLogs("sensornet", logging.INFO) as log:
            status = cmdline.main(self.argv)
            self.assertIn(
                "INFO:sensornet:poll\ttest_bin\t127.0.0.1\tmetrics=1", log.output,
                "Log message not found.",
            )

        self.assertEqual(status, 0, "Command line should run successfully.")
        self.assertGreaterEqual(
            len(self.backend_driver.writes), 0,
            "Data should have been sent to the backend."
        )

    def test_http_connection_error(self):
        """Timeout should be logged in ERROR log."""
        self.set_response(urllib3.exceptions.HTTPError("Test Error"))

        with self.assertLogs("sensornet", logging.INFO) as log:
            status = cmdline.main(self.argv)
            self.assertIn(
                "ERROR:sensornet:Error reading sensor 127.0.0.1: HTTP connection error: HTTPError",
                log.output,
                "Log message not found.",
            )

        self.assertEqual(status, 0, "Command line should run successfully.")
        self.assertGreaterEqual(
            len(self.backend_driver.writes), 0,
            "Data should have been sent to the backend."
        )

    def test_poll_invalid_response(self):
        """No data are sent to the backend, ERROR message should be logged in ERROR log."""
        self.set_response('not json')

        with self.assertLogs("sensornet") as log:
            status = cmdline.main(self.argv)
            self.assertIn(
                "ERROR:sensornet:Error reading sensor 127.0.0.1: "
                "Expecting value: line 1 column 1 (char 0)",
                log.output,
                "Log message not found.",
            )

        self.assertEqual(status, 0, "Command line should run successfully.")
        self.assertGreaterEqual(
            len(self.backend_driver.writes), 0,
            "Data should have been sent to the backend."
        )


if __name__ == '__main__':
    unittest.main()
