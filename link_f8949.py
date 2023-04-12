import sys
from argparse import ArgumentParser, Namespace

from archive.link.process import process_form_link


def get_arguments() -> Namespace:
    parser = ArgumentParser(
        description="Input Form-8949 and Robinhood-1099 datasets and output a unified Form-8949 for the given tax year."
    )

    parser.add_argument(
        "--form8949",
        type=str,
        required=True,
        help="The directory containing the Form-8949 files.",
    )

    parser.add_argument(
        "--form1099",
        type=str,
        default=None,
        help="The directory containing the Form-1099 CSV files.",
    )

    parser.add_argument(
        "--year",
        type=str,
        default=None,
        help="The year for the range of transactions (YYYY).",
    )

    parser.add_argument(
        "--label",
        type=str,
        default=None,
        help="A label to append to the output file name.",
    )

    return parser.parse_args(sys.argv[1:])


def main():
    args = get_arguments()

    process_form_link(
        f8949_directory=args.form8949,
        f1099_directory=args.form1099,
        year=args.year,
        label=args.label,
    )


if __name__ == "__main__":
    main()
