from dataclasses import dataclass


@dataclass(frozen=True)
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
    def to_str(self) -> str:
        """Return the note as a string in the format 'verb size base preposition determiner quote'"""
        note_parts = [
            self.verb,
            self.size,
            self.base,
            self.preposition,
            self.determiner,
            self.quote,
        ]
        filtered_note_parts = filter(str, note_parts)
        return " ".join(filtered_note_parts)

    @property
    def currency_pair(self) -> str:
        """Return the base and quote currency as a string in the format 'base-quote'"""
        if self.base and self.quote:
            return f"{self.base}-{self.quote}"
        return self.base

    def should_skip(self, types: list[str]) -> bool:
        """Return True if the note should be skipped based on the specified transaction types, else False"""
        match_exception = "an external account" == self.determiner
        match_type = types and (self.transaction_type in types)
        return bool(match_exception or match_type)

    def should_keep(self, products: list[str]) -> bool:
        """Return True if the note should be kept based on the specified products, else False"""
        has_product = self.product in products
        has_quote = self.quote in products
        has_currency_pair = self.currency_pair in products
        return has_product or has_quote or has_currency_pair
