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
) -> None:
    # Format user input
    asset = asset.upper()
    label = label.lower()
    exchange = exchange.lower()

    # Parse specified exchange transactions
    parser = parser_factory(exchange)
    transactions = parser.parse(file_path, asset)

    # Format transactions
    for transaction in transactions:
        # Format datetime
        datetime = iso8601.parse_date(transaction.datetime)
        transaction.datetime = datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        # Format transaction type
        transaction_type = transaction.transaction_type.capitalize()
        transaction.transaction_type = transaction_type

    csv_transactions = build_ir_csv_table(transactions)
    csv_sorted = sort_csv(csv_transactions, column=2)
    print_csv(csv_sorted)

    output_file_path = Path(f"data/ir/ir-{exchange}-{label}.csv")
    write_csv(output_file_path, csv_sorted)
