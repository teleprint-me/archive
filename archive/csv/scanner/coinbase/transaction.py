from dataclasses import dataclass
from enum import Enum

from archive.csv.scanner.coinbase import CoinbaseNote


class CoinbaseColumns(Enum):
    TIMESTAMP = 0
    TRANSACTION_TYPE = 1
    ASSET = 2
    QUANTITY = 3
    SPOT_PRICE_CURRENCY = 4
    SPOT_PRICE_AT_TRANSACTION = 5
    SUBTOTAL = 6
    TOTAL = 7
    FEES = 8
    NOTES = 9


@dataclass(frozen=True)
class CoinbaseTransaction:
    timestamp: str
    transaction_type: str
    asset: str
    quantity: str
    currency: str
    spot_price: str
    subtotal: str
    total: str
    fee: str
    notes: CoinbaseNote

    def to_list(self) -> list[str]:
        return [
            self.timestamp,
            self.transaction_type,
            self.asset,
            str(self.quantity),
            self.currency,
            str(self.spot_price),
            str(self.subtotal),
            str(self.total),
            str(self.fee),
            self.notes.to_str,
        ]
