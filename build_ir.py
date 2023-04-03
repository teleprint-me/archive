import argparse
import sys
from pathlib import Path

from archive.ir.builder import build_ir_csv
from archive.ir.config import exchanges
from archive.tools.io import print_csv, write_csv
from archive.tools.sort import sort_csv


def main(exchange, file_path, included_assets, excluded_types):
    # get the exchange scanner
    scan_transactions = exchanges[exchange]["scan"]
    # get the exchange ir builder
    build_ir = exchanges[exchange]["build_ir"]
    # scan transaction using given filepath
    transactions = scan_transactions(file_path)

    # build the ir according to the dataset structure.
    # this is specific to each dataset for each exchange
    if exchange.lower() == "coinbase":
        ir_transactions = build_ir(
            transactions, included_assets, excluded_types
        )

    elif exchange.lower() == "coinbase_pro":
        ir_transactions = build_ir(transactions, included_assets)

    elif exchange.lower() == "kraken":
        ir_transactions = build_ir(transactions, included_assets)

    else:
        raise ValueError(f"Invalid exchange {exchange}")

    # Print formatted csv transactions
    csv_ir_transactions = build_ir_csv(ir_transactions)
    csv_sorted = sort_csv(csv_ir_transactions, column=2)
    print_csv(csv_sorted)

    # Write transactions to CSV in the data/ir directory
    output_file_path = Path("data/ir") / f"ir-{exchange.lower()}.csv"
    write_csv(output_file_path, csv_sorted)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process exchange CSV files.")
    parser.add_argument(
        "exchange", choices=exchanges.keys(), help="Name of the exchange."
    )
    parser.add_argument("file_path", help="Path to the input CSV file.")
    parser.add_argument(
        "--included-assets",
        nargs="+",
        default=["BTC"],
        help="List of assets to include.",
    )
    parser.add_argument(
        "--excluded-types",
        nargs="+",
        default=["Send", "Receive"],
        help="List of transaction types to exclude.",
    )

    args = parser.parse_args(sys.argv[1:])

    main(
        args.exchange,
        args.file_path,
        args.included_assets,
        args.excluded_types,
    )
