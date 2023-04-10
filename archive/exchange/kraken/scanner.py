from pathlib import Path

from archive.exchange.kraken.models import KrakenColumns, KrakenTransaction
from archive.tools.io import read_csv


def scan_kraken_trades(
    filepath: str | Path,
) -> list[KrakenTransaction]:
    transactions = []
    csv_table = read_csv(filepath)

    # omit the header from the conversion process
    for csv_row in csv_table[1:]:
        transaction = KrakenTransaction(
            txid=csv_row[KrakenColumns.TXID.value],
            order_txid=csv_row[KrakenColumns.ORDER_TXID.value],
            pair=csv_row[KrakenColumns.PAIR.value],
            time=csv_row[KrakenColumns.TIME.value],
            type=csv_row[KrakenColumns.TYPE.value],
            order_type=csv_row[KrakenColumns.ORDER_TYPE.value],
            price=float(csv_row[KrakenColumns.PRICE.value]),
            cost=float(csv_row[KrakenColumns.COST.value]),
            fee=float(csv_row[KrakenColumns.FEE.value]),
            vol=float(csv_row[KrakenColumns.VOL.value]),
            margin=float(csv_row[KrakenColumns.MARGIN.value]),
            misc=csv_row[KrakenColumns.MISC.value],
            ledgers=csv_row[KrakenColumns.LEDGERS.value],
        )

        transactions.append(transaction)

    return transactions
