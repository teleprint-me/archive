from typing import Optional

import iso8601

from archive.form8949.models import F8949Transaction


def filter_transactions_by_date(
    transactions: list[F8949Transaction],
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
) -> list[F8949Transaction]:
    if bool(start_date):
        start_date = iso8601.parse_date(start_date)

    if bool(end_date):
        end_date = iso8601.parse_date(end_date)

    filtered_transactions = []

    for transaction in transactions:
        date_sold = iso8601.parse_date(transaction.date_sold)

        if start_date and end_date:
            if start_date <= date_sold <= end_date:
                filtered_transactions.append(transaction)
        elif start_date:
            if start_date <= date_sold:
                filtered_transactions.append(transaction)
        else:
            filtered_transactions.append(transaction)

    return filtered_transactions


def format_datetime(transaction: F8949Transaction) -> F8949Transaction:
    date_acquired = iso8601.parse_date(transaction.date_acquired)
    date_sold = iso8601.parse_date(transaction.date_sold)

    transaction.date_acquired = date_acquired.strftime("%Y-%m-%d %H:%M:%S.%f")
    transaction.date_sold = date_sold.strftime("%Y-%m-%d %H:%M:%S.%f")

    return transaction


def calculate_gain_or_loss(transaction: F8949Transaction) -> F8949Transaction:
    gain_or_loss = transaction.proceeds - transaction.cost_or_other_basis
    transaction.gain_or_loss = gain_or_loss
    return transaction


def parse_f8949(
    transactions: list[F8949Transaction],
) -> list[F8949Transaction]:
    parsed_transactions = []

    for transaction in transactions:
        formatted_transaction = format_datetime(transaction)
        parsed_transaction = calculate_gain_or_loss(formatted_transaction)
        parsed_transactions.append(parsed_transaction)

    return parsed_transactions
