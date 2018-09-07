# QAbifyconsierge_tests.py
# by Sam Heyman

import unittest
import QAbifyConsierge

class TestTaxiCommands(unittest.TestCase):
    def test_taxi_order_valid(self):
        order = QAbifyConsierge.contains_taxi("hey! I need a ride!")
        expected = True
        self.assertEqual(expected, order, "The command failed to be acknowledged as a taxi request")

    def test_taxi_order_not_valid(self):
        order = QAbifyConsierge.contains_taxi("hey! I need to go somewhere!")
        expected = False
        self.assertEqual(expected, order, "The command failed to be acknowledged as a taxi request")


# Run the tests
if __name__ == "__main__":
    unittest.main()