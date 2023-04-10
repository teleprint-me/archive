from typing import Optional

from archive.exchange.coinbase.models import CoinbaseTransaction
from archive.exchange.coinbase.parser import parse_coinbase
from archive.ir.models import IRTransaction


def build_coinbase_ir(
    transactions: list[CoinbaseTransaction],
    included_assets: list[str],
    excluded_types: Optional[list[str]] = None,
) -> list[IRTransaction]:
    ir_transactions = []

    if excluded_types is None:
        excluded_types = ["Send", "Receive"]

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
        # Format CoinbaseNote as a string.
        # Note Format: 'verb size base preposition determiner quote'
        note_parts = [
            transaction.notes.verb,
            transaction.notes.size,
            transaction.notes.base,
            transaction.notes.preposition,
            transaction.notes.determiner,
            transaction.notes.quote,
        ]

        filtered_note_parts = filter(str, note_parts)

        order_note = " ".join(filtered_note_parts)

        # Convert from CoinbaseTransaction to IRTransaction
        ir_transaction = IRTransaction(
            exchange="coinbase",
            product=transaction.currency_pair,
            datetime=transaction.timestamp,
            transaction_type=transaction.transaction_type,
            order_size=float(transaction.quantity),
            market_price=float(transaction.spot_price),
            order_fee=float(transaction.fees),
            order_note=order_note,
        )

        ir_transactions.append(ir_transaction)

    return ir_transactions
