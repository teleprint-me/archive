from datetime import datetime
from pathlib import Path
from typing import Union

from archive.f8949.models import F8949Columns
from archive.f8949.scanner import get_f8949_csv_table
from archive.link.parser import (
    filter_transactions_by_year,
    link_f8949_transactions,
    remove_duplicate_transactions,
)
from archive.tools.io import print_csv, write_csv
from archive.tools.sort import sort_csv


def process_form_link(
    f8949_directory: Union[str, Path],
    f1099_directory: Union[str, Path, None] = None,
    year: str = "",
    label: str = "",
) -> None:
    if not year:
        current_year = datetime.now().year
        year = str(current_year - 1)

    if label:
        filepath = f"data/form-8949-{year}-{label}.csv"
    else:
        filepath = f"data/form-8949-{year}.csv"

    # Step 1: Read all Form-8949 and Form-1099 CSV files and combine their data
    f8949_transactions = link_f8949_transactions(f8949_directory)

    if f1099_directory is not None:
        f1099_transactions = link_f8949_transactions(f1099_directory)
        f8949_transactions.extend(f1099_transactions)

    linked_transactions = remove_duplicate_transactions(f8949_transactions)

    # Step 2: Filter transactions by the given year
    filtered_transactions = filter_transactions_by_year(
        linked_transactions, year
    )

    # Step 3: Sort the transactions by date
    csv_table = get_f8949_csv_table(filtered_transactions)
    sorted_csv = sort_csv(csv_table, column=F8949Columns.DATE_SOLD.value)

    # Step 4: Print and write the CSV table to a file
    print_csv(sorted_csv)
    write_csv(filepath, sorted_csv)
