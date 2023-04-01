import requests
from dateutil.parser import parse


def get_asset_info(currency_pair: str) -> dict:
    """Retrieve the asset info for a given currency pair.

    Args:
        currency_pair: The currency pair to retrieve asset info for.

    Returns:
        A dictionary containing the asset info for the currency pair.
    """
    url = "https://api.kraken.com/0/public/AssetPairs"
    params = {"pair": currency_pair}
    response = requests.get(url, params=params)
    result = response.json()["result"][currency_pair]
    return result


def get_spot_price(currency_pair: str, datetime: str) -> dict:
    """Retrieve the spot price for a currency pair at a specific datetime.

    Args:
        currency_pair: The currency pair to retrieve the spot price for.
        datetime: The UTC datetime string to retrieve the spot price for, in the format "%Y-%m-%dT%H:%M:%SZ".

    Returns:
        A dictionary containing the spot price information for the currency pair and datetime.
    """

    # Calculate the timestamp of the datetime string
    timestamp = int(parse(datetime).timestamp())

    # Set the time range for the Trades endpoint query
    time_range = f"{timestamp-60}:{timestamp+60}"

    # Send a GET request to the Trades endpoint with the specified parameters
    url = "https://api.kraken.com/0/public/Trades"
    params = {"pair": currency_pair, "since": time_range}
    response = requests.get(url, params=params)

    # Extract the trades data from the response and find the trade that
    # occurred closest to the specified datetime
    trades = response.json()["result"][currency_pair]
    closest_trade = min(trades, key=lambda x: abs(int(x[2]) - timestamp))

    # Extract the price information from the closest trade and return it
    return {
        "data": {
            "amount": closest_trade[0],
            "currency": currency_pair,
        }
    }
