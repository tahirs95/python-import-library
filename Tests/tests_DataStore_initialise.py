import unittest

from Store.DataStoreModule import DataStore
from testing.postgresql import Postgresql
from sqlalchemy import create_engine, inspect


class TestDataStoreInitialise(unittest.TestCase):
    # def setUp(self):
    #     self.postgres = Postgresql(port=5432)
    #
    # def tearDown(self):
    #     self.postgres.stop()

    def test_sqlite_initialise(self):
        """Test whether schemas created successfully on SQLite"""
        data_store_sqlite = DataStore("", "", "", 0, ":memory:", db_type="sqlite")
        inspector = inspect(data_store_sqlite.engine)
        table_names = inspector.get_table_names()
        self.assertEqual(len(table_names), 0)

        data_store_sqlite.initialise()
        inspector = inspect(data_store_sqlite.engine)
        table_names = inspector.get_table_names()
        self.assertEqual(len(table_names), 11)
        self.assertIn("Entry", table_names)
        self.assertIn("Platforms", table_names)
        self.assertIn("State", table_names)
        self.assertIn("Datafiles", table_names)
        self.assertIn("Nationalities", table_names)

    def test_postgres_initialise(self):
        # TODO: not working yet
        """Test whether schemas created successfully on PostgresSQL"""
        data_store_postgres = DataStore(
            "postgres", "postgres", "localhost", "5432", "postgres"
        )
        query = ("select schema_name", "from information_schema.schemata;")
        engine = create_engine(self.postgres.url())
        with engine.raw_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            schemas_before = cursor.fetchall()

        self.assertNotIn("datastore_schema", schemas_before)

        data_store_postgres.initialise()
        with engine.raw_connection() as conn:
            cursor = conn.cursor
            cursor.execute(query)
            schemas_after = cursor.fetchall()

        self.assertEqual(schemas_before + 1, schemas_after)
        self.assertIn("datastore_schema", schemas_after)
