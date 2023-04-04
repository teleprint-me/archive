from pathlib import Path

from archive.kraken.models import KrakenColumns, KrakenTransaction
from archive.tools.io import read_csv


def get_kraken_transaction(csv_row: list[str]) -> KrakenTransaction:
    # Parse the row into a new KrakenTransaction instance
    return KrakenTransaction(
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


def get_kraken_csv_row(
    kraken_transaction: KrakenTransaction,
) -> list[str]:
    return [
        kraken_transaction.txid,
        str(kraken_transaction.order_txid),
        kraken_transaction.pair,
        kraken_transaction.time,
        kraken_transaction.type,
        kraken_transaction.order_type,
        str(kraken_transaction.price),
        str(kraken_transaction.cost),
        str(kraken_transaction.fee),
        str(kraken_transaction.vol),
        str(kraken_transaction.margin),
        kraken_transaction.misc,
        kraken_transaction.ledgers,
    ]


def build_kraken_csv(
    transactions: list[KrakenTransaction],
) -> list[list[str]]:
    # include the header in the conversion process
    csv_header = [
        [
            "txid",
            "ordertxid",
            "pair",
            "time",
            "type",
            "ordertype",
            "price",
            "cost",
            "fee",
            "vol",
            "margin",
            "misc",
            "ledgers",
        ]
    ]
    csv_table = []
    for row in transactions:
        transaction = get_kraken_csv_row(row)
        csv_table.append(transaction)
    return csv_header + csv_table


def build_kraken_transactions(
    csv_table: list[list[str]],
) -> list[KrakenTransaction]:
    transactions = []
    # omit the header from the conversion process
    for csv_row in csv_table[1:]:
        transaction = get_kraken_transaction(csv_row)
        transactions.append(transaction)
    return transactions


def scan_kraken(
    filepath: str | Path,
) -> list[KrakenTransaction]:
    csv_table = read_csv(filepath)
    return build_kraken_transactions(csv_table)
