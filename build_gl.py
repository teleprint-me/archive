import sys
from argparse import ArgumentParser, Namespace

from archive.gl.process import process_gl


def get_arguments() -> Namespace:
    parser = ArgumentParser(
        description="Process IR transactions and generate GL transactions."
    )

    parser.add_argument(
        "directory",
        type=str,
        help="The directory containing the IR CSV files.",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/gl",
        help="The output directory path for the GL files.",
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

    process_gl(args.asset, args.label, args.directory, args.output_dir)


if __name__ == "__main__":
    main()
