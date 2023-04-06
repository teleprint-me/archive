from pathlib import Path
from typing import Union

from archive.f8949.models import F8949Columns, F8949Transaction
from archive.gl.models import GLTransaction
from archive.gl.scanner import get_gl_transactions
from archive.tools.io import read_csv


def get_f8949_csv_row(
    transaction: F8949Transaction,
) -> list[str]:
    return [
        transaction.description_of_property,
        transaction.date_acquired,
        transaction.date_sold,
        f"{transaction.proceeds:.2f}",
        f"{transaction.cost_or_other_basis:.2f}",
        transaction.codes,
        f"{transaction.amount_of_adjustment:.2f}",
        f"{transaction.gain_or_loss:.2f}",
    ]


def get_f8949_csv_table(
    transactions: list[F8949Transaction],
) -> list[list[str]]:
    # include the header in the conversion process
    csv_header = [
        [
            "Description of property",
            "Date Acquired",
            "Date Sold or Disposed of",
            "Sales Proceeds",
            "Cost or Other Basis",
            "Codes",
            "Adjustments to Gain or (Loss)",
            "Gain or (Loss)",
        ]
    ]
    csv_table = []
    for row in transactions:
        transaction = get_f8949_csv_row(row)
        csv_table.append(transaction)
    return csv_header + csv_table


def get_f8949_transaction(csv_row: list[str]) -> F8949Transaction:
    return F8949Transaction(
        description_of_property=csv_row[
            F8949Columns.DESCRIPTION_OF_PROPERTY.value
        ],
        date_acquired=csv_row[F8949Columns.DATE_ACQUIRED.value],
        date_sold=csv_row[F8949Columns.DATE_SOLD.value],
        proceeds=float(csv_row[F8949Columns.PROCEEDS.value]),
        cost_or_other_basis=float(
            csv_row[F8949Columns.COST_OR_OTHER_BASIS.value]
        ),
        codes=csv_row[F8949Columns.CODES.value],
        amount_of_adjustment=float(
            csv_row[F8949Columns.AMOUNT_OF_ADJUSTMENT.value]
        ),
        gain_or_loss=float(csv_row[F8949Columns.GAIN_OR_LOSS.value]),
    )


def get_f8949_transactions(
    csv_table: list[list[str]],
) -> list[F8949Transaction]:
    transactions = []
    # omit the header from the conversion process
    for csv_row in csv_table[1:]:
        transaction = get_f8949_transaction(csv_row)
        transactions.append(transaction)
    return transactions


def build_f8949_transactions(
    gl_transactions: list[GLTransaction],
) -> list[F8949Transaction]:
    transactions = []

    for gl_transaction in gl_transactions:
        if gl_transaction.is_buy:
            continue
        if gl_transaction.additional_description == "total":
            continue
        description_of_property = (
            f"{gl_transaction.description}"
            f" - {gl_transaction.additional_description}"
        )

        cost_or_other_basis = (
            gl_transaction.cost_or_other_basis + gl_transaction.exchange_fee
        )

        f8949_transaction = F8949Transaction(
            description_of_property=description_of_property,
            date_acquired=gl_transaction.date_acquired,
            date_sold=gl_transaction.date_sold,
            proceeds=gl_transaction.sales_proceeds,
            cost_or_other_basis=cost_or_other_basis,
        )

        transactions.append(f8949_transaction)

    return transactions


def scan_f8949_transactions(
    filepath: Union[str, Path]
) -> list[F8949Transaction]:
    csv_table = read_csv(filepath)
    transactions = get_gl_transactions(csv_table)
    return build_f8949_transactions(transactions)
