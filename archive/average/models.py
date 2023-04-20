from dataclasses import dataclass
from enum import Enum


class AverageColumn(Enum):
    """Enumerated columns for averaging strategies records."""

    EXCHANGE = 0
    PRODUCT_ID = 1
    PRINCIPAL_AMOUNT = 2
    SIDE = 3
    DATETIME = 4
    MARKET_PRICE = 5
    CURRENT_TARGET = 6
    CURRENT_VALUE = 7
    ORDER_SIZE = 8
    TOTAL_ORDER_SIZE = 9
    INTERVAL = 10


class CostAverageColumn(Enum):
    """Enumerated columns for cost averaging strategy records."""

    EXCHANGE = 0
    PRODUCT_ID = 1
    PRINCIPAL_AMOUNT = 2
    SIDE = 3
    DATETIME = 4
    MARKET_PRICE = 5
    CURRENT_TARGET = 6
    CURRENT_VALUE = 7
    ORDER_SIZE = 8
    TOTAL_ORDER_SIZE = 9
    INTERVAL = 10
    GAIN_OR_LOSS = 11


@dataclass
class AverageRecord:
    """A dataclass representing a base record for averaging strategies."""

    exchange: str
    product_id: str
    principal_amount: float
    side: str
    datetime: str
    market_price: float
    current_target: float
    current_value: float
    order_size: float
    total_order_size: float
    interval: int = 0

    @property
    def base(self) -> str:
        return self.product_id.split("-")[0]

    @property
    def quote(self) -> str:
        return self.product_id.split("-")[1]


@dataclass
class CostAverageRecord(AverageRecord):
    gain_or_loss: float = 0


@dataclass
class DynamicAverageRecord(AverageRecord):
    factor: float = 0
    factor_amount: float = 0
    total_factor_amount: float = 0


@dataclass
class ValueAverageRecord(AverageRecord):
    interest_rate: float = 0
    trade_amount: float = 0
    total_trade_amount: float = 0
