from dataclasses import dataclass
from enum import Enum


class CoinbaseNoteColumn(Enum):
    """Enumeration representing properties in a CoinbaseNote."""

    VERB = 0
    SIZE = 1
    BASE = 2
    PREPOSITION = 3
    DETERMINER = 4
    QUOTE = 5
    PRODUCT = 6
    TRANSACTION_TYPE = 7


class CoinbaseColumn(Enum):
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
class CoinbaseNote:
    """Class representing a Coinbase transaction note.

    A Coinbase transaction note is a short description of a transaction that provides information about the type of transaction and the currencies involved.
    """

    verb: str = ""
    size: str = ""
    base: str = ""
    preposition: str = ""
    determiner: str = ""
    quote: str = ""
    product: str = ""
    transaction_type: str = ""

    @property
    def currency_pair(self) -> str:
        """Return the base and quote currency as a string in the format 'base-quote'"""
        if self.base and self.quote:
            return f"{self.base}-{self.quote}"
        return self.base

    def should_skip(self, excluded_types: list[str]) -> bool:
        """Return True if the note should be skipped based on the specified transaction types, else False"""
        match_exception = "an external account" == self.determiner
        match_type = self.transaction_type in excluded_types
        return bool(match_exception or match_type)

    def should_keep(self, included_assets: list[str]) -> bool:
        """Return True if the note should be kept based on the specified products, else False"""
        has_product = self.product in included_assets
        has_quote = self.quote in included_assets
        has_currency_pair = self.currency_pair in included_assets
        return bool(has_product or has_quote or has_currency_pair)


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
