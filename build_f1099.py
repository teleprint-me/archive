import sys
from argparse import ArgumentParser, Namespace

from archive.f1099.process import process_f1099


def get_arguments() -> Namespace:
    parser = ArgumentParser(
        description="Merge Form 8949 and Robinhood 1099 datasets."
    )

    parser.add_argument(
        "--form8949",
        type=str,
        required=True,
        help="The filepath to the existing Form 8949 CSV file.",
    )

    parser.add_argument(
        "--robinhood1099",
        type=str,
        required=True,
        help="The filepath to the Robinhood 1099 CSV file.",
    )

    parser.add_argument(
        "--asset",
        type=str,
        default="BTC",
        help="The base asset symbol to be included (e.g., BTC, ETH).",
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

    return parser.parse_args(sys.argv[1:])


def main():
    args = get_arguments()

    process_f1099(
        form8949_filepath=args.form8949,
        robinhood1099_filepath=args.robinhood1099,
        asset=args.asset,
        label=args.label,
        start_date=args.start_date,
        end_date=args.end_date,
    )


if __name__ == "__main__":
    main()
