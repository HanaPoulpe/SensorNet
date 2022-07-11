"""Tests that cron polling configuration works properly."""
import unittest


class TestCron(unittest.TestCase):
    """Tests cron response."""
    def test_cron_poll(self):
        """Tests that cron is polling correctly."""
        raise NotImplementedError("Cron is not implemented.")

    def test_cron_no_poll(self):
        """Tests that cron is not polling when polling should be skipped."""
        raise NotImplementedError("Cron is not implemented.")


if __name__ == '__main__':
    unittest.main()
