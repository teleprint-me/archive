from pathlib import Path

from archive.coinbase_pro.models import (
    CoinbaseProColumns,
    CoinbaseProTransaction,
)
from archive.tools.io import read_csv


def get_coinbase_pro_transaction(csv_row: list[str]) -> CoinbaseProTransaction:
    total = float(csv_row[CoinbaseProColumns.TOTAL.value])
    return CoinbaseProTransaction(
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


def get_coinbase_pro_csv_row(
    coinbase_pro_transaction: CoinbaseProTransaction,
) -> list[str]:
    return [
        coinbase_pro_transaction.portfolio,
        str(coinbase_pro_transaction.trade_id),
        coinbase_pro_transaction.product,
        coinbase_pro_transaction.side,
        coinbase_pro_transaction.created_at,
        str(coinbase_pro_transaction.size),
        coinbase_pro_transaction.size_unit,
        str(coinbase_pro_transaction.price),
        str(coinbase_pro_transaction.fee),
        str(coinbase_pro_transaction.total),
        str(coinbase_pro_transaction.total_unit),
    ]


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
    for row in transactions:
        transaction = get_coinbase_pro_csv_row(row)
        csv_table.append(transaction)
    return csv_header + csv_table


def build_coinbase_pro_transactions(
    csv_table: list[list[str]],
) -> list[CoinbaseProTransaction]:
    transactions = []
    # omit the header from the conversion process
    for csv_row in csv_table[1:]:
        transaction = get_coinbase_pro_transaction(csv_row)
        transactions.append(transaction)
    return transactions


def scan_coinbase_pro(
    filepath: str | Path,
) -> list[CoinbaseProTransaction]:
    csv_table = read_csv(filepath)
    return build_coinbase_pro_transactions(csv_table)
