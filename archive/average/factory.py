from abc import ABC, abstractmethod
from typing import Any, Union

from archive.exchange.coinbase.api import (
    get_simulated_market_order as coinbase_simulated_market_order,
)
from archive.exchange.coinbase.api import get_spot_price as coinbase_spot_price
from archive.exchange.coinbase.api import (
    post_market_order as coinbase_market_order,
)
from archive.exchange.kraken.api import get_spot_price as kraken_spot_price


class Broker(ABC):
    """Abstract base class representing a broker for buying and selling assets.

    Subclasses must implement the `get_price`, `get_simulated_order`, and `post_order`
    methods.
    """

    @abstractmethod
    def get_price(self, product_id: str) -> float:
        """Get the current market price of an asset.

        Args:
            product_id (str): The identifier for the asset.

        Returns:
            float: The current market price of the asset.
        """

        raise NotImplementedError()

    @abstractmethod
    def get_simulated_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> dict[str, Union[str, float]]:
        """Simulate an order for an asset.

        Args:
            quote_size (float): The size of the order.
            product_id (str): The identifier for the asset.
            side (str, optional): The side of the order (BUY or SELL). Defaults to "BUY".

        Returns:
            dict[str, Union[str, float]]: A dictionary representing the simulated order.
        """

        raise NotImplementedError()

    @abstractmethod
    def post_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> dict[str, Union[str, float]]:
        """Post an order for an asset.

        Args:
            quote_size (float): The size of the order.
            product_id (str): The identifier for the asset.
            side (str, optional): The side of the order (BUY or SELL). Defaults to "BUY".

        Returns:
            dict[str, Union[str, float]]: A dictionary representing the posted order.
        """

        raise NotImplementedError()


class Coinbase(Broker):
    """A class representing the Coinbase exchange.

    Inherits from the `Broker` abstract base class and provides implementations
    for its methods.
    """

    def get_price(self, product_id: str) -> float:
        """Get the current market price of an asset on Coinbase.

        Args:
            product_id (str): The identifier for the asset.

        Returns:
            float: The current market price of the asset.
        """

        return coinbase_spot_price(product_id)

    def get_simulated_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> dict[str, Union[str, float]]:
        """Simulate an order for an asset on Coinbase.

        Args:
            quote_size (float): The size of the order.
            product_id (str): The identifier for the asset.
            side (str, optional): The side of the order (BUY or SELL). Defaults to "BUY".

        Returns:
            dict[str, Union[str, float]]: A dictionary representing the simulated order.
        """

        return coinbase_simulated_market_order(quote_size, product_id, side)

    def post_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> dict[str, Any]:
        """Post an order for an asset on Coinbase.

        Args:
            quote_size (float): The size of the order.
            product_id (str): The identifier for the asset.
            side (str, optional): The side of the order (BUY or SELL). Defaults to "BUY".

        Returns:
            dict[str, Any]: A dictionary representing the posted order.
        """

        return coinbase_market_order(quote_size, product_id, side)


class Kraken(Broker):
    """A class representing the Kraken exchange.

    Inherits from the `Broker` abstract base class and provides implementations
    for the `get_price` method.
    """

    def get_price(self, product_id: str) -> float:
        """Get the current market price of an asset on Kraken.

        Args:
            product_id (str): The identifier for the asset.

        Returns:
            float: The current market price of the asset.
        """

        return kraken_spot_price(product_id)

    def get_simulated_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> dict[str, Union[str, float]]:
        """Simulate an order for an asset on Kraken.

        This method is not implemented and will raise a `NotImplementedError` if called.

        Args:
            quote_size (float): The size of the order.
            product_id (str): The identifier for the asset.
            side (str, optional): The side of the order (BUY or SELL). Defaults to "BUY".

        Returns:
            dict[str, Union[str, float]]: A dictionary representing the simulated order.

        Raises:
            NotImplementedError: This method is not implemented for the Kraken exchange.
        """

        raise NotImplementedError()

    def post_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> dict[str, Union[str, float]]:
        """Post an order for an asset on Kraken.

        This method is not implemented and will raise a `NotImplementedError` if called.

        Args:
            quote_size (float): The size of the order.
            product_id (str): The identifier for the asset.
            side (str, optional): The side of the order (BUY or SELL). Defaults to "BUY".

        Returns:
            dict[str, Union[str, float]]: A dictionary representing the posted order.

        Raises:
            NotImplementedError: This method is not implemented for the Kraken exchange.
        """

        raise NotImplementedError()


def broker_factory(exchange: str) -> Broker:
    """Factory function for creating instances of the `Broker` abstract base class.

    Args:
        exchange (str): The type of exchange to use ("coinbase" or "kraken").

    Returns:
        Broker: An instance of a subclass of the `Broker` abstract base class.

    Raises:
        ValueError: If an invalid exchange type is provided.
    """

    if exchange == "coinbase":
        return Coinbase()
    elif exchange == "kraken":
        return Kraken()
    else:
        raise ValueError(f"Invalid exchange type: {exchange}")
