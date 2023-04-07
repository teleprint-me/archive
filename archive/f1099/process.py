from pathlib import Path
from typing import Union

from archive.f1099.parser import (
    convert_robinhood_to_f8949_transactions,
    merge_f8949_transactions,
)
from archive.f1099.scanner import scan_form_8949, scan_robinhood_1099
from archive.f8949.process import filter_transactions_by_date, format_datetime
from archive.f8949.scanner import get_f8949_csv_table
from archive.tools.io import print_csv, write_csv
from archive.tools.sort import sort_csv


def process_f1099(
    form8949_filepath: Union[str, Path],
    robinhood1099_filepath: str,
    asset: str,
    label: str,
    start_date: str = "",
    end_date: str = "",
) -> None:
    asset = asset.upper()
    label = label.lower()

    # Step 1: Scan the Robinhood 1099 file for the specified asset
    robinhood_transactions = scan_robinhood_1099(robinhood1099_filepath, asset)

    # Step 2: Convert the scanned Robinhood transactions to Form 8949 transactions
    new_f8949_transactions = convert_robinhood_to_f8949_transactions(
        robinhood_transactions
    )

    # Step 3: Scan the existing Form 8949 file
    existing_f8949_transactions = scan_form_8949(form8949_filepath)

    # Step 4: Merge the existing Form 8949 transactions with the new transactions from the Robinhood 1099
    merged_f8949_transactions = merge_f8949_transactions(
        existing_f8949_transactions, new_f8949_transactions
    )

    formatted_transactions = format_datetime(merged_f8949_transactions)

    filtered_transactions = filter_transactions_by_date(
        formatted_transactions, start_date, end_date
    )

    # Step 5: Generate a CSV table from the merged transactions
    csv_table = get_f8949_csv_table(filtered_transactions)

    # Step 6 (optional): Sort the merged transactions by date
    sorted_csv_table = sort_csv(csv_table, column=2)

    # Step 7: Print and/or write the CSV table to a file
    print_csv(sorted_csv_table)
    write_csv(f"data/f1099/f1099-{label}.csv", sorted_csv_table)
