from pathlib import Path

from archive.exchange.coinbase_pro.models import (
    CoinbaseProAccountColumn,
    CoinbaseProFillColumn,
    CoinbaseProTransaction,
)
from archive.tools.io import read_csv


def scan_coinbase_pro_accounts(
    filepath: str | Path,
) -> list[CoinbaseProTransaction]:
    transactions: list[CoinbaseProTransaction] = []
    csv_table: list[list[str]] = read_csv(filepath)

    # Omit the header from the conversion process
    for idx in range(1, len(csv_table), 2):
        row1 = csv_table[idx]
        row2 = csv_table[idx + 1]

        # Check if both rows have the same timestamp and are of type "conversion"
        if (
            row1[CoinbaseProAccountColumn.TYPE.value] == "conversion"
            and row2[CoinbaseProAccountColumn.TYPE.value] == "conversion"
            and row1[CoinbaseProAccountColumn.TIME.value]
            == row2[CoinbaseProAccountColumn.TIME.value]
        ):
            amount1 = float(row1[CoinbaseProAccountColumn.AMOUNT.value])
            amount2 = float(row2[CoinbaseProAccountColumn.AMOUNT.value])

            side = "buy" if amount1 < 0 else "sell"
            size, size_unit = (
                (abs(amount1), row1[CoinbaseProAccountColumn.UNIT.value])
                if amount1 < 0
                else (abs(amount2), row2[CoinbaseProAccountColumn.UNIT.value])
            )
            total, total_unit = (
                (abs(amount2), row2[CoinbaseProAccountColumn.UNIT.value])
                if amount1 < 0
                else (abs(amount1), row1[CoinbaseProAccountColumn.UNIT.value])
            )

            transaction = CoinbaseProTransaction(
                portfolio=row1[CoinbaseProAccountColumn.PORTFOLIO.value],
                trade_id=0,
                product=f"{size_unit}-{total_unit}",
                side=side,
                created_at=row1[CoinbaseProAccountColumn.TIME.value],
                size=size,
                size_unit=size_unit,
                price=1,
                fee=0,
                total=total,
                total_unit=total_unit,
                notes=f"Converted from {abs(amount1)} {row1[CoinbaseProAccountColumn.UNIT.value]} to {abs(amount2)} {row2[CoinbaseProAccountColumn.UNIT.value]}",
            )

            transactions.append(transaction)

    return transactions


def scan_coinbase_pro_fills(
    filepath: str | Path,
) -> list[CoinbaseProTransaction]:
    transactions: list[CoinbaseProTransaction] = []
    csv_table: list[list[str]] = read_csv(filepath)

    # omit the header from the conversion process
    for csv_row in csv_table[1:]:
        total = float(csv_row[CoinbaseProFillColumn.TOTAL.value])

        transaction = CoinbaseProTransaction(
            portfolio=csv_row[CoinbaseProFillColumn.PORTFOLIO.value],
            trade_id=int(csv_row[CoinbaseProFillColumn.TRADE_ID.value]),
            product=csv_row[CoinbaseProFillColumn.PRODUCT.value],
            side=csv_row[CoinbaseProFillColumn.SIDE.value],
            created_at=csv_row[CoinbaseProFillColumn.CREATED_AT.value],
            size=float(csv_row[CoinbaseProFillColumn.SIZE.value]),
            size_unit=csv_row[CoinbaseProFillColumn.SIZE_UNIT.value],
            price=float(csv_row[CoinbaseProFillColumn.PRICE.value]),
            fee=float(csv_row[CoinbaseProFillColumn.FEE.value]),
            total=total if total > 0 else -total,
            total_unit=csv_row[CoinbaseProFillColumn.TOTAL_UNIT.value],
        )

        transactions.append(transaction)

    return transactions
