from dataclasses import dataclass
from enum import Enum


class CoinbaseProAccountColumn(Enum):
    """Enumeration representing columns in a Coinbase Pro Account CSV dataset."""

    PORTFOLIO = 0
    TYPE = 1
    TIME = 2
    AMOUNT = 3
    BALANCE = 4
    UNIT = 5  # represents given asset, e.g. BTC
    TRANSFER_ID = 6
    TRADE_ID = 7
    ORDER_ID = 8


class CoinbaseProFillColumn(Enum):
    """Enumeration representing columns in a Coinbase Pro Fills CSV dataset."""

    PORTFOLIO = 0
    TRADE_ID = 1
    PRODUCT = 2
    SIDE = 3
    CREATED_AT = 4
    SIZE = 5
    SIZE_UNIT = 6  # represents base product, e.g. BTC
    PRICE = 7
    FEE = 8
    TOTAL = 9
    TOTAL_UNIT = 10  # represents quote product, e.g. USD
    NOTES = 11


@dataclass
class CoinbaseProTransaction:
    """A dataclass representing a Coinbase Pro transaction."""

    portfolio: str
    trade_id: int
    product: str
    side: str
    created_at: str
    size: float
    size_unit: str
    price: float
    fee: float
    total: float
    total_unit: str
    notes: str = str()

    @property
    def base(self) -> str:
        return self.size_unit

    @property
    def quote(self) -> str:
        return self.total_unit

    @property
    def fiat(self) -> list[str]:
        return [
            "USD",
            "GBP",
            "EUR",
        ]

    @property
    def stablecoins(self) -> list[str]:
        return [
            "USDC",
            "USDT",
            "DAI",
            "TUSD",
        ]

    @property
    def is_fiat(self) -> bool:
        return self.quote in self.fiat

    @property
    def is_stablecoin(self) -> bool:
        return self.quote in self.stablecoins

    def should_keep(self, included_assets: list[str]) -> bool:
        return (
            self.base in included_assets
            or self.quote in included_assets
            or self.product in included_assets
        )
