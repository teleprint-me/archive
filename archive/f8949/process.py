from pathlib import Path
from typing import Optional, Union

from archive.f8949.parser import (
    filter_transactions_by_date,
    format_datetime,
    parse_f8949,
)
from archive.f8949.scanner import get_f8949_csv_table, scan_f8949_transactions
from archive.tools.io import print_csv, write_csv


def process_f8949(
    file_path: Union[str, Path],
    label: str,
    output_dir: Union[str, Path],
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
) -> Union[str, Path]:
    # Format user input
    label = label.lower()

    scanned_transactions = scan_f8949_transactions(file_path)
    filtered_transactions = filter_transactions_by_date(
        scanned_transactions, start_date, end_date
    )
    parsed_transactions = parse_f8949(filtered_transactions)
    formatted_transactions = format_datetime(parsed_transactions)

    csv_f8949_transactions = get_f8949_csv_table(formatted_transactions)
    print_csv(csv_f8949_transactions)

    output_file_path = Path(output_dir, f"f8949-{label}.csv")
    write_csv(output_file_path, csv_f8949_transactions)

    return output_file_path
