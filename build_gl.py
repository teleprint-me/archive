import argparse
import sys
from pathlib import Path
from typing import Union

from archive.gl.parser import parse_gl
from archive.gl.scanner import get_gl_csv_table, scan_gl_transactions
from archive.tools.io import print_csv, write_csv


def main(asset: str, directory: Union[str, Path]):
    gl_transactions = scan_gl_transactions(asset, directory)
    gl_transactions = parse_gl(gl_transactions)
    csv_gl_transactions = get_gl_csv_table(gl_transactions)
    print_csv(csv_gl_transactions)
    output_file_path = Path("data/gl/gains-and-losses.csv")
    write_csv(output_file_path, csv_gl_transactions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process IR transactions and generate GL transactions."
    )

    parser.add_argument(
        "directory",
        type=str,
        help="The directory containing the IR CSV files.",
    )

    parser.add_argument(
        "--asset",
        type=str,
        default="BTC",
        help="The base asset symbol to be calculated (e.g., BTC, ETH).",
    )

    args = parser.parse_args(sys.argv[1:])

    main(args.asset, args.directory)
