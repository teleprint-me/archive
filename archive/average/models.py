from dataclasses import dataclass
from enum import Enum


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


class DynamicAverageColumn(Enum):
    """Enumerated columns for dynamic averaging strategy records."""

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
    MULTIPLIER = 11
    TRADE_AMOUNT = 12
    TOTAL_TRADE_AMOUNT = 13


class ValueAverageColumn(Enum):
    """Enumerated columns for value averaging strategy records."""

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
    GROWTH_RATE = 11
    TRADE_AMOUNT = 12
    TOTAL_TRADE_AMOUNT = 13


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


@dataclass
class CostAverageRecord(AverageRecord):
    """A dataclass representing a cost averaging record."""

    gain_or_loss: float = 0


@dataclass
class DynamicAverageRecord(AverageRecord):
    """A dataclass representing a dynamic averaging record."""

    multiplier: float = 0
    trade_amount: float = 0
    total_trade_amount: float = 0


@dataclass
class ValueAverageRecord(AverageRecord):
    """A dataclass representing a value averaging record."""

    growth_rate: float = 0
    trade_amount: float = 0
    total_trade_amount: float = 0
