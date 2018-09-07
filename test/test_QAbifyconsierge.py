# QAbifyconsierge_tests.py
# by Sam Heyman

import unittest
import QAbifyConsierge

class TaxiCommands(unittest.TestCase):
    def test_taxi_order(self):
        order = QAbifyConsierge.contains_taxi("hey! I need a ride!")
        expected = True
        self.assertEqual(expected, order)


# Run the tests
if __name__ == "main":
    unittest.main()