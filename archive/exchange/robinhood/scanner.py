from pathlib import Path

from archive.exchange.robinhood.models import (
    RobinhoodColumns,
    RobinhoodTransaction,
)
from archive.tools.io import read_csv


def scan_robinhood(
    filepath: str | Path,
) -> list[RobinhoodTransaction]:
    transactions = []
    csv_table = read_csv(filepath)

    # Exclude header from conversion process
    for csv_row in csv_table[1:]:
        transaction = RobinhoodTransaction(
            asset_name=csv_row[RobinhoodColumns.ASSET_NAME.value],
            received_date=csv_row[RobinhoodColumns.RECEIVED_DATE.value],
            cost_basis=float(csv_row[RobinhoodColumns.COST_BASIS.value]),
            date_sold=csv_row[RobinhoodColumns.DATE_SOLD.value],
            proceeds=float(csv_row[RobinhoodColumns.PROCEEDS.value]),
        )

        transactions.append(transaction)

    return transactions
