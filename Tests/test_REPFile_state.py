import os, sys
import unittest
import datetime

from Formats.REPFile import REPFile
from Formats.State import State
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

    ####################
    #### line tests ####
    ####################

    def test_lineOk(self):
        state = State(1, "100112 120800 SUBJECT VC 60 23 40.25 N 000 01 25.86 E 109.08  6.00  0.00 ")
        state.parse()

        self.assertEqual(1, state.getLineNum())
        self.assertEqual("SUBJECT", state.getTimestamp())
        self.assertEqual("SUBJECT", state.getPlatform())
        self.assertEqual("SUBJECT", state.getSymbology())
        self.assertEqual("SUBJECT", state.getLatitude())
        self.assertEqual("SUBJECT", state.getLongitude())
        self.assertEqual("SUBJECT", state.getHeading())
        self.assertEqual("SUBJECT", state.getSpeed())
        self.assertEqual("SUBJECT", state.getDepth())
        self.assertEqual("SUBJECT", state.getTextLabel())


    def test_stateConversion(self):
        state = State(1, "100112 120800 SUBJECT VC 60 23 40.25 N 000 01 25.86 E 109.08  6.00  0.00 ")
        state.parse()

        # Speed and Heading from state
        # heading -> 109.08 (degrees)
        # speed   -> 6.00 (knots)

        # state.parse will call the appropriate setters for speed and headings
        # Asserting converted values from getters

        self.assertEqual(1.9038051480754146, state.getHeading())
        self.assertEqual(3.086666666666667, state.getSpeed())
        




if __name__ == "__main__":
    unittest.main()
