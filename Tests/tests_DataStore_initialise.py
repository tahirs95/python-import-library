import unittest

from Store.DataStoreModule import DataStore
from testing.postgresql import Postgresql
from sqlalchemy import create_engine


class TestDataStoreInitialise(unittest.TestCase):

    def setUp(self):
        self.data_store_sqlite = DataStore("", "", "", 0, ":memory:",
                                      db_type="sqlite")
        self.data_store_postgres = DataStore("postgres", "postgres", "localhost",
                                        "5432", "postgres")

        # self.postgres = Postgresql(port=5432)

    # def tearDown(self):
    #     self.postgres.stop()

    def test_sqlite_initialise(self):
        """Test whether schemas created successfully on SQLite"""
        pass

    def test_postgres_initialise(self):
        """Test whether schemas created successfully on PostgresSQL"""

        # engine = create_engine(self.postgres.url())
        pass
