from dataclasses import dataclass
from enum import Enum


class IRColumns(Enum):
    """Enumerated columns for intermediary representation."""

    EXCHANGE = 0
    PRODUCT = 1
    DATETIME = 2
    TRANSACTION_TYPE = 3
    ORDER_SIZE = 4
    MARKET_PRICE = 5
    ORDER_FEE = 6
    ORDER_NOTE = 7


@dataclass(frozen=True)
class IRTransaction:
    """A dataclass representing the datasets intermediary representation.

    Attributes:
        exchange (str): The cryptocurrency exchange.
        product (str): The asset involved in the transaction.
        datetime (str): The timestamp of the transaction.
        transaction_type (str): The type of transaction.
        order_size (str): The quantity of the asset involved in the transaction.
        market_price (str): The spot price of the asset at the time of the transaction.
        order_fee (str): The fee charged for the transaction.
        order_note (str): The note associated with the transaction.
    """

    exchange: str
    product: str
    datetime: str
    transaction_type: str
    order_size: float
    market_price: float
    order_fee: float = 0.0
    order_note: str = str()
