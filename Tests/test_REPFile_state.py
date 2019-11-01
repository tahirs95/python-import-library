import os, sys
import unittest
import datetime

from Formats.REPFile import REPFile, REPLine
from Formats.Location import Location

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
TEST_FILE = os.path.join(dir_path, "reptest1.rep")
ERROR_TEST_FILE = os.path.join(dir_path, "reptest2.rep")

class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    def setUp(self):
        pass

    def tearDown(self):
        pass

    ####################
    #### file tests ####
    ####################

    def test_fileNotFound_excep(self):
        excep_thrown = False
        try:
            REPFile("nonexistant.rep")
        except IOError:
            excep_thrown = True

        self.assertTrue(excep_thrown)

    def test_getFileType(self):
        repfile = REPFile(TEST_FILE)
        self.assertEqual("REP", repfile.getDatafileType())

    def test_getFileName(self):
        repfile = REPFile(TEST_FILE)
        self.assertEqual(TEST_FILE, repfile.getDatafileName())

    def test_getAllLines(self):
        repfile = REPFile(TEST_FILE)
        self.assertEqual(8, len(repfile.getLines()))

    def test_FileTypes(self):
        repfile = REPFile(TEST_FILE)
        self.assertEqual("REP", repfile.getDatafileType())
        self.assertEqual(TEST_FILE, repfile.getDatafileName())


    def test_fileParseError(self):
        excep_thrown = False
        try:
            REPFile(ERROR_TEST_FILE)
        except Exception:
            excep_thrown = True

        self.assertTrue(excep_thrown)
   
if __name__ == "__main__":
    unittest.main()
