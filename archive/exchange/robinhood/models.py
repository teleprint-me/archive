from dataclasses import dataclass
from enum import Enum


class RobinhoodColumns(Enum):
    """Enumeration representing columns in a Robinhood 1099 CSV dataset."""

    ASSET_NAME = 0
    RECEIVED_DATE = 1
    COST_BASIS = 2
    DATE_SOLD = 3
    PROCEEDS = 4


@dataclass
class RobinhoodTransaction:
    """A dataclass representing a Robinhood 1099 transaction."""

    asset_name: str
    received_date: str
    cost_basis: float
    date_sold: str
    proceeds: float

    @property
    def exchange(self) -> str:
        return "robinhood"

    @property
    def asset(self) -> str:
        return self.asset_name

    def should_keep(self, included_assets: list[str]) -> bool:
        return self.asset_name in included_assets
