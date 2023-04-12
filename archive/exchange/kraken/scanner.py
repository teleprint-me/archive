from pathlib import Path

from archive.exchange.kraken.api import get_spot_price
from archive.exchange.kraken.models import (
    KrakenLedgerColumn,
    KrakenTradeColumn,
    KrakenTransaction,
    products,
)
from archive.tools.io import read_csv


# NOTE: This is experimental and only extracts staking tx's
def scan_kraken_ledgers(filepath: str | Path) -> list[KrakenTransaction]:
    """
    Parses a Kraken ledgers CSV file to extract staking transactions and returns a list of KrakenTransaction objects.

    Args:
        filepath: A string or Path object representing the path to the Kraken ledgers CSV file.

    Returns:
        A list of KrakenTransaction objects representing the parsed staking transactions.

    Raises
        KeyError: If the 'products' dictionary in 'archive/exchange/kraken/models.py' has an invalid format.

        ValueError: If an unknown product is encountered and needs to be added to the 'products' dictionary in 'archive/exchange/kraken/models.py'.
    """

    transactions = []
    csv_table = read_csv(filepath)

    # omit the header from the conversion process
    for csv_row in csv_table[1:]:
        transaction_type = csv_row[KrakenLedgerColumn.TYPE.value]

        if transaction_type == "staking":
            transaction_pair = ""

            transaction_vol = csv_row[KrakenLedgerColumn.AMOUNT.value]

            transaction_time = csv_row[KrakenLedgerColumn.TIME.value]

            # Extract symbol from "SYMBOL.S" pattern
            transaction_asset = csv_row[KrakenLedgerColumn.ASSET.value]
            transaction_asset = transaction_asset.split(".")[0]

            # Discover transaction pair
            for pair, product in products.items():
                try:
                    if transaction_asset == product.split("-")[0]:
                        transaction_pair = pair
                except IndexError:
                    raise KeyError(
                        f"Kraken: '{product}' is an invalid format. Please check the 'products' dictionary in 'archive/exchange/kraken/models.py'."
                    )

            # Quote may either be USD or ZUSD depending on product pair.
            #
            # NOTE: There's no finite way to determine which quote asset
            # to use due to poor implementation and a lack of a standard
            # format.
            if not transaction_pair:
                raise ValueError(
                    f"Kraken: '{transaction_asset}' is an unknown product. Please add it to the 'products' dictionary in 'archive/exchange/kraken/models.py'."
                )

            # NOTE: There is a potential issue with fetching spot prices
            # and results may be debatable.
            transaction_price = get_spot_price(
                transaction_pair, transaction_time
            )

            transaction = KrakenTransaction(
                txid="",
                order_txid=csv_row[KrakenLedgerColumn.REFID.value],
                pair=transaction_pair,
                time=transaction_time,
                type="buy",
                order_type=transaction_type,
                price=transaction_price,
                cost=0.00,
                fee=float(csv_row[KrakenLedgerColumn.FEE.value]),
                vol=float(transaction_vol),
                margin=0.00000000,
                misc="received",
                ledgers=csv_row[KrakenLedgerColumn.TXID.value],
                notes=f"Received {transaction_vol} {transaction_asset} from Kraken {transaction_type}",
            )

            transactions.append(transaction)

    return transactions


def scan_kraken_trades(
    filepath: str | Path,
) -> list[KrakenTransaction]:
    transactions = []
    csv_table = read_csv(filepath)

    # omit the header from the conversion process
    for csv_row in csv_table[1:]:
        transaction = KrakenTransaction(
            txid=csv_row[KrakenTradeColumn.TXID.value],
            order_txid=csv_row[KrakenTradeColumn.ORDER_TXID.value],
            pair=csv_row[KrakenTradeColumn.PAIR.value],
            time=csv_row[KrakenTradeColumn.TIME.value],
            type=csv_row[KrakenTradeColumn.TYPE.value],
            order_type=csv_row[KrakenTradeColumn.ORDER_TYPE.value],
            price=float(csv_row[KrakenTradeColumn.PRICE.value]),
            cost=float(csv_row[KrakenTradeColumn.COST.value]),
            fee=float(csv_row[KrakenTradeColumn.FEE.value]),
            vol=float(csv_row[KrakenTradeColumn.VOL.value]),
            margin=float(csv_row[KrakenTradeColumn.MARGIN.value]),
            misc=csv_row[KrakenTradeColumn.MISC.value],
            ledgers=csv_row[KrakenTradeColumn.LEDGERS.value],
        )

        transactions.append(transaction)

    return transactions
