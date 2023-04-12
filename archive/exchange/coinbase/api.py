import time
from typing import Optional

import requests
from requests import RequestException


def get_spot_price(
    currency_pair: str,
    datetime: Optional[str] = None,
) -> float:
    """Perform a GET request to the coinbase API path for spot prices.

    Args:
        currency_pair: The base and quote currency pair, e.g. "BTC-USD"
        datetime: (optional) For historic spot price, use format YYYY-MM-DD (UTC)

    Returns:
        The response of the GET request as a float representing the spot price

    Raises:
        RequestException: If there's an issue with the response or if the response is missing data
    """

    # The rate limit of the API requests, in seconds.
    # This is calculated as 1 / (10000 requests per hour / 3600 seconds per hour)
    # The rate limit is used to block a request for at least 0.36 seconds.
    time.sleep(1 / (10000 / 3600))

    url = f"https://api.coinbase.com/v2/prices/{currency_pair}/spot"

    try:
        if datetime:
            response = requests.get(
                url, params={"date": datetime}, timeout=30
            ).json()
        else:
            response = requests.get(url, timeout=30).json()

        if "data" in response and "amount" in response["data"]:
            return float(response["data"]["amount"])
        elif "errors" in response and "message" in response["errors"]:
            raise RequestException(response["errors"]["message"])
        elif "error" in response and "error_description" in response["error"]:
            raise RequestException(response["error"]["error_description"])
        else:
            raise RequestException("Invalid response from the API")

    except RequestException as e:
        raise RequestException(f"Error retrieving spot price: {e}")
