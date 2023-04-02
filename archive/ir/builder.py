from os import scandir
from pathlib import Path

from archive.ir.transaction import IRColumns, IRTransaction
from archive.tools.io import read_csv


def build_ir_csv_row(
    ir_transaction: IRTransaction,
) -> list[str]:
    return [
        ir_transaction.exchange,
        ir_transaction.product,
        ir_transaction.datetime,
        ir_transaction.transaction_type,
        f"{float(ir_transaction.order_size):.8f}",
        f"{float(ir_transaction.market_price):.8f}",
        f"{float(ir_transaction.order_fee):.8f}",
        ir_transaction.order_note,
    ]


def build_ir_csv(
    ir_table: list[IRTransaction],
) -> list[list[str]]:
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
    transactions = [build_ir_csv_row(ir_tx) for ir_tx in ir_table]
    return header + transactions


def read_ir_transactions(dir_path: str | Path) -> list[list[str]]:
    header: list[list[str]] = []
    table: list[list[str]] = []

    for entry in scandir(dir_path):
        if entry.is_file:
            csv_table = read_csv(entry.path)
            if not header:
                header = [csv_table[0]]
            table.extend(csv_table[1:])

    sorted_table = sorted(table, key=lambda row: row[IRColumns.DATETIME.value])

    return header + sorted_table


def build_ir_transactions(csv_table: list[list[str]]) -> list[IRTransaction]:
    transactions = []
    for row in csv_table[1:]:  # Skip the header row
        transaction = IRTransaction(
            exchange=row[IRColumns.EXCHANGE.value],
            product=row[IRColumns.PRODUCT.value],
            datetime=row[IRColumns.DATETIME.value],
            transaction_type=row[IRColumns.TRANSACTION_TYPE.value],
            order_size=float(row[IRColumns.ORDER_SIZE.value]),
            market_price=float(row[IRColumns.MARKET_PRICE.value]),
            order_fee=float(row[IRColumns.ORDER_FEE.value]),
            order_note=row[IRColumns.ORDER_NOTE.value],
        )
        transactions.append(transaction)

    return transactions
