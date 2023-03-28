from dataclasses import dataclass
from enum import Enum


class CoinbaseNoteColumns(Enum):
    VERB = 0
    SIZE = 1
    BASE = 2
    PREPOSITION = 3
    DETERMINER = 4
    QUOTE = 5
    PRODUCT = 6
    TRANSACTION_TYPE = 7


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
