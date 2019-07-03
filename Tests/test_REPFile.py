import os, sys
import unittest

from Formats.REPFile import REPFile, REPLine

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
        self.assertEqual("SUBJECT", repline.getTimestamp())
        self.assertEqual("SUBJECT", repline.getPlatform())
        self.assertEqual("SUBJECT", repline.getSymbology())
        self.assertEqual("SUBJECT", repline.getLatitude())
        self.assertEqual("SUBJECT", repline.getLongitude())
        self.assertEqual("SUBJECT", repline.getHeading())
        self.assertEqual("SUBJECT", repline.getSpeed())
        self.assertEqual("SUBJECT", repline.getDepth())
        self.assertEqual("SUBJECT", repline.getTextLabel())

if __name__ == "__main__":
    unittest.main()
