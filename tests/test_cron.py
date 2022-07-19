"""Tests that cron polling configuration works properly."""
import datetime
import unittest

import sensor_net.cron as cron


class TestCron(unittest.TestCase):
    """Tests cron response."""
    def test_cron_poll(self):
        """Tests that cron is polling correctly."""
        date = datetime.datetime(2022, 1, 1, 1, 1, 55)
        cron_exp = "1 * * * *"

        self.assertTrue(
            cron.is_triggered(cron_exp, date),
            "Cron should be triggered.",
        )

    def test_cron_no_poll(self):
        """Tests that cron is not polling when polling should be skipped."""
        date = datetime.datetime(2022, 1, 1, 1, 0, 55)
        cron_exp = "1 * * * *"

        self.assertFalse(
            cron.is_triggered(cron_exp, date),
            "Cron should not be triggered.",
        )


if __name__ == '__main__':
    unittest.main()
