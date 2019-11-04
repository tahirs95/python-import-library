import os, sys
import unittest
import datetime
import math

from pint import UnitRegistry

from Formats.REPFile import REPFile
from Formats.State import State
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
    #### tests ####
    ####################


    def test_roundTripDegs(self):

        uReg = UnitRegistry()
        Quantity = uReg.Quantity

        headingDegs = Quantity(180.0, uReg.degrees)

        self.assertEqual("<Quantity(180.0, 'degree')>", repr(headingDegs))

        headingRads = headingDegs.to(uReg.radians)

        self.assertEqual("<Quantity(3.141592653589793, 'radian')>", repr(headingRads))

        backToDegs = headingRads.to(uReg.degrees)
        self.assertEqual("<Quantity(180.0, 'degree')>", repr(backToDegs))

    def test_roundTripSpeed(self):
        uReg = UnitRegistry()
        Quantity = uReg.Quantity

        speedKts = Quantity(20, uReg.knot)

        self.assertEqual("<Quantity(20, 'knot')>", repr(speedKts))

        speedMs = speedKts.to(uReg.meter / uReg.second)

        self.assertEqual("<Quantity(10.28888888888889, 'meter / second')>", repr(speedMs))

        backToKts = speedMs.to(uReg.knot)
        self.assertEqual("<Quantity(20.000000000000004, 'knot')>", repr(backToKts))
        self.assertAlmostEqual(20, backToKts.magnitude)


    def test_stateConversion(self):
        state = State(1, "100112 120800 SUBJECT VC 60 23 40.25 N 000 01 25.86 E 109.08  6.00  0.00 ")
        state.parse()

        # Speed and Heading from state
        # heading -> 109.08 (degrees)
        # speed   -> 6.00 (knots)

        # use `almost-equal`
        print("speed in test:", repr(state.getSpeed()))
        print("heading in text", repr(state.getHeading()))
        self.assertEqual("<Quantity(109.08, 'degree')>", repr(state.getHeading()))
        self.assertEqual("<Quantity(6.0, 'knot')>", repr(state.getSpeed()))
        

if __name__ == "__main__":
    unittest.main()
