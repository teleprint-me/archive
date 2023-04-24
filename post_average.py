import sys
from argparse import ArgumentParser, Namespace

from archive.average.cost import execute_cost_average
from archive.average.dynamic import execute_dynamic_average
from archive.average.value import execute_value_average


def get_arguments() -> Namespace:
    parser = ArgumentParser(description="Post Averaging Orders.")

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="data/average/average_records.csv",
        help="File to read from and write to (default: average_records.csv)",
    )

    parser.add_argument(
        "-x",
        "--execute",
        action="store_true",  # NOTE: Ensure this is store_true!
        help="Execute order based on set environment variables",
    )

    parser.add_argument(
        "-c",
        "--cost-average",
        action="store_true",
        help="Simulate or execute cost averaging. (default)",
    )

    parser.add_argument(
        "-d",
        "--dynamic-average",
        action="store_true",
        help="Simulate or execute dynamic averaging.",
    )

    parser.add_argument(
        "-v",
        "--value-average",
        action="store_true",
        help="Simulate or execute value averaging.",
    )

    return parser.parse_args(sys.argv[1:])


def main():
    args = get_arguments()

    if args.dynamic_average:
        execute_dynamic_average(args.file, args.execute)
    elif args.value_average:
        execute_value_average(args.file, args.execute)
    else:
        execute_cost_average(args.file, args.execute)


if __name__ == "__main__":
    main()
