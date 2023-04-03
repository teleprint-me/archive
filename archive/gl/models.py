from dataclasses import dataclass
from enum import Enum


class GLColumns(Enum):
    """Enumeration representing columns in a Gains and Losses CSV dataset."""

    ADDITIONAL_DESCRIPTION = 0
    DESCRIPTION = 1
    DATE_ACQUIRED = 2
    TRANSACTION_TYPE = 3
    ORDER_SIZE = 4
    MARKET_PRICE = 5
    EXCHANGE_FEE = 6
    COST_OR_OTHER_BASIS = 7
    ACB_PER_SHARE = 8
    DATE_SOLD = 9
    SALES_PROCEEDS = 10
    GAIN_OR_LOSS = 11
    ORDER_NOTE = 12


class GLTotalColumns(Enum):
    TOTAL_ORDER_SIZE = 0
    TOTAL_COST_OR_OTHER_BASIS = 1
    TOTAL_ACB_PER_SHARE = 2
    TOTAL_GAIN_OR_LOSS = 3


@dataclass
class GLTransaction:
    """A dataclass representing a Gain or Loss transaction."""

    additional_description: str
    description: str
    date_acquired: str
    transaction_type: str
    order_size: float
    market_price: float
    exchange_fee: float
    cost_or_other_basis: float = float()
    acb_per_share: float = float()
    date_sold: str = str()
    sales_proceeds: float = float()
    gain_or_loss: float = float()
    order_note: str = str()

    @property
    def is_sell(self) -> bool:
        return self.transaction_type == "Sell"

    @property
    def is_buy(self) -> bool:
        return self.transaction_type == "Buy"


@dataclass
class GLTotalTransaction:
    order_size: float = float()
    cost_or_other_basis: float = float()
    acb_per_share: float = float()
    gain_or_loss: float = float()
