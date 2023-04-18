from abc import ABC, abstractmethod

from archive.average.models import AverageRecord


class Broker(ABC):
    @abstractmethod
    def order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> AverageRecord:
        raise NotImplementedError()


class Coinbase(Broker):
    def order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> AverageRecord:
        raise NotImplementedError()


class Kraken(Broker):
    def order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> AverageRecord:
        raise NotImplementedError()


def broker_factory(exchange: str) -> Broker:
    if exchange == "coinbase":
        return Coinbase()
    elif exchange == "kraken":
        return Kraken()
    else:
        raise ValueError(f"Invalid exchange type: {exchange}")
