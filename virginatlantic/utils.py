def build_payload(origin, destination, travel_class, page_number, limit):
    """
    Build the payload for the Virgin Atlantic API request.

    Args:
        origin (str): Origin airport code (e.g., "LHR").
        destination (str): Destination airport code (e.g., "JFK").
        travel_class (str): Travel class (e.g., "ECONOMY", "PREMIUM", "BUSINESS").
        page_number (int): Page number for pagination.
        limit (int): Number of results per page.

    Returns:
        list: Payload as a list containing the request structure.
    """
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
                    "templateName": "from-city",
                    "originLocationLevel": "City",
                    "originGeoId": "2643743",
                    "OriginAirportName": origin,
                    "OriginCityName": "London",
                    "OriginStateName": "England",
                    "OriginCountryName": "United Kingdom",
                    "toOriginCountryName": "the United Kingdom"
                },
                "filters": {
                    "origin": {"code": origin, "geoId": "-111413"},
                    "travelClass": travel_class,
                    "sorting": "DEPARTURE_DATE_ASC"
                },
                "urlParameters": {},
                "nearestOriginAirport": {}
            },
            "query": """query ($page: PageInput!, $id: String!, $pageNumber: Int, $limit: Int, $flatContext: FlatContextInput, $urlParameters: StandardFareModuleUrlParameters, $filters: StandardFareModuleFiltersInput, $nearestOriginAirport: AirportInput) {
                standardFareModule(page: $page, id: $id, pageNumber: $pageNumber, limit: $limit, flatContext: $flatContext, urlParameters: $urlParameters, filters: $filters, nearestOriginAirport: $nearestOriginAirport) {
                    id
                    metaData {
                        name
                        title
                        subtitle
                        footer
                        viewType
                        __typename
                    }
                    visualizationSettings {
                        includeImages
                        includeCta
                        numberOfColumns
                        textAlignment
                        showJourneyType
                        showTravelClass
                        showFareTimestamp
                        showDates
                        carouselVisualizationType
                        ctaButtonStyle
                        __typename
                    }
                    filterSettings {
                        visualization
                        showOriginFilter
                        showDestinationFilter
                        showBudgetFilter
                        showTravelClassFilter
                        showBrandedTravelClassFilter
                        locationAttributesFilters
                        validateOriginsCountryMarket
                        currencyCode
                        restrictOriginFilter
                        restrictDestinationFilter
                        showRedemptionUnitFilter
                        showNumberOfStopsFilter
                        showJourneyTypeFilter
                        showSortingFilter
                        __typename
                    }
                    sortingFilterValues
                    fares(pageNumber: $pageNumber, limit: $limit, urlParameters: $urlParameters, nearestOriginAirport: $nearestOriginAirport) {
                        originCity
                        destinationCity
                        formattedTotalPrice
                        formattedDepartureDate
                        formattedReturnDate
                        formattedTravelClass
                    }
                    error
                    __typename
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
    print(f"Response data: {response_data}")

    # Extract the first item if the response is a list
    if isinstance(response_data, list):
        response_data = response_data[0]

    # Navigate to the 'fares' key in the response
    standard_fare_module = response_data.get("data", {}).get("standardFareModule", {})
    fares = standard_fare_module.get("fares", [])

    # Parse each fare and return a clean list
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