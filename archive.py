import argparse
import sys
from pathlib import Path
from typing import Optional

from archive.form8949.parser import filter_transactions_by_date, parse_f8949
from archive.form8949.scanner import (
    get_f8949_csv_table,
    scan_f8949_transactions,
)
from archive.gl.parser import parse_gl
from archive.gl.scanner import get_gl_csv_table, scan_gl_transactions
from archive.ir.scanner import scan_ir_transactions
from archive.tools.io import print_csv, write_csv

# TODO: Update the script to expect a single asset symbol instead of a list of included products
# and get rid of the excluded types. Use default values for now.


def main(
    exchange_file_list: list[tuple[str, str]],
    asset: str,
    label: str,
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
):
    ir_transactions_all = []

    # Step 1: Process exchange CSV files for each exchange
    for exchange, file_path in exchange_file_list:
        ir_transactions = process_exchange_csv(
            exchange, file_path, asset, label
        )
        ir_transactions_all.extend(ir_transactions)

        ir_output_file_path = Path(f"data/ir/ir-{exchange}-{label}.csv")
        write_csv(ir_output_file_path, ir_transactions)

    # Combine IR transactions from all exchanges into a single CSV file
    ir_all_output_file_path = Path(f"data/ir/ir-all-{label}.csv")
    write_csv(ir_all_output_file_path, ir_transactions_all)

    # Step 2: Process IR transactions and generate GL transactions
    gl_transactions = process_ir_transactions(asset, label)
    gl_output_file_path = Path(f"data/gl/gains-and-losses-{label}.csv")
    write_csv(gl_output_file_path, gl_transactions)

    # Step 3: Process GL transactions and generate Form 8949 CSV
    f8949_transactions = process_gl_transactions(label, start_date, end_date)
    f8949_output_file_path = Path(f"data/out/form-8949-{label}.csv")
    write_csv(f8949_output_file_path, f8949_transactions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process transactions and generate Form 8949."
    )

    parser.add_argument(
        "--exchange-file",
        action="append",
        nargs=2,
        metavar=("EXCHANGE", "FILE_PATH"),
        help="Name of the exchange and path to the input CSV file. Repeat this argument for multiple exchanges.",
    )

    parser.add_argument(
        "--asset",
        type=str,
        default="BTC",
        help="The base asset symbol to be calculated (e.g., BTC, ETH).",
    )

    parser.add_argument(
        "--label",
        type=str,
        default="bitcoin",
        help="A label to be appended to the output file name.",
    )

    parser.add_argument(
        "--start-date",
        type=str,
        help="The start date for transactions to be included (YYYY-MM-DD).",
    )

    parser.add_argument(
        "--end-date",
        type=str,
        help="The end date for transactions to be included (YYYY-MM-DD).",
    )

    args = parser.parse_args(sys.argv[1:])

    main(
        args.exchange_file,
        args.asset,
        args.label,
        args.start_date,
        args.end_date,
    )
