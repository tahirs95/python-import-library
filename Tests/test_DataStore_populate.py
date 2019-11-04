import unittest
import os

from unittest import TestCase
from Store.DataStoreModule import DataStore

FILE_PATH = os.path.dirname(__file__)
TEST_DATA_PATH = os.path.join(FILE_PATH, "sample_data")


class TestDataStorePopulate(TestCase):
    def setUp(self):
        self.sqlite = DataStore("", "", "", 0, ":memory:", db_type="sqlite")
        self.sqlite.initialise()

    def tearDown(self):
        pass

    def test_populate_reference(self):
        """Test whether CSVs successfully imported to SQLite"""

        # Check tables are created but empty
        with self.sqlite.session_scope() as session:
            nationalities = self.sqlite.getNationalities()
            platform_types = self.sqlite.getPlatformTypes()

        # There must be no entities at the beginning
        self.assertEqual(len(nationalities), 0)
        self.assertEqual(len(platform_types), 0)

        # Import CSVs to the related tables
        with self.sqlite.session_scope() as session:
            self.sqlite.populateReference(TEST_DATA_PATH)

        # Check tables filled with correct data
        with self.sqlite.session_scope() as session:
            nationalities = self.sqlite.getNationalities()
            platform_types = self.sqlite.getPlatformTypes()
            nationality_object = self.sqlite.searchNationality("UNITED KINGDOM")
            platform_type_object = self.sqlite.searchPlatformType("TYPE-1")

            # Check whether they are not empty anymore and filled with correct data
            self.assertNotEqual(len(nationalities), 0)
            self.assertNotEqual(len(platform_types), 0)

            self.assertIn(nationality_object.name, "UNITED KINGDOM")
            self.assertIn(platform_type_object.name, "TTYPE-1")


if __name__ == "__main__":
    unittest.main()
