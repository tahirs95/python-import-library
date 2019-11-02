import unittest

from Store.DataStoreModule import DataStore
from testing.postgresql import Postgresql
from sqlalchemy import create_engine, inspect


class TestDataStoreInitialise(unittest.TestCase):
    def test_sqlite_initialise(self):
        """Test whether schemas created successfully on SQLite"""
        data_store_sqlite = DataStore("", "", "", 0, ":memory:", db_type="sqlite")

        # inspector makes it possible to load lists of schema, table, column
        # information for the sqlalchemy engine
        inspector = inspect(data_store_sqlite.engine)
        table_names = inspector.get_table_names()

        # there must be no table at the beginning
        self.assertEqual(len(table_names), 0)

        # creating database from schema
        data_store_sqlite.initialise()

        inspector = inspect(data_store_sqlite.engine)
        table_names = inspector.get_table_names()

        # 11 tables must be created. A few of them tested
        self.assertEqual(len(table_names), 11)
        self.assertIn("Entry", table_names)
        self.assertIn("Platforms", table_names)
        self.assertIn("State", table_names)
        self.assertIn("Datafiles", table_names)
        self.assertIn("Nationalities", table_names)

    def test_postgres_initialise(self):
        """Test whether schemas created successfully on PostgresSQL"""
        data_store_postgres = DataStore(
            "postgres", "postgres", "localhost", "5432", "postgres"
        )

        # inspector makes it possible to load lists of schema, table, column
        # information for the sqlalchemy engine
        inspector = inspect(data_store_postgres.engine)
        table_names = inspector.get_table_names()
        schema_names = inspector.get_schema_names()

        # there must be no table, and no schema for datastore at the beginning
        self.assertEqual(len(table_names), 0)
        self.assertNotIn("datastore_schema", schema_names)

        # creating database from schema
        data_store_postgres.initialise()

        inspector = inspect(data_store_postgres.engine)
        table_names = inspector.get_table_names()
        schema_names = inspector.get_schema_names()

        # 11 tables must be created. A few of them tested
        self.assertEqual(len(table_names), 11)
        self.assertIn("Entry", table_names)
        self.assertIn("Platforms", table_names)
        self.assertIn("State", table_names)
        self.assertIn("Datafiles", table_names)
        self.assertIn("Nationalities", table_names)

        # datastore_schema must be created
        self.assertIn("datastore_schema", schema_names)
