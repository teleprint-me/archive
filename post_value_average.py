import sys
from argparse import ArgumentParser, Namespace

from archive.average.cost import execute_cost_average


def get_arguments() -> Namespace:
    parser = ArgumentParser(description="Post Cost Average Orders.")

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="data/average/value_average_records.csv",
        help="File to read from and write to (default: value_average_records.csv)",
    )

    parser.add_argument(
        "-x",
        "--execute",
        action="store_true",  # NOTE: Ensure this is store_true!
        help="Execute order based on set environment variables",
    )

    return parser.parse_args(sys.argv[1:])


def main():
    args = get_arguments()

    execute_cost_average(args.file, args.execute)


if __name__ == "__main__":
    main()
