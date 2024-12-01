class APIError(Exception):
    """
    Exception raised when an API request fails.
    """
    def __init__(self, message):
        super().__init__(f"APIError: {message}")