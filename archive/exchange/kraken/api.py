import time
from datetime import datetime as dt
from typing import Optional, Union

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
    # NOTE: This is specific to processing crypto-to-crypto
    # transactions and should be renamed. A stand alone function
    # should have this identifier instead to avoid confusion
    # with the REST API endpoint. Renaming this function will
    # affect other aspects of the code base and should be accounted
    # for before making any changes.
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


def get_spot_price(
    currency_pair: str,
    datetime: Optional[str] = None,
) -> float:
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

    if not datetime:
        datetime = dt.now().isoformat()

    # Calculate the timestamp of the datetime string
    timestamp = int(parse(datetime).timestamp())

    # Set the time range for the Trades endpoint query
    time_range = f"{timestamp-300}:{timestamp+300}"

    # Send a GET request to the Trades endpoint with the specified parameters
    url = "https://api.kraken.com/0/public/Trades"
    params = {"pair": currency_pair, "since": time_range}
    response = requests.get(url, params=params)

    try:
        # Extract the trades data from the response and find the trade that
        # occurred closest to the specified datetime
        trades = response.json()["result"][currency_pair]
        avg_price = sum(float(trade[0]) for trade in trades) / len(trades)
        return avg_price

    except KeyError as e:
        raise RequestException(f"Error retrieving spot price: {e}")


def post_market_order(
    quote_size: float,
    product_id: str,
    side: str = "BUY",
) -> dict[str, Union[str, float]]:
    """
    Post a market order to the Coinbase Advanced Trade API.

    Args:
        quote_size: The amount of quote currency to spend on the order (required for BUY orders).
        product_id: The product this order was created for, e.g., 'BTC-USD'.
        side: The side of the order, either 'BUY' or 'SELL'. Defaults to 'BUY'.

    Returns:
        A dictionary containing details of the created order, including order_id, product_id, side, base_size, and quote_size.

    Raises:
        RequestException: If there's an issue with the response or if the response contains an error message.
    """
    # NOTE: This should be adapted and implemented to Krakens REST API.
    # The return structure should follow the required base parameters
    # as a return value:
    # return {
    #     "order_id": order["order_id"],
    #     "exchange": "coinbase",
    #     "product_id": order["product_id"],
    #     "principal_amount": float(quote_size),
    #     "side": order["side"],
    #     "datetime": order["created_time"],
    #     "market_price": float(order["average_filled_price"]),
    #     "order_size": float(order["filled_size"]),
    #     "order_fee": float(order["total_fees"]),
    # }
    raise NotImplementedError()
