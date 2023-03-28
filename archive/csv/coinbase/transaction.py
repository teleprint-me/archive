from dataclasses import dataclass
from enum import Enum

from archive.csv.coinbase.note import CoinbaseNote


class CoinbaseColumns(Enum):
    """An enumeration representing the different columns in a Coinbase transaction CSV."""

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
    """A dataclass representing a Coinbase transaction.

    Attributes:
        timestamp (str): The timestamp of the transaction.
        transaction_type (str): The type of transaction.
        asset (str): The asset involved in the transaction.
        quantity (str): The quantity of the asset involved in the transaction.
        currency (str): The currency used in the transaction.
        spot_price (str): The spot price of the asset at the time of the transaction.
        subtotal (str): The subtotal of the transaction.
        total (str): The total amount of the transaction.
        fee (str): The fee charged for the transaction.
        notes (CoinbaseNote): The note associated with the transaction.
    """

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
