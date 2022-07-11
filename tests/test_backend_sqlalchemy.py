"""Test SQLAlchemy backend."""
import unittest


class TestSQLAlchemyBackend(unittest.TestCase):
    """Tests SQLAlchemy backend."""
    def test_write_success(self):
        """Test write to SQLAlchemy. Data should be written to the database."""
        raise NotImplementedError("SQLAlchemy backend is not implemented.")

    def test_write_failed(self):
        """Test write error accessing to SQLAlchemy. Should raise a BackendWriteError."""
        raise NotImplementedError("SQLAlchemy backend is not implemented.")


if __name__ == '__main__':
    unittest.main()
