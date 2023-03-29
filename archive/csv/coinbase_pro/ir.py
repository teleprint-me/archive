from typing import Optional

from archive.csv.coinbase_pro.parser import parse_coinbase_pro
from archive.csv.coinbase_pro.transaction import CoinbaseProTransaction
from archive.csv.ir.transaction import IRTransaction


def get_coinbase_pro_ir_row(
    transaction: CoinbaseProTransaction,
) -> IRTransaction:
    return IRTransaction(
        exchange="coinbase",
        product=transaction.product,
        datetime=transaction.created_at,
        transaction_type=transaction.side,
        order_size=float(transaction.size),
        market_price=float(transaction.price),
        order_fee=float(transaction.fee),
        order_note=transaction.notes,
    )


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
        ir_transaction = get_coinbase_pro_ir_row(transaction)
        ir_transactions.append(ir_transaction)

    return ir_transactions
