from pathlib import Path

from archive.exchange.robinhood.models import (
    RobinhoodColumns,
    RobinhoodTransaction,
)
from archive.tools.io import read_csv


def get_robinhood_transaction(csv_row: list[str]) -> RobinhoodTransaction:
    return RobinhoodTransaction(
        asset_name=csv_row[RobinhoodColumns.ASSET_NAME.value],
        received_date=csv_row[RobinhoodColumns.RECEIVED_DATE.value],
        cost_basis=float(csv_row[RobinhoodColumns.COST_BASIS.value]),
        date_sold=csv_row[RobinhoodColumns.DATE_SOLD.value],
        proceeds=float(csv_row[RobinhoodColumns.PROCEEDS.value]),
    )


def get_robinhood_csv_row(
    transaction: RobinhoodTransaction,
) -> list[str]:
    return [
        transaction.asset_name,
        transaction.received_date,
        str(transaction.cost_basis),
        transaction.date_sold,
        str(transaction.proceeds),
    ]


def build_robinhood_csv_table(
    transactions: list[RobinhoodTransaction],
) -> list[list[str]]:
    # Include header in conversion process
    csv_header = [
        [
            "ASSET NAME",
            "RECEIVED DATE",
            "COST BASIS(USD)",
            "DATE SOLD",
            "PROCEEDS",
        ]
    ]
    csv_table = []
    for row in transactions:
        transaction = get_robinhood_csv_row(row)
        csv_table.append(transaction)
    return csv_header + csv_table


def build_robinhood_transactions(
    csv_table: list[list[str]],
) -> list[RobinhoodTransaction]:
    # Exclude header from conversion process
    transactions = []
    for csv_row in csv_table[1:]:
        transaction = get_robinhood_transaction(csv_row)
        transactions.append(transaction)
    return transactions


def scan_robinhood(
    filepath: str | Path,
) -> list[RobinhoodTransaction]:
    csv_table = read_csv(filepath)
    return build_robinhood_transactions(csv_table)
