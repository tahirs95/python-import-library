import os, sys
import unittest
import datetime

from Formats.REPFile import REPFile, REPLine
from Formats.Location import Location

class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    def setUp(self):
        pass

    def tearDown(self):
        pass

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
