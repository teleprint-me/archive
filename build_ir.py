import sys
from argparse import ArgumentParser, Namespace

from archive.ir.process import process_ir


def get_arguments() -> Namespace:
    parser = ArgumentParser(description="Process exchange CSV files.")

    parser.add_argument(
        "--exchange-file",
        action="append",
        nargs=2,
        metavar=("EXCHANGE", "FILE_PATH"),
        help="Name of the exchange and path to the input CSV file. Repeat this argument for multiple exchanges.",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/ir",
        help="The output directory path for the IR files.",
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

    return parser.parse_args(sys.argv[1:])


def main():
    args = get_arguments()

    for exchange, file_path in args.exchange_file:
        process_ir(
            args.asset, args.label, exchange, file_path, args.output_dir
        )


if __name__ == "__main__":
    main()
