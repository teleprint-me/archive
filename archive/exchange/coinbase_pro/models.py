from dataclasses import dataclass
from enum import Enum


class CoinbaseProColumns(Enum):
    """Enumeration representing columns in a Coinbase Pro CSV dataset."""

    PORTFOLIO = 0
    TRADE_ID = 1
    PRODUCT = 2
    SIDE = 3
    CREATED_AT = 4
    SIZE = 5
    SIZE_UNIT = 6  # represents the base product
    PRICE = 7
    FEE = 8
    TOTAL = 9
    TOTAL_UNIT = 10  # represents the quote product
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
