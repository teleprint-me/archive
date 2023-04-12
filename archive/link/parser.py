from os import scandir
from pathlib import Path

from dateutil import parser

from archive.f8949.models import F8949Columns, F8949Transaction
from archive.f8949.parser import calculate_gain_or_loss
from archive.tools.io import read_csv


def link_f8949_transactions(directory: str | Path) -> list[F8949Transaction]:
    transactions: list[F8949Transaction] = []

    for entry in scandir(directory):
        if entry.is_file():
            csv_table = read_csv(entry.path)

            for row in csv_table[1:]:
                transaction = F8949Transaction(
                    description_of_property=row[
                        F8949Columns.DESCRIPTION_OF_PROPERTY.value
                    ],
                    date_acquired=row[F8949Columns.DATE_ACQUIRED.value],
                    date_sold=row[F8949Columns.DATE_SOLD.value],
                    proceeds=float(row[F8949Columns.PROCEEDS.value]),
                    cost_or_other_basis=float(
                        row[F8949Columns.COST_OR_OTHER_BASIS.value]
                    ),
                    codes=row[F8949Columns.CODES.value],
                    amount_of_adjustment=float(
                        row[F8949Columns.AMOUNT_OF_ADJUSTMENT.value]
                    ),
                    gain_or_loss=float(row[F8949Columns.GAIN_OR_LOSS.value]),
                )

                transaction = calculate_gain_or_loss(transaction)

                transactions.append(transaction)

    return transactions


def remove_duplicate_transactions(
    transactions: list[F8949Transaction],
) -> list[F8949Transaction]:
    seen = set()
    filtered_transactions = []

    for transaction in transactions:
        transaction_hash = hash(
            (
                transaction.description_of_property,
                transaction.date_acquired,
                transaction.date_sold,
                transaction.proceeds,
                transaction.cost_or_other_basis,
                transaction.codes,
                transaction.amount_of_adjustment,
                transaction.gain_or_loss,
            )
        )

        if transaction_hash not in seen:
            seen.add(transaction_hash)
            filtered_transactions.append(transaction)

    return filtered_transactions


def filter_transactions_by_year(
    transactions: list[F8949Transaction], year: str
) -> list[F8949Transaction]:
    filtered_transactions = []

    dt_year = parser.parse(year)

    for transaction in transactions:
        dt_sold = parser.parse(transaction.date_sold)

        if dt_sold.year == dt_year.year:
            filtered_transactions.append(transaction)

    return filtered_transactions
