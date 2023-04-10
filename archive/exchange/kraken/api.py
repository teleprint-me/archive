import time

import requests
from dateutil.parser import parse
from requests import RequestException


def get_asset_info(currency_pair: str) -> tuple[str, str]:
    """Retrieve the base and quote products for a given currency pair.

    Args:
        currency_pair: The currency pair to retrieve asset info for.

    Returns:
        A tuple containing the base and quote products as strings.
    """
    url = "https://api.kraken.com/0/public/AssetPairs"
    params = {"pair": currency_pair}
    response = requests.get(url, params=params)
    result = response.json()["result"][currency_pair]

    if len(currency_pair) == 6 or len(currency_pair) == 7:
        base_product = f"{result['base']}USD"
        quote_product = f"{result['quote']}USD"
    else:
        base_product = f"{result['base']}ZUSD"
        quote_product = f"{result['quote']}ZUSD"

    return base_product, quote_product


def get_spot_price(currency_pair: str, datetime: str) -> float:
    """Retrieve the spot price for a currency pair at a specific datetime.

    Args:
        currency_pair: The currency pair to retrieve the spot price for.
        datetime: The UTC datetime string to retrieve the spot price for, in the format "%Y-%m-%dT%H:%M:%SZ".

    Returns:
        The spot price for the currency pair and datetime as a float.

    Raises:
        RequestException: If there's an issue with the response or if the response is missing data.
    """
    # The rate limit of the API requests, in seconds.
    # The rate limit is used to block a request for at least 1.00 second.
    time.sleep(1)

    # Calculate the timestamp of the datetime string
    timestamp = int(parse(datetime).timestamp())

    # Set the time range for the Trades endpoint query
    time_range = f"{timestamp-60}:{timestamp+60}"

    # Send a GET request to the Trades endpoint with the specified parameters
    url = "https://api.kraken.com/0/public/Trades"
    params = {"pair": currency_pair, "since": time_range}
    response = requests.get(url, params=params)

    try:
        # Extract the trades data from the response and find the trade that
        # occurred closest to the specified datetime
        trades = response.json()["result"][currency_pair]
        closest_trade = min(trades, key=lambda x: abs(int(x[2]) - timestamp))

        # Extract the price information from the closest trade and return it as a float
        return float(closest_trade[0])

    except KeyError as e:
        raise RequestException(f"Error retrieving spot price: {e}")
