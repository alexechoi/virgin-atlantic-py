import unittest
from virginatlantic.api import VirginAtlantic

class TestVirginAtlanticAPI(unittest.TestCase):
    def setUp(self):
        self.api = VirginAtlantic()

    def test_get_flight_prices(self):
        # Mocked API response
        result = self.api.get_flight_prices("LHR", "JFK", "ECONOMY")
        self.assertIsInstance(result, list)
        for flight in result:
            self.assertIn("origin", flight)
            self.assertIn("destination", flight)
            self.assertIn("price", flight)