from pathlib import Path
from typing import List, Optional, Union

from peewee import OperationalError, SqliteDatabase

from archive.ir.models import IRTransaction, IRTransactionModel


def db_connect(
    db_path: Optional[Union[str, Path]] = "",
) -> Optional[SqliteDatabase]:
    """Connect to the database and create the table if it does not exist.

    Args:
        db_path (Optional[Union[str, Path]], optional): Path to the database file. Defaults to "transactions.db".

    Returns:
        Optional[SqliteDatabase]: A connected database object or None if connection fails.
    """
    db_path = db_path or Path("transactions.db")
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


def read_ir_table(db: Optional[SqliteDatabase]) -> List[IRTransaction]:
    """Read the IRTransaction table from the database and return a list of IRTransaction objects.

    Args:
        db (Optional[SqliteDatabase]): A connected database object.

    Returns:
        List[IRTransaction]: A list of IRTransaction objects.
    """
    ir_transactions = []

    if not db:
        return ir_transactions

    query = IRTransactionModel.select()

    for row in query:
        ir_transaction = IRTransaction(
            exchange=row.exchange,
            product=row.product,
            datetime=row.datetime,
            transaction_type=row.transaction_type,
            order_size=row.order_size,
            market_price=row.market_price,
            order_fee=row.order_fee,
            order_note=row.order_note,
        )

        ir_transactions.append(ir_transaction)

    return ir_transactions


def write_ir_table(
    transactions: List[IRTransaction],
    db: Optional[SqliteDatabase],
) -> None:
    """Write a list of IRTransaction objects to the database.

    Args:
        transactions (List[IRTransaction]): A list of IRTransaction objects.
        db (Optional[SqliteDatabase]): A connected database object.
    """
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
