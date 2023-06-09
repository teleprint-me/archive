from typing import Optional

from archive.exchange.coinbase_pro.models import CoinbaseProTransaction
from archive.exchange.coinbase_pro.parser import parse_coinbase_pro
from archive.ir.models import IRTransaction


def build_coinbase_pro_ir(
    transactions: list[CoinbaseProTransaction],
    included_assets: list[str],
    include_missing: Optional[bool] = True,
) -> list[IRTransaction]:
    ir_transactions = []

    parsed_transactions = parse_coinbase_pro(
        transactions, included_assets, include_missing
    )

    for transaction in parsed_transactions:
        ir_transaction = IRTransaction(
            exchange="coinbase_pro",
            product=transaction.product,
            datetime=transaction.created_at,
            transaction_type=transaction.side.capitalize(),
            order_size=float(transaction.size),
            market_price=float(transaction.price),
            order_fee=float(transaction.fee),
            order_note=transaction.notes,
        )

        ir_transactions.append(ir_transaction)

    return ir_transactions
