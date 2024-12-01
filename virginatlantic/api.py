import logging
import requests
from .config import BASE_URL, HEADERS
from .utils import build_payload, parse_response
from .exceptions import APIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VirginAtlantic:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS

    def get_flight_prices(
        self,
        origin="",
        destination="",
        travel_class="ECONOMY",
        sorting="POPULAR",
        page_number=1,
        limit=20
    ):
        """
        Fetch flight prices from Virgin Atlantic API.

        Args:
            origin (str): Origin airport code (optional).
            destination (str): Destination airport code (optional).
            travel_class (str): Travel class (ECONOMY, PREMIUM, UPPER CLASS). Default is "ECONOMY".
            sorting (str): Sorting method (POPULAR, DEPARTURE_DATE_ASC, PRICE_ASC, etc.). Default is "POPULAR".
            page_number (int): Pagination number. Default is 1.
            limit (int): Number of results per page. Default is 20.

        Returns:
            list: Parsed flight price data.
        """
        payload = build_payload(origin, destination, travel_class, sorting, page_number, limit)

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Network error: {e}")

        if response.status_code != 200:
            raise APIError(f"API returned an error: {response.status_code} - {response.text}")

        result = parse_response(response.json())
        if not result and destination:
            logger.warning(f"No results returned. Ensure '{destination}' is a valid Virgin Atlantic destination.")

        return result