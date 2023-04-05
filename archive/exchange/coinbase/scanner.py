from pathlib import Path

from archive.exchange.coinbase.models import (
    CoinbaseColumns,
    CoinbaseTransaction,
)
from archive.exchange.coinbase.note import CoinbaseNote, CoinbaseNoteColumns
from archive.tools.io import read_csv


def get_coinbase_note(csv_row: list[str]) -> CoinbaseNote:
    """Create a CoinbaseNote instance from a note string.

    Args:
        notes: A string representing a Coinbase transaction note.
        product: The asset being transacted (e.g. "BTC").
        transaction_type: The type of transaction (e.g. "buy").

    Returns:
        A CoinbaseNote instance.
    """
    # Extract "Notes", "Asset", and "Transaction Type" from the given
    # transaction record.
    notes = csv_row[CoinbaseColumns.NOTES.value].split(" ")
    product = csv_row[CoinbaseColumns.ASSET.value]
    transaction_type = csv_row[CoinbaseColumns.TRANSACTION_TYPE.value]

    # Address Grammar
    #   - Description: The `Address Grammar` always consists of a single token.
    #   - Grammar: `DETERMINER`
    #   - Sample: "xxxxxxxxxxxxxxxxxxxx68dd"
    if len(notes) == 1:
        return CoinbaseNote(
            determiner=notes[CoinbaseNoteColumns.VERB.value],
            product=product,
            transaction_type=transaction_type,
        )

    # Trade Grammar
    #   - Description: The `Trade Grammar` always consists of 6 tokens.
    #   - Grammar: `VERB SIZE BASE PREPOSITION DETERMINER QUOTE`
    #   - Sample: "Bought 0.00094589 BTC for $10.00 USD"
    if notes[CoinbaseNoteColumns.VERB.value] in [
        "Bought",
        "Sold",
        "Converted",
    ]:
        return CoinbaseNote(
            verb=notes[CoinbaseNoteColumns.VERB.value],
            size=notes[CoinbaseNoteColumns.SIZE.value],
            base=notes[CoinbaseNoteColumns.BASE.value],
            preposition=notes[CoinbaseNoteColumns.PREPOSITION.value],
            determiner=notes[CoinbaseNoteColumns.DETERMINER.value],
            quote=notes[CoinbaseNoteColumns.QUOTE.value],
            product=product,
            transaction_type=transaction_type,
        )

    # Transaction Grammar
    #   - Description: The `Transaction Grammar` always consists of 5 or more tokens;
    #                  The number of `DETERMINER` tokens is unknown in advance and they
    #                  are merged into a single token.
    #   - Grammar: `VERB SIZE BASE PREPOSITION DETERMINER`
    #   - Sample: "Sent 0.00188372 BTC to xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx7Qih"
    return CoinbaseNote(
        verb=notes[CoinbaseNoteColumns.VERB.value],
        size=notes[CoinbaseNoteColumns.SIZE.value],
        base=notes[CoinbaseNoteColumns.BASE.value],
        preposition=notes[CoinbaseNoteColumns.PREPOSITION.value],
        determiner=" ".join(notes[CoinbaseNoteColumns.DETERMINER.value :]),
        product=product,
        transaction_type=transaction_type,
    )


def get_coinbase_note_as_string(coinbase_note: CoinbaseNote) -> str:
    """Return the note as a string in the format 'verb size base preposition determiner quote'"""
    note_parts = [
        coinbase_note.verb,
        coinbase_note.size,
        coinbase_note.base,
        coinbase_note.preposition,
        coinbase_note.determiner,
        coinbase_note.quote,
    ]
    filtered_note_parts = filter(str, note_parts)
    return " ".join(filtered_note_parts)


def get_coinbase_transaction(csv_row: list[str]) -> CoinbaseTransaction:
    """Build a CoinbaseTransaction from a CSV row and a notes row.

    Args:
        csv_row: A list representing a row from a Coinbase CSV file.

    Returns:
        CoinbaseTransaction: A CoinbaseTransaction object representing the transaction.
    """
    return CoinbaseTransaction(
        timestamp=csv_row[CoinbaseColumns.TIMESTAMP.value],
        transaction_type=csv_row[CoinbaseColumns.TRANSACTION_TYPE.value],
        asset=csv_row[CoinbaseColumns.ASSET.value],
        quantity=csv_row[CoinbaseColumns.QUANTITY.value],
        currency=csv_row[CoinbaseColumns.CURRENCY.value],
        spot_price=csv_row[CoinbaseColumns.SPOT_PRICE.value],
        subtotal=csv_row[CoinbaseColumns.SUBTOTAL.value],
        total=csv_row[CoinbaseColumns.TOTAL.value],
        fees=csv_row[CoinbaseColumns.FEES.value],
        notes=get_coinbase_note(csv_row),
    )


def get_coinbase_csv_row(
    coinbase_transaction: CoinbaseTransaction,
) -> list[str]:
    return [
        coinbase_transaction.timestamp,
        coinbase_transaction.transaction_type,
        coinbase_transaction.asset,
        f"{float(coinbase_transaction.quantity):.8f}",
        coinbase_transaction.currency,
        f"{float(coinbase_transaction.spot_price):.2f}",
        f"{float(coinbase_transaction.subtotal):.2f}",
        f"{float(coinbase_transaction.total):.2f}",
        f"{float(coinbase_transaction.fees):.2f}",
        get_coinbase_note_as_string(coinbase_transaction.notes),
    ]


def build_coinbase_csv(
    transactions: list[CoinbaseTransaction],
) -> list[list[str]]:
    # include the header in the conversion process
    csv_header = [
        [
            "Timestamp",
            "Transaction Type",
            "Asset",
            "Quantity Transacted",
            "Spot Price Currency",
            "Spot Price at Transaction",
            "Subtotal",
            "Total (inclusive of fees and/or spread)",
            "Fees and/or Spread",
            "Notes",
        ]
    ]
    csv_table = []
    for row in transactions:
        transaction = get_coinbase_csv_row(row)
        csv_table.append(transaction)
    return csv_header + csv_table


def build_coinbase_transactions(
    csv_table: list[list[str]],
) -> list[CoinbaseTransaction]:
    transactions = []
    # omit the header from the conversion process
    for csv_row in csv_table[1:]:
        transaction = get_coinbase_transaction(csv_row)
        transactions.append(transaction)
    return transactions


def scan_coinbase(
    filepath: str | Path,
) -> list[CoinbaseTransaction]:
    """Scan the CSV file and extract Coinbase transaction data."""
    csv_table = read_csv(filepath)
    return build_coinbase_transactions(csv_table)
