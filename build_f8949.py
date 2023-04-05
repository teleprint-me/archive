import argparse
import sys
from pathlib import Path
from typing import Optional, Union

from archive.form8949.parser import filter_transactions_by_date, parse_f8949
from archive.form8949.scanner import (
    get_f8949_csv_table,
    scan_f8949_transactions,
)
from archive.tools.io import print_csv, write_csv


def main(
    filepath: Union[str, Path],
    label: str,
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
):
    f8949_transactions = scan_f8949_transactions(filepath)
    f8949_transactions = parse_f8949(f8949_transactions)
    f8949_transactions = filter_transactions_by_date(
        f8949_transactions, start_date, end_date
    )
    csv_f8949_transactions = get_f8949_csv_table(f8949_transactions)
    print_csv(csv_f8949_transactions)
    output_file_path = Path(f"data/out/form-8949-{label}.csv")
    write_csv(output_file_path, csv_f8949_transactions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process GL transactions and generate Form 8949 CSV."
    )

    parser.add_argument(
        "filepath",
        type=str,
        help="The filepath to the gains and losses CSV file.",
    )

    parser.add_argument(
        "--label",
        type=str,
        default="bitcoin",
        help="A label to append to the output file name.",
    )

    parser.add_argument(
        "--start_date",
        type=str,
        default=None,
        help="The start date for the range of transactions (YYYY-MM-DD).",
    )

    parser.add_argument(
        "--end_date",
        type=str,
        default=None,
        help="The end date for the range of transactions (YYYY-MM-DD).",
    )

    args = parser.parse_args(sys.argv[1:])

    main(args.filepath, args.label, args.start_date, args.end_date)
