"""Test SQLAlchemy backend."""
import datetime
import decimal
import logging
import unittest

import src.sensor_net
import src.sensor_net.backend_driver.sqlalchemy
import src.sensor_net.backend_driver.sqlalchemy.schema


class TestSQLAlchemyBackendWorking(unittest.TestCase):
    """Tests SQLAlchemy backend."""
    def setUp(self) -> None:
        """
        Prepare the test case.

        -> Create a SQLite database
        -> Create tables
        -> Create SQLLite backend configuration
        -> Retrieve SQLAlchemy backend connected to SQLLite
        """
        logging.basicConfig(level=logging.DEBUG)

        self.driver = src.sensor_net.backend_driver.sqlalchemy.get_driver(
            "test_daemon",
            {"url": "sqlite:///:memory:"},
        )

        self.schema = src.sensor_net.backend_driver.sqlalchemy.schema.Schema()
        self.schema.setup(self.driver.engine)

    def test_write_success(self):
        """Test write to SQLAlchemy. Data should be written to the database."""
        self.driver.write(
            network_name="test_net",
            network_prefix="tst",
            sensor_address="0.0.0.0",
            data=[src.sensor_net.SensorData(
                "heartbeat",
                123,
                datetime.datetime(2022, 1, 2, 3, 4, 5)  # 2022-01-02, 03:04:05
            )],
        )

        with self.driver.engine.connect() as conn:
            results = conn.execute(self.driver.table.select()).all()
            self.assertEqual(len(results), 1, "There should be only one result.")
            self.assertEqual(
                results[0][:-1],  # Remove d_created_utc to avoid patching datetime.utcnow
                (
                    "test_daemon",
                    "tst0.0.0.0",
                    "test_net",
                    "heartbeat",
                    datetime.datetime(2022, 1, 2, 3, 4, 5),
                    decimal.Decimal(123.0),
                ),
                "Data are not as expected."
            )


class TestSQLAlchemyBackendIssues(unittest.TestCase):
    """Test with incomplete Database setup."""

    def setUp(self) -> None:
        """Backend driver."""
        self.driver = src.sensor_net.backend_driver.sqlalchemy.get_driver(
            "failed_tests",
            {"url": "sqlite:///:memory:"},
        )

    def test_write_failed(self):
        """Test write error accessing to SQLAlchemy. Should raise a BackendWriteError."""
        self.assertRaises(
            src.sensor_net.backend_driver.sqlalchemy.BackendWriteError,
            self.driver.write,
            network_name="test_net",
            network_prefix="tst",
            sensor_address="0.0.0.0",
            data=[src.sensor_net.SensorData(
                "heartbeat",
                123.456,
                datetime.datetime(2022, 1, 2, 3, 4, 5)  # 2022-01-02, 03:04:05
            )],
        )


if __name__ == '__main__':
    unittest.main()
