from dataclasses import dataclass
from enum import Enum


class F8949Columns(Enum):
    """Enumeration representing columns in a Form-8949 CSV dataset."""

    DESCRIPTION_OF_PROPERTY = 0
    DATE_ACQUIRED = 1
    DATE_SOLD = 2
    PROCEEDS = 3
    COST_OR_OTHER_BASIS = 4
    CODES = 5
    AMOUNT_OF_ADJUSTMENT = 6
    GAIN_OR_LOSS = 7


@dataclass
class F8949Transaction:
    """A dataclass representing a Form-8949 transaction."""

    description_of_property: str
    date_acquired: str
    date_sold: str
    proceeds: float
    cost_or_other_basis: float
    codes: str = str()
    amount_of_adjustment: float = float()
    gain_or_loss: float = float()
