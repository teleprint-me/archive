from datetime import datetime
from pathlib import Path
from typing import Optional, Union

import iso8601
from iso8601.iso8601 import ParseError

from archive.f8949.models import F8949Transaction
from archive.f8949.parser import parse_f8949
from archive.f8949.scanner import get_f8949_csv_table, scan_f8949_transactions
from archive.tools.io import print_csv, write_csv


def filter_transactions_by_date(
    transactions: list[F8949Transaction],
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
) -> list[F8949Transaction]:
    has_start = bool(start_date)
    has_end = bool(end_date)

    if has_start:
        start_date = iso8601.parse_date(start_date)
    if has_end:
        end_date = iso8601.parse_date(end_date)

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


def process_f8949(
    file_path: Union[str, Path],
    label: str,
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
) -> None:
    scanned_transactions = scan_f8949_transactions(file_path)
    filtered_transactions = filter_transactions_by_date(
        scanned_transactions, start_date, end_date
    )
    parsed_transactions = parse_f8949(filtered_transactions)
    formatted_transactions = format_datetime(parsed_transactions)

    csv_f8949_transactions = get_f8949_csv_table(formatted_transactions)
    print_csv(csv_f8949_transactions)

    output_file_path = Path(f"data/f8949/f8949-{label}.csv")
    write_csv(output_file_path, csv_f8949_transactions)
