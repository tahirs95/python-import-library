import os, sys
import unittest
import datetime
import math

from . import ureg, Quantity

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
        headingDegs = Quantity(180.0 * ureg.degrees)

        self.assertEqual("<Quantity(180.0, 'degree')>", repr(headingDegs))

        headingRads = headingDegs.to(ureg.radians)

        self.assertEqual("<Quantity(3.141592653589793, 'radian')>", repr(headingRads))

        backToDegs = headingRads.to(ureg.degrees)
        self.assertEqual("<Quantity(180.0, 'degree')>", repr(backToDegs))

    def test_roundTripSpeed(self):
        speedKts = Quantity(20, ureg.knot)

        self.assertEqual("<Quantity(20, 'knot')>", repr(speedKts))

        speedMs = speedKts.to(ureg.meter / ureg.second)

        self.assertEqual("<Quantity(10.28888888888889, 'meter / second')>", repr(speedMs))

        backToKts = speedMs.to(ureg.knot)
        self.assertEqual("<Quantity(20.000000000000004, 'knot')>", repr(backToKts))
        self.assertAlmostEqual(20, backToKts.magnitude)


    def test_stateConversion(self):
        state = State(1, "100112 120800 SUBJECT VC 60 23 40.25 N 000 01 25.86 E 109.08  6.00  0.00 ")
        state.parse()

        # Speed and Heading from state
        # heading -> 109.08 (degrees)
        # speed   -> 6.00 (knots)

        # state.parse will call the appropriate setters for speed and headings
        # Asserting converted values from getters

        # find acceptable answer for heading
        heading_degs = 109.08
        heading_rads = math.radians(heading_degs)

        # find acceptable answer for speed
        speed_kts = 6.00
        speed_ms = speed_kts / 1.944
        # for an approximate result, divide the speed value by 1.944

        # use `almost-equal`
        self.assertAlmostEqual(heading_rads, state.getHeading(), delta=0.01)
        self.assertAlmostEqual(speed_ms, state.getSpeed(), delta=0.001)
        

if __name__ == "__main__":
    unittest.main()
