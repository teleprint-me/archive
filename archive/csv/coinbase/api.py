import time
from typing import Optional

import requests


def get_spot_price(currency_pair: str, datetime: Optional[str] = None) -> dict:
    """Perform a GET request to the coinbase API path for spot prices.

    Args:
        currency_pair: The base and quote currency pair, e.g. "BTC-USD"
        datetime: (optional) For historic spot price, use format YYYY-MM-DD (UTC)

    Returns:
        The response of the GET request as a dictionary
    """
    # The rate limit of the API requests, in seconds.
    # This is calculated as 1 / (10000 requests per hour / 3600 seconds per hour)
    # The rate limit is used to block a request for at least 0.36 seconds.
    time.sleep(1 / (10000 / 3600))
    url = f"https://api.coinbase.com/v2/prices/{currency_pair}/spot"
    if datetime:
        return requests.get(url, params={"date": datetime}, timeout=30).json()
    return requests.get(url, timeout=30).json()
