# tests.py
# by Sam Heyman

import unittest
import qabify_bot
from utilities import get_distance

class TestTaxiCommands(unittest.TestCase):
    def test_taxi_order_valid(self):
        order = qabify_bot.contains_taxi("hey! I need a ride!")
        expected = True
        self.assertEqual(expected, order, "The command failed to be acknowledged as a taxi request")

    def test_taxi_order_not_valid(self):
        order = qabify_bot.contains_taxi("hey! I am lost!")
        expected = False
        self.assertEqual(expected, order, "The command failed to be acknowledged as a taxi request")

    def test_get_distance_crow_flies(self):
        pointA = (-3.568, 40.498)
        pointB = (-3.704, 40.417)
        expected = 14.6
        result = get_distance(pointA, pointB, 'crow_flies')
        difference = result - expected
        self.assertLessEqual(difference,0.2)

    def test_get_distance_driving(self):
        pointA = (40.461165, -3.568)
        pointB = (40.417, -3.704)
        expected = 17.9
        result = get_distance(pointA, pointB, 'driving')
        difference = result - expected
        self.assertLessEqual(difference,0.2)

    def test_can_reserve_taxi(self):
        pass

    def test_can_return_all_taxis(self):
        pass

    
# Run the tests
if __name__ == "__main__":
    unittest.main()