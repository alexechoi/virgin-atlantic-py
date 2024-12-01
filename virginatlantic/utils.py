def build_payload(origin, destination, travel_class, sorting, page_number, limit):
    """
    Build the payload for the Virgin Atlantic API request.

    Args:
        origin (str): Origin airport code (e.g., "LHR"). Leave blank for no filter.
        destination (str): Destination airport code (e.g., "JFK"). Leave blank for no filter.
        travel_class (str): Travel class (ECONOMY, PREMIUM, UPPER CLASS).
        sorting (str): Sorting method (e.g., "POPULAR", "DEPARTURE_DATE_ASC").
        page_number (int): Page number for pagination.
        limit (int): Number of results per page.

    Returns:
        list: Payload as a list containing the request structure.
    """
    # Convert travel_class and sorting to strings
    travel_class = str(travel_class).upper()
    sorting = str(sorting).upper()

    if travel_class not in ["ECONOMY", "PREMIUM", "UPPER CLASS"]:
        raise ValueError("Invalid travel class. Must be 'ECONOMY', 'PREMIUM', or 'UPPER CLASS'.")

    sorting_options = {
        "POPULAR": "POPULARITY",
        "DEPARTURE_DATE_ASC": "DEPARTURE_DATE_ASC",
        "DEPARTURE_DATE_DESC": "DEPARTURE_DATE_DESC",
        "PRICE_ASC": "PRICE_ASC",
        "PRICE_DESC": "PRICE_DESC"
    }
    if sorting not in sorting_options:
        raise ValueError(
            "Invalid sorting option. Must be one of: 'POPULAR', 'DEPARTURE_DATE_ASC', "
            "'DEPARTURE_DATE_DESC', 'PRICE_ASC', 'PRICE_DESC'."
        )

    # Handle origin and destination as optional
    origin_filter = {"code": origin} if origin else {}
    destination_filter = {"code": destination} if destination else {}

    return [
        {
            "variables": {
                "page": {
                    "tenant": "vs",
                    "slug": "flights-from-london",
                    "siteEdition": "en-gb"
                },
                "id": "62867e5799abbc76cc15c63f",
                "pageNumber": page_number,
                "limit": limit,
                "flatContext": {
                    "siteEditionCountryGeoId": "2635167",
                    "templateId": "5e286e2ac2fb8cd7020058c5",
                    "templateName": "from-city"
                },
                "filters": {
                    "origin": origin_filter,
                    "destination": destination_filter,
                    "travelClass": travel_class,
                    "sorting": sorting_options[sorting]
                },
                "urlParameters": {},
                "nearestOriginAirport": {}
            },
            "query": """query ($page: PageInput!, $id: String!, $pageNumber: Int, $limit: Int, $flatContext: FlatContextInput, $urlParameters: StandardFareModuleUrlParameters, $filters: StandardFareModuleFiltersInput, $nearestOriginAirport: AirportInput) {
                standardFareModule(page: $page, id: $id, pageNumber: $pageNumber, limit: $limit, flatContext: $flatContext, urlParameters: $urlParameters, filters: $filters, nearestOriginAirport: $nearestOriginAirport) {
                    fares {
                        originCity
                        destinationCity
                        formattedTotalPrice
                        formattedDepartureDate
                        formattedReturnDate
                        formattedTravelClass
                    }
                }
            }"""
        }
    ]

def parse_response(response_data):
    """
    Parse the API response into a user-friendly format.

    Args:
        response_data (dict): The raw JSON response from the API.

    Returns:
        list: A list of dictionaries containing flight details.
    """
    # Extract the first item if the response is a list
    if isinstance(response_data, list):
        response_data = response_data[0]

    standard_fare_module = response_data.get("data", {}).get("standardFareModule", {})
    fares = standard_fare_module.get("fares", [])

    return [
        {
            "origin": fare.get("originCity"),
            "destination": fare.get("destinationCity"),
            "price": fare.get("formattedTotalPrice"),
            "departure_date": fare.get("formattedDepartureDate"),
            "return_date": fare.get("formattedReturnDate"),
            "travel_class": fare.get("formattedTravelClass"),
        }
        for fare in fares
    ]