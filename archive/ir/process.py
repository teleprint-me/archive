# archive/ir/process.py
from pathlib import Path
from typing import List, Optional, Tuple, Union

import iso8601
from peewee import SqliteDatabase

from archive.ir.csv import build_csv_ir_table
from archive.ir.db import db_connect, write_ir_table
from archive.ir.factory import parser_factory
from archive.ir.models import IRTransaction
from archive.tools.io import print_csv, write_csv
from archive.tools.sort import sort_csv


def format_user_input(
    asset: str,
    label: str,
    exchange: str,
    output_mode: str,
) -> Tuple[str, str, str, str]:
    """Format user input to standardize the case of input values."""
    asset = asset.upper()
    label = label.lower()
    exchange = exchange.lower()
    output_mode = output_mode.lower()

    return asset, label, exchange, output_mode


def format_transactions(
    transactions: List[IRTransaction],
) -> List[IRTransaction]:
    """Format transaction datetime and transaction type values."""
    for transaction in transactions:
        # Format datetime
        datetime = iso8601.parse_date(transaction.datetime)
        transaction.datetime = datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        # Format transaction type
        transaction_type = transaction.transaction_type.capitalize()
        transaction.transaction_type = transaction_type

    return transactions


def handle_output_mode(
    output_mode: str,
    csv_sorted: List[List[str]],
    output_file_path: Path,
    transactions: List[IRTransaction],
    db: Optional[SqliteDatabase],
) -> None:
    """Handle different output modes based on user selection."""
    if output_mode == "print":
        print_csv(csv_sorted)
    elif output_mode == "csv":
        write_csv(output_file_path, csv_sorted)
    elif output_mode == "db":
        write_ir_table(transactions, db)
    else:
        print("Invalid output mode specified. Exiting.")


def process_ir(
    asset: str,
    label: str,
    exchange: str,
    source: str,
    output_mode: str,
    output_dir: Union[str, Path],
    input_file: Union[str, Path],
) -> None:
    """Process Intermediary Representation Transaction data."""
    (asset, label, exchange, output_mode) = format_user_input(
        asset, label, exchange, output_mode
    )

    output_file_path = Path(output_dir, f"ir-{exchange}-{label}.csv")

    db = db_connect()

    # Parse specified exchange transactions
    parser = parser_factory(exchange, source)
    transactions = parser.parse(input_file, asset)

    # Do nothing if data set is empty
    if not transactions:
        return None

    formatted_transactions = format_transactions(transactions)

    csv_transactions = build_csv_ir_table(formatted_transactions)
    csv_sorted = sort_csv(csv_transactions, column=2)

    handle_output_mode(
        output_mode,
        csv_sorted,
        output_file_path,
        formatted_transactions,
        db,
    )
