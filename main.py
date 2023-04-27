import sys
from argparse import ArgumentParser, Namespace

from archive.f1099.process import process_f1099
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
        "--robinhood1099",
        type=str,
        help="Path to the input Robinhood 1099 CSV file (optional).",
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

    parser.add_argument(
        "--ir-output-dir",
        type=str,
        default="data/ir",
        help="The output directory path for intermediate representation files.",
    )

    parser.add_argument(
        "--gl-output-dir",
        type=str,
        default="data/gl",
        help="The output directory path for gains and losses files.",
    )

    parser.add_argument(
        "--f8949-output-dir",
        type=str,
        default="data/f8949",
        help="The output directory path for Form-8949 files.",
    )

    parser.add_argument(
        "--f1099-output-dir",
        type=str,
        default="data/f1099",
        help="The output directory path for Form-1099 files.",
    )

    return parser.parse_args(sys.argv[1:])


def main() -> None:
    args = get_arguments()

    # Step 1: Process exchange CSV files for each exchange
    for exchange, file_path in args.exchange_file:
        process_ir(
            args.asset,
            args.label,
            exchange,
            file_path,
            args.ir_output_dir,
        )

    # Step 2: Process IR transactions and generate GL transactions
    gl_file_path = process_gl(
        args.asset, args.label, "data/ir/", args.gl_output_dir
    )

    if not gl_file_path:
        return None

    # Step 3: Process GL transactions and generate Form-8949 CSV
    f8949_file_path = process_f8949(
        gl_file_path,
        args.label,
        args.f8949_output_dir,
        args.start_date,
        args.end_date,
    )

    # Step 4: Process Form-1099 Transactions and generate Form-8949 CSV
    if args.robinhood1099:
        process_f1099(
            f8949_file_path,
            args.robinhood1099,
            args.asset,
            args.label,
            args.f1099_output_dir,
            args.start_date,
            args.end_date,
        )


if __name__ == "__main__":
    main()
