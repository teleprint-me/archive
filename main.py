import sys
from argparse import ArgumentParser, Namespace

from archive.f8949.process import process_f8949
from archive.gl.process import process_gl
from archive.ir.process import process_ir


def get_arguments() -> Namespace:
    parser = ArgumentParser(
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

    return parser.parse_args(sys.argv[1:])


def main() -> None:
    args = get_arguments()

    # Step 1: Process exchange CSV files for each exchange
    for exchange, file_path in args.exchange_file:
        process_ir(args.asset, args.label, exchange, file_path)

    # Step 2: Process IR transactions and generate GL transactions
    gl_file_path = process_gl(args.asset, args.label, "data/ir/")

    # Step 3: Process GL transactions and generate Form 8949 CSV
    process_f8949(gl_file_path, args.label, args.start_date, args.end_date)


if __name__ == "__main__":
    main()
