from pathlib import Path
from typing import Union

import iso8601

from archive.gl.models import GLTransaction
from archive.gl.parser import parse_gl
from archive.gl.scanner import get_gl_csv_table, scan_gl_transactions
from archive.tools.io import print_csv, write_csv


def format_transactions(
    transactions: list[GLTransaction],
) -> list[GLTransaction]:
    for transaction in transactions:
        if bool(transaction.date_acquired):
            date_acquired = iso8601.parse_date(transaction.date_acquired)
            transaction.date_acquired = date_acquired.strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )

        if bool(transaction.date_sold):
            date_sold = iso8601.parse_date(transaction.date_sold)
            transaction.date_sold = date_sold.strftime("%Y-%m-%d %H:%M:%S.%f")

        if bool(transaction.transaction_type):
            transaction_type = transaction.transaction_type.capitalize()
            transaction.transaction_type = transaction_type

    return transactions


def process_gl(
    asset: str,
    label: str,
    directory: Union[str, Path],
) -> Union[str, Path]:
    # Format user input
    asset = asset.upper()
    label = label.lower()

    gl_transactions = scan_gl_transactions(asset, directory)
    gl_transactions = format_transactions(gl_transactions)
    gl_transactions = parse_gl(gl_transactions)

    csv_gl_transactions = get_gl_csv_table(gl_transactions)
    print_csv(csv_gl_transactions, width=320)

    output_file_path = Path(f"data/gl/gl-{label}.csv")
    write_csv(output_file_path, csv_gl_transactions)

    return output_file_path
