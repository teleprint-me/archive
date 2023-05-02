# archive/ir/models.py
from dataclasses import dataclass
from enum import Enum

from peewee import CharField, FloatField, Model, SqliteDatabase

# Define the database connection
db = SqliteDatabase("transactions.db")


class IRTransactionModel(Model):
    exchange = CharField()
    product = CharField()
    datetime = CharField()
    transaction_type = CharField()
    order_size = FloatField()
    market_price = FloatField()
    order_fee = FloatField(default=0.0)
    order_note = CharField(default="")

    class Meta:
        database = db
        indexes = (
            (
                (
                    "exchange",
                    "product",
                    "datetime",
                    "transaction_type",
                    "order_size",
                    "market_price",
                    "order_fee",
                    "order_note",
                ),
                True,
            ),
        )


class IRColumn(Enum):
    """Enumerated columns for intermediary representation."""

    EXCHANGE = 0
    PRODUCT = 1
    DATETIME = 2
    TRANSACTION_TYPE = 3
    ORDER_SIZE = 4
    MARKET_PRICE = 5
    ORDER_FEE = 6
    ORDER_NOTE = 7


@dataclass
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

    @property
    def is_buy(self) -> bool:
        return self.transaction_type == "Buy"

    @property
    def is_sell(self) -> bool:
        return self.transaction_type == "Sell"
