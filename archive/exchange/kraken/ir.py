from typing import Optional

from archive.exchange.kraken.models import KrakenTransaction
from archive.exchange.kraken.parser import parse_kraken
from archive.ir.models import IRTransaction


def build_kraken_ir(
    transactions: list[KrakenTransaction],
    included_assets: list[str],
    include_missing: Optional[bool] = True,
) -> list[IRTransaction]:
    """Build an IR from a list of KrakenTransaction's.

    Args:
        transactions: A list of KrakenTransaction's.
        included_assets: A list of strings representing the desired assets.
        include_missing: Include missing transactions in the IR.

    Returns:
        A list of IRTransaction's.
    """
    ir_transactions = []

    parsed_transactions = parse_kraken(
        transactions, included_assets, include_missing
    )

    for transaction in parsed_transactions:
        ir_transaction = IRTransaction(
            exchange="kraken",
            product=transaction.product,
            datetime=transaction.time,
            transaction_type=transaction.type.capitalize(),
            order_size=transaction.vol,
            market_price=transaction.price,
            order_fee=transaction.fee,
            order_note=transaction.notes,
        )

        ir_transactions.append(ir_transaction)

    return ir_transactions
