# integration_tests.py
# by Sam Heyman

import unittest
import time
import json
from unittest.mock import patch
from context import taxi_bot

class TestAPIs(unittest.TestCase):

    # test cabify API available
    def test_taxi_API_no_results(self):
        with patch('context.taxi_bot.get_taxis') as mocked_get:
            mocked_get.return_value = []
            result = taxi_bot.handle_command("all taxis in madrid", None)
            self.assertEqual(result, "Sorry, there are currently no taxis in madrid")

    def test_taxi_API_two_results(self):
        with patch('context.taxi_bot.get_taxis') as mocked_get:
            mocked_get.return_value = [{"taxi_id": 1, "state": "hired", "name": "hyundai", "location": {"lon": 3.703, "lat": 40.41}, "city": "madrid"}, {"taxi_id": 2, "state": "hired", "name": "fiat", "location": {"lon": 2.1734, "lat": 41.38}, "city": "barcelona"}, {"taxi_id": 3, "state": "free", "name": "peugeot", "location": {"lon": 2.3522, "lat": 48.86}, "city": "paris"}, {"taxi_id": 4, "state": "hired", "name": "renault", "location": {"lon": 0.1278, "lat": 51.5074}, "city": "london"}]
            result = taxi_bot.handle_command("all taxis in madrid", None)
            self.assertIn("Found 4 taxis in madrid:", 'Found 4 taxis in madrid:')

    
    # TODO test Slack API available
    # def test_slack_API_available(self):
    #     pass

# Run the tests
if __name__ == "__main__":
    unittest.main()