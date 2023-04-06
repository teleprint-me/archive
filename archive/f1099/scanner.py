from pathlib import Path
from typing import Union

from archive.exchange.robinhood.models import RobinhoodTransaction
from archive.exchange.robinhood.parser import parse_robinhood
from archive.exchange.robinhood.scanner import scan_robinhood
from archive.f8949.models import F8949Transaction
from archive.f8949.scanner import get_f8949_transactions
from archive.tools.io import read_csv


def scan_robinhood_1099(
    filepath: Union[str, Path],
    asset: str,
) -> list[RobinhoodTransaction]:
    transactions = scan_robinhood(filepath)
    return parse_robinhood(transactions, [asset])


def scan_form_8949(filepath: Union[str, Path]) -> list[F8949Transaction]:
    csv_table = read_csv(filepath)
    return get_f8949_transactions(csv_table)
