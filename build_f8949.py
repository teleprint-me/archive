import sys
from argparse import ArgumentParser, Namespace

from archive.f8949.process import process_f8949


def get_arguments() -> Namespace:
    parser = ArgumentParser(
        description="Process GL transactions and generate Form 8949 CSV."
    )

    parser.add_argument(
        "filepath",
        type=str,
        help="The filepath to the gains and losses CSV file.",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/f8949",
        help="The output directory path for the Form 8949 files.",
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

    process_f8949(
        args.filepath,
        args.label,
        args.output_dir,
        args.start_date,
        args.end_date,
    )


if __name__ == "__main__":
    main()
