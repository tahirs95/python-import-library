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
        repline = REPLine(1, "100112 120800 SUBJECT VC 60 23 40.25 N 000 01 25.86 E 109.08  6.00  0.00 ")
        repline.parse()

        self.assertEqual(1, repline.getLineNum())

        print(repline.getTimestamp())

        self.assertEqual(datetime.datetime(2010, 1, 12, 12, 8), repline.getTimestamp())
        self.assertEqual("SUBJECT", repline.getPlatform())
        self.assertEqual("VC", repline.getSymbology())
     #FixMe   self.assertEqual(Location(60.0, 23.0, 40.25, "N"), repline.getLatitude())
     #FixMe   self.assertEqual("SUBJECT", repline.getLongitude())
        self.assertEqual(109.08, repline.getHeading())
        self.assertEqual(6.0, repline.getSpeed())
        self.assertEqual(0.0, repline.getDepth())
        self.assertEqual(None, repline.getTextLabel())

if __name__ == "__main__":
    unittest.main()
