from pathlib import Path
from typing import Union

import iso8601

from archive.ir.builder import build_ir_csv_table
from archive.ir.factory import parser_factory
from archive.tools.io import print_csv, write_csv
from archive.tools.sort import sort_csv


def process_ir(
    asset: str,
    label: str,
    exchange: str,
    file_path: Union[str, Path],
    output_dir: Union[str, Path],
) -> None:
    # Format user input
    asset = asset.upper()
    label = label.lower()
    exchange = exchange.lower()

    # Parse specified exchange transactions
    parser = parser_factory(exchange)
    transactions = parser.parse(file_path, asset)

    # Do nothing if data set is empty
    if not (len(transactions) > 0):
        return

    # Format transactions
    for transaction in transactions:
        # Format datetime
        datetime = iso8601.parse_date(transaction.datetime)
        transaction.datetime = datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        # Format transaction type
        transaction_type = ""
        # NOTE: Some transactions have more than a single word
        elements = transaction.transaction_type.split()
        # Cycle through the list of words
        for element in elements:
            # Format the words individual and append them
            transaction_type += element.capitalize()
        # Update the transaction type
        transaction.transaction_type = transaction_type

    # Keep only the transactions specified by the user
    transactions = [tx for tx in transactions if tx.should_keep([asset])]

    csv_transactions = build_ir_csv_table(transactions)
    csv_sorted = sort_csv(csv_transactions, column=2)
    print_csv(csv_sorted)

    output_file_path = Path(output_dir, f"ir-{exchange}-{label}.csv")
    write_csv(output_file_path, csv_sorted)
