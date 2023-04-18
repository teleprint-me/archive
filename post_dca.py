import sys
from argparse import ArgumentParser, Namespace

from archive.average.cost import execute_dca


def get_arguments() -> Namespace:
    parser = ArgumentParser(description="Post DCA orders.")

    parser.add_argument(
        "-x",
        "--execute",
        action="store_false",
        help="The key of the environment variable to set",
    )

    return parser.parse_args(sys.argv[1:])


def main():
    args = get_arguments()

    execute_dca(args.execute)


if __name__ == "__main__":
    main()
