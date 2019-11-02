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

        self.postgres = Postgresql(port=5432)

    def tearDown(self):
        self.postgres.stop()

    def test_sqlite_initialise(self):
        """Test whether schemas created successfully on SQLite"""
        pass

    def test_postgres_initialise(self):
        # TODO: not tested yet because of pip3 library issues
        """Test whether schemas created successfully on PostgresSQL"""
        query = (
            "select schema_name",
            "from information_schema.schemata;"
        )
        engine = create_engine(self.postgres.url())
        with engine.raw_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            schemas_before = cursor.fetchall()

        self.assertNotIn("datastore_schema", schemas_before)

        self.data_store_postgres.initialise()
        with engine.raw_connection() as conn:
            cursor = conn.cursor
            cursor.execute(query)
            schemas_after = cursor.fetchall()

        self.assertEqual(schemas_before+1, schemas_after)
        self.assertIn("datastore_schema", schemas_after)

