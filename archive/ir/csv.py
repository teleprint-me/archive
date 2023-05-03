from os import scandir
from pathlib import Path
from typing import List

from archive.ir.models import IRColumn, IRTransaction
from archive.tools.io import read_csv


def build_csv_ir_table(
    transactions: List[IRTransaction],
) -> List[List[str]]:
    """Convert a list of IRTransaction objects into a CSV table.

    Args:
        transactions (List[IRTransaction]): A list of IRTransaction objects.

    Returns:
        List[List[str]]: A nested list representing a CSV table.
    """
    body = []

    header = [
        [
            "Exchange",
            "Product",
            "Datetime",
            "Transaction Type",
            "Order Size",
            "Market Price",
            "Order Fee",
            "Order Note",
        ]
    ]

    for transaction in transactions:
        tx = [
            transaction.exchange,
            transaction.product,
            transaction.datetime,
            transaction.transaction_type,
            f"{float(transaction.order_size):.8f}",
            f"{float(transaction.market_price):.8f}",
            f"{float(transaction.order_fee):.8f}",
            transaction.order_note,
        ]

        body.append(tx)

    return header + body


def build_ir_transactions_from_csv(
    csv_table: List[List[str]],
) -> List[IRTransaction]:
    """Convert a CSV table into a list of IRTransaction objects.

    Args:
        csv_table (List[List[str]]): A nested list representing a CSV table.

    Returns:
        List[IRTransaction]: A list of IRTransaction objects.
    """
    transactions = []

    for row in csv_table[1:]:  # Skip the header row
        transaction = IRTransaction(
            exchange=row[IRColumn.EXCHANGE.value],
            product=row[IRColumn.PRODUCT.value],
            datetime=row[IRColumn.DATETIME.value],
            transaction_type=row[IRColumn.TRANSACTION_TYPE.value],
            order_size=float(row[IRColumn.ORDER_SIZE.value]),
            market_price=float(row[IRColumn.MARKET_PRICE.value]),
            order_fee=float(row[IRColumn.ORDER_FEE.value]),
            order_note=row[IRColumn.ORDER_NOTE.value],
        )

        transactions.append(transaction)

    return transactions


def scan_csv_ir_transactions(directory: str | Path) -> List[List[str]]:
    """Scan a directory for CSV files and combine their content into a single CSV table.

    Args:
        directory (str | Path): The directory to scan for CSV files.

    Returns:
        List[List[str]]: A nested list representing a combined CSV table.
    """
    header: List[List[str]] = []
    body: List[List[str]] = []

    for entry in scandir(directory):
        if entry.is_file:
            csv_table = read_csv(entry.path)

            if not header:
                header = [csv_table[0]]

            # NOTE: Trailing spaces and newlines at EOF can cause empty lists
            # to be added to the body. We check if the List is valid first to
            # avoid this issue.
            if csv_table[1:]:
                body.extend(csv_table[1:])

    sorted_table = sorted(body, key=lambda row: row[IRColumn.DATETIME.value])

    return header + sorted_table
