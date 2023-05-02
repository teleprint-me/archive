# ./build_ir.py
import sys
from argparse import ArgumentParser, Namespace

from archive.ir.process import process_ir


def get_arguments() -> Namespace:
    parser = ArgumentParser(description="Process exchange CSV files.")

    parser.add_argument(
        "-i",
        "--input-src",
        action="append",
        nargs=3,
        metavar=("EXCHANGE", "SOURCE", "INPUT_FILE"),
        help="The name of the exchange, source, and file path to the input CSV file. Repeat this argument for multiple exchanges.",
    )

    parser.add_argument(
        "-m",
        "--output-mode",
        type=str,
        choices=["print", "csv", "db"],
        default="csv",
        help="The output mode for processed data. Choices are 'print', 'csv', or 'db' (default: csv).",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="data/ir",
        help="The output directory path for the Intermediary Representation files (default: data/ir).",
    )

    parser.add_argument(
        "-a",
        "--asset",
        type=str,
        default="BTC",
        help="The base asset symbol to be calculated (default: BTC; e.g., ETH, LTC).",
    )

    parser.add_argument(
        "-l",
        "--label",
        type=str,
        default="bitcoin",
        help="A label to be appended to the output file name (default: bitcoin).",
    )

    return parser.parse_args(sys.argv[1:])


def main():
    args = get_arguments()

    for exchange, source, input_file in args.input_src:
        process_ir(
            asset=args.asset,
            label=args.label,
            exchange=exchange,
            source=source,
            output_mode=args.output_mode,
            output_dir=args.output_dir,
            input_file=input_file,
        )


if __name__ == "__main__":
    main()
