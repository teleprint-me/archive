from pathlib import Path
from typing import Union

from archive.ir.builder import build_ir_csv
from archive.ir.config import exchanges
from archive.ir.models import IRTransaction
from archive.tools.io import print_csv, write_csv
from archive.tools.sort import sort_csv


def process_ir(
    asset: str, label: str, exchange: str, file_path: Union[str, Path]
) -> None:
    asset = asset.upper()
    label = label.lower()
    exchange = exchange.lower()

    scan_transactions = exchanges[exchange]["scan"]
    build_ir = exchanges[exchange]["build_ir"]

    transactions = scan_transactions(file_path)

    if exchange in ["coinbase", "coinbase_pro", "kraken"]:
        ir_transactions = build_ir(transactions, [asset])
    else:
        raise ValueError(f"Invalid exchange {exchange}")

    csv_ir_transactions = build_ir_csv(ir_transactions)
    csv_sorted = sort_csv(csv_ir_transactions, column=2)
    print_csv(csv_sorted)

    output_file_path = Path(f"data/ir/ir-{exchange}-{label}.csv")
    write_csv(output_file_path, csv_sorted)
