import unittest
from unittest import TestCase
from testing.postgresql import Postgresql
from Store.DataStoreModule import DataStore
from sqlalchemy import inspect


class TestDataStoreInitialisePostgres(TestCase):
    def setUp(self):
        try:
            self.postgres = Postgresql(
                database="test", host="localhost", user="postgres", port=55527
            )
        except RuntimeError as e:
            raise Exception("PostgreSQL database couldn't be created! "
                            "Test is skipping.")

    def tearDown(self):
        self.postgres.stop()

    def test_postgres_initialise(self):
        """Test whether schemas created successfully on PostgresSQL"""
        data_store_postgres = DataStore(
            db_username="postgres",
            db_password="",
            db_host="localhost",
            db_port=55527,
            db_name="test",
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


class TestDataStoreInitialiseSQLite(TestCase):
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

if __name__ == "__main__":
    unittest.main()