from pathlib import Path
from typing import Optional, Union

from archive.form8949.parser import filter_transactions_by_date, parse_f8949
from archive.form8949.scanner import (
    get_f8949_csv_table,
    scan_f8949_transactions,
)
from archive.tools.io import print_csv, write_csv


def process_f8949(
    file_path: Union[str, Path],
    label: str,
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
) -> None:
    f8949_transactions = scan_f8949_transactions(file_path)
    f8949_transactions = parse_f8949(f8949_transactions)

    f8949_transactions = filter_transactions_by_date(
        f8949_transactions, start_date, end_date
    )

    csv_f8949_transactions = get_f8949_csv_table(f8949_transactions)
    print_csv(csv_f8949_transactions)

    output_file_path = Path(f"data/out/form-8949-{label}.csv")
    write_csv(output_file_path, csv_f8949_transactions)
