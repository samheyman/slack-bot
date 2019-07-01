# tests.py
# by Sam Heyman

import unittest
# from utilities import get_distance
from context import taxi_bot, utilities

class TestTaxiCommands(unittest.TestCase):

    def test_get_distance_crow_flies(self):
        pointA = (-3.568, 40.498)
        pointB = (-3.704, 40.417)
        expected = 14.6
        result = utilities.get_distance(pointA, pointB, 'crow_flies')
        difference = result - expected
        self.assertLessEqual(difference,0.2)

    def test_get_distance_driving(self):
        pointA = (40.461165, -3.568)
        pointB = (40.417, -3.704)
        expected = 17.9
        result = utilities.get_distance(pointA, pointB, 'driving')
        difference = result - expected
        self.assertLessEqual(difference,0.2)

    def test_can_reserve_taxi(self):
        pass

    def test_can_return_all_taxis(self):
        pass

    
# Run the tests
if __name__ == "__main__":
    unittest.main()