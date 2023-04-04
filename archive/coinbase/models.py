from dataclasses import dataclass
from enum import Enum

from archive.coinbase.note import CoinbaseNote


class CoinbaseColumns(Enum):
    """Enumeration representing columns in a Coinbase CSV dataset."""

    TIMESTAMP = 0
    TRANSACTION_TYPE = 1
    ASSET = 2
    QUANTITY = 3
    CURRENCY = 4
    SPOT_PRICE = 5
    SUBTOTAL = 6
    TOTAL = 7
    FEES = 8
    NOTES = 9


@dataclass
class CoinbaseTransaction:
    """A dataclass representing a Coinbase transaction."""

    timestamp: str
    transaction_type: str
    asset: str
    quantity: str
    currency: str
    spot_price: str
    subtotal: str
    total: str
    fees: str
    notes: CoinbaseNote

    @property
    def currency_pair(self) -> str:
        """Return the asset and currency pair in a string format of 'base-quote'"""
        return f"{self.asset}-{self.currency}"

    def should_skip(self, excluded_types: list[str]) -> bool:
        return (
            self.notes.should_skip(excluded_types)
            or self.transaction_type in excluded_types
        )

    def should_keep(self, included_assets: list[str]) -> bool:
        return (
            self.notes.should_keep(included_assets)
            or self.asset in included_assets
            or self.currency_pair in included_assets
        )
