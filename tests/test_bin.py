"""Test the polling tool execution overall."""
import unittest


class TestSensorNet(unittest.TestCase):
    """Tests the data poller."""
    def test_poll_no_issues(self):
        """Should send data to the backend, and log the polling to INFO log."""
        raise NotImplementedError("Polling is not implemented.")

    def test_poll_timeout(self):
        """No data are sent to the backend, timeout should be logged in ERROR log."""
        raise NotImplementedError("Polling is not implemented.")

    def test_poll_invalid_response(self):
        """No data are sent to the backend, ERROR message should be logged in ERROR log."""
        raise NotImplementedError("Polling is not implemented.")


if __name__ == '__main__':
    unittest.main()
