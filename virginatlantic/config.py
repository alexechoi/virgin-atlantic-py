# config.py

# Base URL for Virgin Atlantic API
BASE_URL = "https://vg-api.airtrfx.com/graphql"

# Headers for the API request
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-GB,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://flights.virginatlantic.com",
    "referer": "https://flights.virginatlantic.com/en-gb/flights-from-london?cta=VA_NHP_LHRFLIGHTS",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}