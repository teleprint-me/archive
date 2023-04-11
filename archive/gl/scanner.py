from pathlib import Path
from typing import Union

from archive.gl.models import GLColumns, GLTransaction
from archive.ir.builder import build_ir_transactions, scan_ir_transactions
from archive.ir.models import IRTransaction


def get_gl_csv_row(
    transaction: GLTransaction,
) -> list[str]:
    return [
        transaction.additional_description,
        transaction.description,
        transaction.date_acquired,
        transaction.transaction_type,
        f"{transaction.order_size:.8f}",
        f"{transaction.market_price:.2f}",
        f"{transaction.exchange_fee:.2f}",
        f"{transaction.cost_or_other_basis:.2f}",
        f"{transaction.acb_per_share:.2f}",
        transaction.date_sold,
        f"{transaction.sales_proceeds:.2f}",
        f"{transaction.gain_or_loss:.2f}",
        transaction.order_note,
    ]


def get_gl_csv_table(
    transactions: list[GLTransaction],
) -> list[list[str]]:
    # include the header in the conversion process
    csv_header = [
        [
            "Additional Description",
            "Description",
            "Date Acquired",
            "Transaction Type",
            "Order Size",
            "Market Price",
            "Exchange Fee",
            "Cost or Other Basis",
            "ACB per Share",
            "Date Sold",
            "Sales Proceeds",
            "Gain or Loss",
            "Order Note",
        ]
    ]
    csv_table = []
    for row in transactions:
        transaction = get_gl_csv_row(row)
        csv_table.append(transaction)
    return csv_header + csv_table


def get_gl_transaction(csv_row: list[str]) -> GLTransaction:
    return GLTransaction(
        additional_description=csv_row[GLColumns.ADDITIONAL_DESCRIPTION.value],
        description=csv_row[GLColumns.DESCRIPTION.value],
        date_acquired=csv_row[GLColumns.DATE_ACQUIRED.value],
        transaction_type=csv_row[GLColumns.TRANSACTION_TYPE.value],
        order_size=float(csv_row[GLColumns.ORDER_SIZE.value]),
        market_price=float(csv_row[GLColumns.MARKET_PRICE.value]),
        exchange_fee=float(csv_row[GLColumns.EXCHANGE_FEE.value]),
        cost_or_other_basis=float(
            csv_row[GLColumns.COST_OR_OTHER_BASIS.value]
        ),
        acb_per_share=float(csv_row[GLColumns.ACB_PER_SHARE.value]),
        date_sold=csv_row[GLColumns.DATE_SOLD.value],
        sales_proceeds=float(csv_row[GLColumns.SALES_PROCEEDS.value]),
        gain_or_loss=float(csv_row[GLColumns.GAIN_OR_LOSS.value]),
        order_note=csv_row[GLColumns.ORDER_NOTE.value],
    )


def get_gl_transactions(
    csv_table: list[list[str]],
) -> list[GLTransaction]:
    transactions = []
    # omit the header from the conversion process
    for csv_row in csv_table[1:]:
        transaction = get_gl_transaction(csv_row)
        transactions.append(transaction)
    return transactions


def filter_transactions(
    asset: str, transactions: list[IRTransaction]
) -> list[IRTransaction]:
    filtered_transactions = []
    for transaction in transactions:
        if transaction.product.startswith(asset):
            filtered_transactions.append(transaction)
    return filtered_transactions


def build_gl_transactions(
    ir_transactions: list[IRTransaction],
) -> list[GLTransaction]:
    transactions = []

    last_acquired = ""

    for ir_transaction in ir_transactions:
        if ir_transaction.is_buy:
            gl_transaction = GLTransaction(
                additional_description=ir_transaction.exchange,
                description=ir_transaction.product,
                date_acquired=ir_transaction.datetime,
                transaction_type=ir_transaction.transaction_type,
                order_size=ir_transaction.order_size,
                market_price=ir_transaction.market_price,
                exchange_fee=ir_transaction.order_fee,
                order_note=ir_transaction.order_note,
            )

            last_acquired = gl_transaction.date_acquired

        else:
            gl_transaction = GLTransaction(
                additional_description=ir_transaction.exchange,
                description=ir_transaction.product,
                date_acquired=last_acquired,
                transaction_type=ir_transaction.transaction_type,
                order_size=ir_transaction.order_size,
                market_price=ir_transaction.market_price,
                exchange_fee=ir_transaction.order_fee,
                date_sold=ir_transaction.datetime,
            )

        transactions.append(gl_transaction)

    return transactions


def remove_duplicate_transactions(
    transactions: list[IRTransaction],
) -> list[IRTransaction]:
    seen = set()
    filtered_transactions = []

    for transaction in transactions:
        transaction_hash = hash(
            (
                transaction.datetime,
                transaction.transaction_type,
                transaction.product,
                transaction.order_size,
                transaction.market_price,
                transaction.order_fee,
                transaction.exchange,
            )
        )

        if transaction_hash not in seen:
            seen.add(transaction_hash)
            filtered_transactions.append(transaction)

    return filtered_transactions


def scan_gl_transactions(
    asset: str, directory: Union[str, Path]
) -> list[GLTransaction]:
    csv_table = scan_ir_transactions(directory)
    transactions = build_ir_transactions(csv_table)
    transactions = remove_duplicate_transactions(transactions)
    filtered_transactions = filter_transactions(asset, transactions)
    return build_gl_transactions(filtered_transactions)
