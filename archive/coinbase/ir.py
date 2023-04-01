from typing import Optional

from archive.coinbase.parser import parse_coinbase
from archive.coinbase.scanner import get_coinbase_note_as_string
from archive.coinbase.transaction import CoinbaseTransaction
from archive.ir.transaction import IRTransaction


def get_coinbase_ir_row(
    transaction: CoinbaseTransaction,
) -> IRTransaction:
    return IRTransaction(
        exchange="coinbase",
        product=transaction.currency_pair,
        datetime=transaction.timestamp,
        transaction_type=transaction.transaction_type,
        order_size=float(transaction.quantity),
        market_price=float(transaction.spot_price),
        order_fee=float(transaction.fees),
        order_note=get_coinbase_note_as_string(transaction.notes),
    )


def build_coinbase_ir(
    transactions: list[CoinbaseTransaction],
    included_assets: list[str],
    excluded_types: Optional[list[str]] = None,
) -> list[IRTransaction]:
    ir_transactions = []

    if excluded_types and "Convert" in excluded_types:
        parsed_transactions = parse_coinbase(
            transactions,
            included_assets,
            excluded_types,
            include_missing=False,
        )
    else:
        parsed_transactions = parse_coinbase(
            transactions, included_assets, excluded_types
        )

    for transaction in parsed_transactions:
        ir_transaction = get_coinbase_ir_row(transaction)
        ir_transactions.append(ir_transaction)

    return ir_transactions
