import hashlib
import hmac
import time
from os import getenv
from typing import Any, Optional

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
__version__: str = "0.1.5"

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

        self.key: Optional[str] = getenv("API_KEY")
        self.secret: Optional[str] = getenv("API_SECRET")

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
        raise RequestException(f"Error retrieving request: {error}")


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
        raise RequestException(f"Error retrieving request: {error}")


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

    except RequestException as e:
        raise RequestException(f"Error retrieving spot price: {e}")
