import argparse
import sys
from pathlib import Path
from typing import Union

from archive.gl.builder import build_gl_csv, build_gl_transactions
from archive.ir.builder import build_ir_transactions, read_ir_transactions
from archive.tools.io import print_csv, write_csv


def main(directory: Union[str, Path]):
    # Get the consolidated dataset as a CSV table.
    # read_ir_transactions(dir_path: str | Path) -> list[list[str]]
    csv_table = read_ir_transactions(directory)
    # Rebuild the IRTransactions from the CSV dataset.
    # build_ir_transactions(csv_table: list[list[str]]) -> list[IRTransaction]
    ir_transactions = build_ir_transactions(csv_table)
    # Build the GLTransactions from the IRTransaction dataset
    # build_gl_transactions(transactions: list[IRTransaction]) -> list[GLTransaction]
    gl_transactions = build_gl_transactions(ir_transactions)
    # Build the GL CSV dataset.
    # build_gl_csv(transactions: list[GLTransaction]) -> list[list[str]]
    csv_gl_transactions = build_gl_csv(gl_transactions)
    # Print the GL CSV dataset to stdout.
    # print_csv(csv_table: list[list[str]]) -> None
    print_csv(csv_gl_transactions)
    # Write transactions to CSV in the data/gl directory
    output_file_path = Path("data/gl/gains-and-losses.csv")
    # write_csv(path: str | Path, csv_table: list[list[str]]) -> None
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

    args = parser.parse_args(sys.argv[1:])

    main(args.directory)
