# Virgin Atlantic API Python Package

This Python package provides an interface to fetch data from the Virgin Atlantic API. It supports retrieving **flight prices** with various filters such as travel class, sorting options, and pagination. The package handles GraphQL queries to fetch and parse the flight data for user-friendly usage.

⚠️ **Disclaimer:** This package is not affiliated with Virgin Atlantic.

---

## Features

- Fetch the **flight prices** for a specific route.
- **Optional origin and destination** for broader searches.
- Filter flights by **travel class**:
  - Economy
  - Premium
  - Upper Class
- Sort results by:
  - Popularity
  - Departure Date (Earliest to Latest)
  - Departure Date (Latest to Earliest)
  - Price (Low to High)
  - Price (High to Low)
- Handle pagination to fetch more results.

---

## Installation

This package will soon be available on [PyPI](https://pypi.org/project/virginatlantic/). You can install it directly using pip:

```bash
pip install virginatlantic
```

Or clone the repository and install it locally:

```bash
git clone https://github.com/alexechoi/virgin-atlantic-py.git
cd virgin-atlantic-py
pip install .
```

---

## Usage

### Initialize the Client

To use the package, initialize the `VirginAtlantic` client:

```python
from virginatlantic.api import VirginAtlantic

# Initialize the client
client = VirginAtlantic()
```

---

### Fetch Flight Prices

#### **Basic Example**
Retrieve flight prices for a specific route and travel class:

```python
flights = client.get_flight_prices(
    origin="LHR",  # London Heathrow
    destination="JFK",  # New York JFK
    travel_class="ECONOMY",  # Travel class
    sorting="PRICE_ASC",  # Sort by price (low to high)
    page_number=1,  # First page
    limit=10  # Number of results per page
)

# Display results
for flight in flights:
    print(
        f"From {flight['origin']} to {flight['destination']}: "
        f"{flight['price']} ({flight['departure_date']} to {flight['return_date']}, {flight['travel_class']})"
    )
```

#### **Output**
```
From London to New York: $450 (2024-12-15 to 2024-12-22, Economy)
From London to New York: $470 (2024-12-16 to 2024-12-23, Economy)
```

---

### Optional Parameters

You can omit the `origin` or `destination` to fetch all flights departing from or arriving at any location:

```python
# Flights from any origin to JFK
flights = client.get_flight_prices(destination="JFK", travel_class="PREMIUM")
```

---

### Advanced Sorting

Sort results using any of the following options:
- **`POPULAR`**: By popularity.
- **`DEPARTURE_DATE_ASC`**: Departure date (earliest to latest).
- **`DEPARTURE_DATE_DESC`**: Departure date (latest to earliest).
- **`PRICE_ASC`**: Price (low to high).
- **`PRICE_DESC`**: Price (high to low).

```python
# Sort by departure date (latest to earliest)
flights = client.get_flight_prices(
    origin="LHR", destination="JFK", travel_class="UPPER CLASS", sorting="DEPARTURE_DATE_DESC"
)
```

---

## Error Handling

The package raises appropriate errors for invalid inputs:

- **Invalid Travel Class**: Raises a `ValueError` if the travel class is not `ECONOMY`, `PREMIUM`, or `UPPER CLASS`.
- **Invalid Sorting Option**: Raises a `ValueError` for unrecognized sorting methods.
- **API Errors**: Raises an `APIError` for network or server-side issues.

Example:
```python
try:
    flights = client.get_flight_prices("LHR", "JFK", "INVALID_CLASS")
except ValueError as e:
    print(f"Error: {e}")
```

---

## Contributing

Contributions are welcome! If you encounter bugs or have suggestions for new features, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License.

---

### Example Code

Here's a full example for quick reference:

```python
from virginatlantic.api import VirginAtlantic

def main():
    # Initialize the client
    client = VirginAtlantic()

    # Fetch flight prices
    flights = client.get_flight_prices(
        origin="LHR",  # London Heathrow
        destination="JFK",  # New York JFK
        travel_class="ECONOMY",  # Travel class
        sorting="PRICE_ASC",  # Sort by price (low to high)
        page_number=1,  # First page
        limit=5  # Fetch 5 results
    )

    # Print the flight details
    print("Available flights:")
    for flight in flights:
        print(
            f"From {flight['origin']} to {flight['destination']}: "
            f"{flight['price']} ({flight['departure_date']} to {flight['return_date']}, {flight['travel_class']})"
        )

if __name__ == "__main__":
    main()
```

---

### Happy Coding! 😊 - Created by [Alex Choi](https://github.com/alexechoi)