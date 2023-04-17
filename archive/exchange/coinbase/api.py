import hashlib
import hmac
import time
from datetime import datetime
from os import getenv
from typing import Any, Optional

# NOTE: Always generate uuid4 for privacy!
from uuid import uuid4

import requests
from dotenv import load_dotenv
from requests import RequestException
from requests.auth import AuthBase
from requests.models import PreparedRequest

load_dotenv()

# Name of agent making requests.
__agent__: str = "teleprint-me/archive"

# Source code: Link to GitHub repository.
__source__: str = f"https://github.com/{__agent__}"

# Source version.
__version__: str = "0.1.6"

# Rate limit of API requests in seconds.
# Calculated as 1 / (10000 requests per hour / 3600 seconds per hour)
# Rate limit used to block request for at least 0.36 seconds.
__limit__: float = 1 / (10000 / 3600)

# Timeout value for HTTP requests.
__timeout__: int = 30

# Sign In lets Coinbase users easily and securely sign in to your product or service,
# and lets you integrate Coinbase supported cryptocurrencies into your applications.
__coinbase__: str = "https://api.coinbase.com/v2"

# Coinbase Advanced Trade replaces and improves upon Coinbase Pro.
# Advanced Trade API supports programmatic trading and order management with a REST API
# and WebSocket protocol for real-time market data.
__advanced__: str = "https://api.coinbase.com/api/v3/brokerage"


class Auth(AuthBase):
    """Create and return an HTTP request with authentication headers.

    Args
        api: Instance of the API class, if not provided, a default instance is created.
    """

    def __init__(self):
        """Create an instance of the Auth class.

        Args:
            api: Instance of the API class, if not provided, a default instance is created.
        """

        self.key: Optional[str] = getenv("API_KEY") or ""
        self.secret: Optional[str] = getenv("API_SECRET") or ""

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        """Return the prepared request with updated headers.

        Args:
            request: A prepared HTTP request.

        Returns:
            The same request with updated headers.
        """

        # Create payload.
        timestamp: str = str(int(time.time()))
        body: str = "" if not request.body else request.body.decode("utf-8")
        method: str = "" if not request.method else request.method.upper()
        message: str = f"{timestamp}{method}{request.path_url}{body}"

        # Create signature.
        key = self.secret.encode("ascii")
        msg = message.encode("ascii")
        signature = hmac.new(key, msg, hashlib.sha256).hexdigest()

        # Sign and authenticate payload.
        header: dict = {
            "User-Agent": f"{__agent__}/{__version__} {__source__}",
            "CB-ACCESS-KEY": self.key,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "CB-VERSION": "2021-08-03",
            "Content-Type": "application/json",
        }

        # Inject payload
        request.headers.update(header)

        return request


__auth__ = Auth()


def get(url: str, data: Optional[dict] = None) -> dict[str, Any]:
    """Perform a GET request to the specified API path.

    Args:
        path: The API endpoint to be requested.
        data: (optional) Query parameters to be passed with the request.

    Returns:
        The response of the GET request.
    """

    time.sleep(__limit__)

    try:
        response = requests.get(
            url=url,
            params=data,
            auth=__auth__,
            timeout=__timeout__,
        ).json()

        if "errors" in response and "message" in response["errors"]:
            raise RequestException(response["errors"]["message"])
        elif "error" in response and "error_description" in response["error"]:
            raise RequestException(response["error"]["error_description"])
        elif "error" in response and "message" in response["error"]:
            raise RequestException(response["error"]["message"])
        else:
            return response

    except RequestException as error:
        raise RequestException(f"Error retrieving GET request: {error}")


def post(url: str, data: Optional[dict] = None) -> dict[str, Any]:
    """Perform a POST request to the specified API path.

    Args:
        path: The API endpoint to be requested.
        data: (optional) JSON payload to be sent with the request.

    Returns: The response of the POST request.
    """

    time.sleep(__limit__)

    try:
        response = requests.post(
            url=url,
            json=data,
            auth=__auth__,
            timeout=__timeout__,
        )

        if "errors" in response and "message" in response["errors"]:
            raise RequestException(response["errors"]["message"])
        elif "error" in response and "error_description" in response["error"]:
            raise RequestException(response["error"]["error_description"])
        elif "error" in response and "message" in response["error"]:
            raise RequestException(response["error"]["message"])
        else:
            return response

    except RequestException as error:
        raise RequestException(f"Error retrieving POST request: {error}")


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

    url = f"{__coinbase__}/prices/{currency_pair}/spot"

    try:
        if datetime:
            response = get(url, data={"date": datetime})
        else:
            response = get(url)

        if "data" in response and "amount" in response["data"]:
            return float(response["data"]["amount"])
        else:
            raise RequestException("Invalid response from the API")

    except RequestException as error:
        raise RequestException(f"Error retrieving spot price: {error}")


def post_market_order(
    quote_size: float,
    product_id: str,
    side: str = "BUY",
) -> dict[str, Any]:
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

    try:
        market_order = {
            "client_order_id": str(uuid4()),
            "product_id": product_id,
            "side": side,
            "order_configuration": {
                "market_market_ioc": {"quote_size": str(quote_size)}
            },
        }

        response = post("/orders", data=market_order)

        if "success" in response and response["success"]:
            success_response = response["success_response"]
            market_response = response["order_configuration"][
                "market_market_ioc"
            ]

            return {
                "exchange": "coinbase",
                "datetime": datetime.now().isoformat(),
                "order_id": response["order_id"],
                "product_id": success_response["product_id"],
                "side": success_response["side"],
                "base_size": market_response["base_size"],
                "quote_size": market_response["quote_size"],
            }

        else:
            raise RequestException(response["error_response"]["message"])

    except RequestException as error:
        raise RequestException(f"Error posting market order: {error}")
