import unittest
from unittest.mock import patch
from virginatlantic.api import VirginAtlantic
from virginatlantic.exceptions import APIError


class TestVirginAtlanticAPI(unittest.TestCase):
    def setUp(self):
        self.api = VirginAtlantic()

    @patch("virginatlantic.api.requests.post")
    def test_get_flight_prices_success(self, mock_post):
        # Mock a successful API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": {
                "standardFareModule": {
                    "fares": [
                        {
                            "originCity": "London",
                            "destinationCity": "New York",
                            "formattedTotalPrice": "$450",
                            "formattedDepartureDate": "2024-12-15",
                            "formattedReturnDate": "2024-12-22",
                            "formattedTravelClass": "Economy"
                        }
                    ]
                }
            }
        }

        result = self.api.get_flight_prices("LHR", "JFK", "ECONOMY", "POPULAR", 1, 10)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        # Check the structure of each flight
        for flight in result:
            self.assertIn("origin", flight)
            self.assertIn("destination", flight)
            self.assertIn("price", flight)
            self.assertIn("departure_date", flight)
            self.assertIn("return_date", flight)
            self.assertIn("travel_class", flight)

    @patch("virginatlantic.api.requests.post")
    def test_get_flight_prices_invalid_class(self, mock_post):
        # Expect a ValueError for an invalid travel class
        with self.assertRaises(ValueError) as context:
            self.api.get_flight_prices("LHR", "JFK", "INVALID_CLASS", "POPULAR", 1, 10)
        self.assertEqual(str(context.exception), "Invalid travel class. Must be 'ECONOMY', 'PREMIUM', or 'UPPER CLASS'.")

    @patch("virginatlantic.api.requests.post")
    def test_get_flight_prices_invalid_sorting(self, mock_post):
        # Expect a ValueError for an invalid sorting option
        with self.assertRaises(ValueError) as context:
            self.api.get_flight_prices("LHR", "JFK", "ECONOMY", "INVALID_SORTING", 1, 10)
        self.assertEqual(
            str(context.exception),
            "Invalid sorting option. Must be one of: 'POPULAR', 'DEPARTURE_DATE_ASC', "
            "'DEPARTURE_DATE_DESC', 'PRICE_ASC', 'PRICE_DESC'."
        )

    @patch("virginatlantic.api.requests.post")
    def test_get_flight_prices_api_error(self, mock_post):
        # Mock an API error response
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = {"error": "Internal Server Error"}

        with self.assertRaises(APIError) as context:
            self.api.get_flight_prices("LHR", "JFK", "ECONOMY", "POPULAR", 1, 10)
        self.assertIn("API returned an error", str(context.exception))

    @patch("virginatlantic.api.requests.post")
    def test_get_flight_prices_no_results_warning(self, mock_post):
        # Mock a response with no results
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": {
                "standardFareModule": {
                    "fares": []
                }
            }
        }

        with self.assertLogs(level="WARNING") as log:
            result = self.api.get_flight_prices("LHR", "XYZ", "ECONOMY", "POPULAR", 1, 10)
        self.assertEqual(result, [])
        self.assertIn("No results returned. Ensure 'XYZ' is a valid Virgin Atlantic destination.", log.output[0])

    @patch("virginatlantic.api.requests.post")
    def test_get_flight_prices_optional_origin_destination(self, mock_post):
        # Mock a successful response with no origin or destination
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": {
                "standardFareModule": {
                    "fares": [
                        {
                            "originCity": "London",
                            "destinationCity": "New York",
                            "formattedTotalPrice": "$450",
                            "formattedDepartureDate": "2024-12-15",
                            "formattedReturnDate": "2024-12-22",
                            "formattedTravelClass": "Economy"
                        }
                    ]
                }
            }
        }

        result = self.api.get_flight_prices("", "", "ECONOMY", "POPULAR", 1, 10)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        flight = result[0]
        self.assertEqual(flight["origin"], "London")
        self.assertEqual(flight["destination"], "New York")
        self.assertEqual(flight["price"], "$450")