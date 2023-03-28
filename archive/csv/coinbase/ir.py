from typing import Optional

from archive.csv.coinbase.parser import parse_coinbase
from archive.csv.coinbase.scanner.builder import get_coinbase_note_as_string
from archive.csv.coinbase.scanner.transaction import CoinbaseTransaction
from archive.csv.ir.transaction import IRTransaction


def get_coinbase_ir_list(
    transactions: list[CoinbaseTransaction],
    included_assets: list[str],
    excluded_types: Optional[list[str]] = None,
) -> list[IRTransaction]:
    ir_transactions = []

    if excluded_types and "Convert" in excluded_types:
        selected_transactions = parse_coinbase(
            transactions,
            included_assets,
            excluded_types,
            include_missing=False,
        )
    else:
        selected_transactions = parse_coinbase(
            transactions, included_assets, excluded_types
        )

    for tx in selected_transactions:
        ir_transaction = IRTransaction(
            exchange="coinbase",
            product=tx.currency_pair,
            datetime=tx.timestamp,
            transaction_type=tx.transaction_type,
            order_size=float(tx.quantity),
            market_price=float(tx.spot_price),
            order_fee=float(tx.fees),
            order_note=get_coinbase_note_as_string(tx.notes),
        )
        ir_transactions.append(ir_transaction)

    return ir_transactions
