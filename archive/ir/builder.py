from os import scandir
from pathlib import Path

from archive.ir.models import IRColumn, IRTransaction
from archive.tools.io import read_csv


def build_ir_csv_table(
    transactions: list[IRTransaction],
) -> list[list[str]]:
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


def build_ir_transactions(csv_table: list[list[str]]) -> list[IRTransaction]:
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


def scan_ir_transactions(directory: str | Path) -> list[list[str]]:
    header: list[list[str]] = []
    body: list[list[str]] = []

    for entry in scandir(directory):
        if entry.is_file:
            csv_table = read_csv(entry.path)

            if not header:
                header = [csv_table[0]]

            body.extend(csv_table[1:])

    sorted_table = sorted(body, key=lambda row: row[IRColumn.DATETIME.value])

    return header + sorted_table
