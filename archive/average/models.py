from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AveragingColumn(Enum):
    """Enumerated columns for the averaging strategies records."""

    EXCHANGE = 0
    PRODUCT_ID = 1
    SIDE = 2
    DATETIME = 3
    MARKET_PRICE = 4
    CURRENT_TARGET = 5
    CURRENT_VALUE = 6
    ORDER_SIZE = 7
    TOTAL_ORDER_SIZE = 8
    INTERVAL = 9


@dataclass
class AveragingRecord:
    """A dataclass representing a base record for averaging strategies."""

    exchange: str
    product_id: str
    datetime: str
    principal_amount: float
    market_price: float
    side: str
    current_target: float
    current_value: float
    order_size: float
    total_order_size: float
    interval: int

    @property
    def base(self) -> str:
        return self.product_id.split("-")[0]

    @property
    def quote(self) -> str:
        return self.product_id.split("-")[1]

    def increment_interval(self) -> int:
        self.interval += 1
        return self.interval


@dataclass
class CostAveragingRecord(AveragingRecord):
    gain_loss: Optional[float]


@dataclass
class DynamicAveragingRecord(AveragingRecord):
    factor: Optional[float]
    factor_amount: Optional[float]
    total_factor_amount: Optional[float]


@dataclass
class ValueAveragingRecord(AveragingRecord):
    interest_rate: Optional[float]
    trade_amount: Optional[float]
    total_trade_amount: Optional[float]
