# archive/ir/process.py
from pathlib import Path
from typing import List, Optional, Tuple, Union

import iso8601
from peewee import OperationalError, SqliteDatabase

from archive.ir.builder import build_ir_csv_table
from archive.ir.factory import parser_factory
from archive.ir.models import IRTransaction, IRTransactionModel
from archive.tools.io import print_csv, write_csv
from archive.tools.sort import sort_csv


def format_user_input(
    asset: str,
    label: str,
    exchange: str,
    output_mode: str,
) -> Tuple[str, str, str, str]:
    asset = asset.upper()
    label = label.lower()
    exchange = exchange.lower()
    output_mode = output_mode.lower()

    return asset, label, exchange, output_mode


def format_transactions(
    transactions: List[IRTransaction],
) -> List[IRTransaction]:
    for transaction in transactions:
        # Format datetime
        datetime = iso8601.parse_date(transaction.datetime)
        transaction.datetime = datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        # Format transaction type
        transaction_type = transaction.transaction_type.capitalize()
        transaction.transaction_type = transaction_type

    return transactions


def db_connect(
    db_path: str = "transactions.db",
) -> Optional[SqliteDatabase]:
    # Connect to the database
    db = SqliteDatabase(db_path)
    IRTransactionModel._meta.database = db

    try:
        db.connect()
        if not IRTransactionModel.table_exists():
            db.create_tables([IRTransactionModel], safe=True)
        return db
    except OperationalError:
        print(f"Error connecting to {db_path}. Exiting.")
        return None


def write_db(
    transactions: List[IRTransaction],
    db: Optional[SqliteDatabase],
) -> None:
    if not db:
        return None

    for transaction in transactions:
        try:
            # Check for duplicates
            IRTransactionModel.get(
                (IRTransactionModel.exchange == transaction.exchange)
                & (IRTransactionModel.product == transaction.product)
                & (IRTransactionModel.datetime == transaction.datetime)
                & (
                    IRTransactionModel.transaction_type
                    == transaction.transaction_type
                )
                & (IRTransactionModel.order_size == transaction.order_size)
                & (IRTransactionModel.market_price == transaction.market_price)
                & (IRTransactionModel.order_fee == transaction.order_fee)
                & (IRTransactionModel.order_note == transaction.order_note)
            )
        except IRTransactionModel.DoesNotExist:
            # Insert the new transaction if it's not a duplicate
            IRTransactionModel.create(
                exchange=transaction.exchange,
                product=transaction.product,
                datetime=transaction.datetime,
                transaction_type=transaction.transaction_type,
                order_size=transaction.order_size,
                market_price=transaction.market_price,
                order_fee=transaction.order_fee,
                order_note=transaction.order_note,
            )


def handle_output_mode(
    output_mode: str,
    csv_sorted: List[List[str]],
    output_file_path: Path,
    transactions: List[IRTransaction],
    db: Optional[SqliteDatabase],
) -> None:
    if output_mode == "print":
        print_csv(csv_sorted)
    elif output_mode == "csv":
        write_csv(output_file_path, csv_sorted)
    elif output_mode == "db":
        write_db(transactions, db)
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
    """Process Intermediary Representation Transaction data"""
    asset, label, exchange, output_mode = format_user_input(
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

    csv_transactions = build_ir_csv_table(formatted_transactions)
    csv_sorted = sort_csv(csv_transactions, column=2)

    handle_output_mode(
        output_mode,
        csv_sorted,
        output_file_path,
        formatted_transactions,
        db,
    )
