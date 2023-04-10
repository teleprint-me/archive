from dataclasses import dataclass
from enum import Enum

# Define a mapping between exchange product names and a standard naming convention
products = {
    # Stable Coins
    "USDCUSD": "USDC-USD",
    "DAIUSD": "DAI-USD",
    # USD Trade Pairs
    "XXBTZUSD": "BTC-USD",
    "XETHZUSD": "ETH-USD",
    "XLTCZUSD": "LTC-USD",
    "XXMRZUSD": "XMR-USD",
    "XZECZUSD": "ZEC-USD",
    "DOTUSD": "DOT-USD",
    "LINKUSD": "LINK-USD",
    "COMPUSD": "COMP-USD",
    "UNIUSD": "UNI-USD",
    "YFIUSD": "YFI-USD",
    "XXRPZUSD": "XRP-USD",
    # BTC Trade Pairs
    "XETHXXBT": "ETH-BTC",
    "XLTCXXBT": "LTC-BTC",
    "XXMRXXBT": "XMR-BTC",
    # Add more mappings as needed
}


class KrakenColumns(Enum):
    """Enumeration representing columns in a Kraken CSV dataset."""

    TXID = 0
    ORDER_TXID = 1
    PAIR = 2
    TIME = 3
    TYPE = 4
    ORDER_TYPE = 5
    PRICE = 6
    COST = 7
    FEE = 8
    VOL = 9
    MARGIN = 10
    MISC = 11
    LEDGERS = 12
    NOTES = 13


@dataclass
class KrakenTransaction:
    """A dataclass representing a Kraken transaction."""

    txid: str
    order_txid: str
    pair: str
    time: str
    type: str
    order_type: str
    price: float
    cost: float
    fee: float
    vol: float
    margin: float
    misc: str
    ledgers: str
    notes: str = str()

    @property
    def product(self) -> str:
        """
        Returns the standardized product name from Kraken's non-standardized product name.
        If the product name is not found in the `products` dictionary, it raises a KeyError.
        """
        try:
            return products[self.pair]
        except KeyError:
            raise KeyError(
                f"Unknown Kraken product: '{self.pair}'. Please add it to the 'products' dictionary in 'archive/exchange/kraken/models.py'."
            )

    @property
    def base(self) -> str:
        """
        Returns the base asset symbol of the transaction's product.
        Raises a KeyError if the product name is not in the expected standardized format.
        """
        try:
            return self.product.split("-")[0]
        except IndexError:
            raise KeyError(
                f"Unexpected Kraken product format: '{self.product}'. Please check the 'products' dictionary in 'archive/exchange/kraken/models.py'."
            )

    @property
    def quote(self) -> str:
        """
        Returns the quote asset symbol of the transaction's product.
        Raises a KeyError if the product name is not in the expected standardized format.
        """
        try:
            return self.product.split("-")[1]
        except IndexError:
            raise KeyError(
                f"Unexpected Kraken product format: '{self.product}'. Please check the 'products' dictionary in 'archive/exchange/kraken/models.py'."
            )

    @property
    def fiat(self) -> list[str]:
        """
        Returns a list of fiat currencies.
        """
        return [
            "USD",
            "GBP",
            "EUR",
            "CAD",
            "JPY",
            "CHF",
            "AUD",
            "NZD",
        ]

    @property
    def stablecoins(self) -> list[str]:
        """
        Returns a list of stablecoins.
        """
        return [
            "USDT",
            "USDC",
            "DAI",
            "PAX",
            "BUSD",
            "HUSD",
            "TUSD",
        ]

    @property
    def is_fiat(self) -> bool:
        """
        Returns True if the quote asset of the transaction's product is a fiat currency.
        """
        return self.quote in self.fiat

    @property
    def is_stablecoin(self) -> bool:
        """
        Returns True if the quote asset of the transaction's product is a stablecoin.
        """
        return self.quote in self.stablecoins

    def should_keep(self, included_assets: list[str]) -> bool:
        """
        Returns True if the transaction involves any of the specified assets.
        """
        return (
            self.base in included_assets
            or self.quote in included_assets
            or self.product in included_assets
        )
