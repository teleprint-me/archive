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
    @abstractmethod
    def post_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> dict[str, Union[str, float]]:
        raise NotImplementedError()

    @abstractmethod
    def get_price(self, product_id: str) -> float:
        raise NotImplementedError()

    @abstractmethod
    def get_simulated_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> dict[str, Union[str, float]]:
        raise NotImplementedError()


class Coinbase(Broker):
    def post_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> dict[str, Any]:
        return coinbase_market_order(quote_size, product_id, side)

    def get_price(self, product_id: str) -> float:
        return coinbase_spot_price(product_id)

    def get_simulated_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> dict[str, Union[str, float]]:
        return coinbase_simulated_market_order(quote_size, product_id, side)


class Kraken(Broker):
    def post_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> dict[str, Union[str, float]]:
        raise NotImplementedError()

    def get_price(self, product_id: str) -> float:
        return kraken_spot_price(product_id)

    def get_simulated_order(
        self, market_price: float
    ) -> dict[str, Union[str, float]]:
        raise NotImplementedError()


def broker_factory(exchange: str) -> Broker:
    if exchange == "coinbase":
        return Coinbase()
    elif exchange == "kraken":
        return Kraken()
    else:
        raise ValueError(f"Invalid exchange type: {exchange}")
