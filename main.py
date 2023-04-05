import argparse
import sys
from typing import Optional

from archive.form8949.process import process_f8949
from archive.gl.process import process_gl
from archive.ir.process import process_ir


def main(
    exchange_file_list: list[tuple[str, str]],
    asset: str,
    label: str,
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
):
    # Step 1: Process exchange CSV files for each exchange
    for exchange, file_path in exchange_file_list:
        process_ir(asset, label, exchange, file_path)

    # Step 2: Process IR transactions and generate GL transactions
    gl_file_path = process_gl(asset, label, "data/ir/")

    # Step 3: Process GL transactions and generate Form 8949 CSV
    process_f8949(gl_file_path, label, start_date, end_date)


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
