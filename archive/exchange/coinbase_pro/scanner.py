from pathlib import Path

from archive.exchange.coinbase_pro.models import (
    CoinbaseProColumns,
    CoinbaseProTransaction,
)
from archive.tools.io import read_csv


def build_coinbase_pro_csv(
    transactions: list[CoinbaseProTransaction],
) -> list[list[str]]:
    # include the header in the conversion process
    csv_header = [
        [
            "portfolio",
            "trade id",
            "product",
            "side",
            "created at",
            "size",
            "size unit",
            "price",
            "fee",
            "total",
            "price/fee/total unit",
        ]
    ]
    csv_table = []
    for tx in transactions:
        transaction = [
            tx.portfolio,
            str(tx.trade_id),
            tx.product,
            tx.side,
            tx.created_at,
            str(tx.size),
            tx.size_unit,
            str(tx.price),
            str(tx.fee),
            str(tx.total),
            str(tx.total_unit),
        ]
        csv_table.append(transaction)
    return csv_header + csv_table


def build_coinbase_pro_transactions(
    csv_table: list[list[str]],
) -> list[CoinbaseProTransaction]:
    transactions = []
    # omit the header from the conversion process
    for csv_row in csv_table[1:]:
        total = float(csv_row[CoinbaseProColumns.TOTAL.value])
        transaction = CoinbaseProTransaction(
            portfolio=csv_row[CoinbaseProColumns.PORTFOLIO.value],
            trade_id=int(csv_row[CoinbaseProColumns.TRADE_ID.value]),
            product=csv_row[CoinbaseProColumns.PRODUCT.value],
            side=csv_row[CoinbaseProColumns.SIDE.value],
            created_at=csv_row[CoinbaseProColumns.CREATED_AT.value],
            size=float(csv_row[CoinbaseProColumns.SIZE.value]),
            size_unit=csv_row[CoinbaseProColumns.SIZE_UNIT.value],
            price=float(csv_row[CoinbaseProColumns.PRICE.value]),
            fee=float(csv_row[CoinbaseProColumns.FEE.value]),
            total=total if total > 0 else -total,
            total_unit=csv_row[CoinbaseProColumns.TOTAL_UNIT.value],
        )
        transactions.append(transaction)
    return transactions


def scan_coinbase_pro_fills(
    filepath: str | Path,
) -> list[CoinbaseProTransaction]:
    csv_table = read_csv(filepath)
    return build_coinbase_pro_transactions(csv_table)
