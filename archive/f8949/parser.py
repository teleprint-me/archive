from datetime import datetime
from typing import Optional

import iso8601
from iso8601 import parse_date
from iso8601.iso8601 import ParseError

from archive.f8949.models import F8949Transaction


def filter_transactions_by_date(
    transactions: list[F8949Transaction],
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
) -> list[F8949Transaction]:
    has_start = bool(start_date)
    has_end = bool(end_date)

    if has_start:
        start_date = parse_date(start_date)
    if has_end:
        end_date = parse_date(end_date)

    filtered_transactions = []

    for transaction in transactions:
        try:
            date_sold = iso8601.parse_date(transaction.date_sold)
        except (ParseError,):
            dt = datetime.strptime(transaction.date_sold, "%m/%d/%y")
            date_sold = dt.strftime("%Y-%m-%d")

        if has_start and has_end:
            if start_date <= date_sold <= end_date:
                filtered_transactions.append(transaction)
        elif has_start:
            if start_date <= date_sold:
                filtered_transactions.append(transaction)
        else:
            filtered_transactions.append(transaction)

    return filtered_transactions


def format_datetime(
    transactions: list[F8949Transaction],
) -> list[F8949Transaction]:
    for transaction in transactions:
        try:
            date_acquired = iso8601.parse_date(transaction.date_acquired)
        except (ParseError,):
            dt = datetime.strptime(transaction.date_acquired, "%m/%d/%y")
            date_acquired_str = dt.strftime("%Y-%m-%d")
            date_acquired = iso8601.parse_date(date_acquired_str)
            transaction.date_acquired = date_acquired_str

        try:
            date_sold = iso8601.parse_date(transaction.date_sold)
        except (ParseError,):
            dt = datetime.strptime(transaction.date_sold, "%m/%d/%y")
            date_sold_str = dt.strftime("%Y-%m-%d")
            date_sold = iso8601.parse_date(date_sold_str)
            transaction.date_sold = date_sold_str

        transaction.date_sold = date_sold.strftime("%Y-%m-%d %H:%M:%S.%f")
        transaction.date_acquired = date_acquired.strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )

    return transactions


def calculate_gain_or_loss(transaction: F8949Transaction) -> F8949Transaction:
    gain_or_loss = transaction.proceeds - transaction.cost_or_other_basis
    transaction.gain_or_loss = gain_or_loss
    return transaction


def parse_f8949(
    transactions: list[F8949Transaction],
) -> list[F8949Transaction]:
    parsed_transactions = []

    for transaction in transactions:
        parsed_transaction = calculate_gain_or_loss(transaction)
        parsed_transactions.append(parsed_transaction)

    return parsed_transactions
