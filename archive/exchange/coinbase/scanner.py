from pathlib import Path

from archive.exchange.coinbase.models import (
    CoinbaseColumn,
    CoinbaseNote,
    CoinbaseNoteColumn,
    CoinbaseTransaction,
)
from archive.tools.io import read_csv


def csv_row_to_coinbase_note(csv_row: list[str]) -> CoinbaseNote:
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
    notes = csv_row[CoinbaseColumn.NOTES.value].split(" ")
    product = csv_row[CoinbaseColumn.ASSET.value]
    transaction_type = csv_row[CoinbaseColumn.TRANSACTION_TYPE.value]

    # Address Grammar
    #   - Description: The `Address Grammar` always consists of a single token.
    #   - Grammar: `DETERMINER`
    #   - Sample: "xxxxxxxxxxxxxxxxxxxx68dd"
    if len(notes) == 1:
        return CoinbaseNote(
            determiner=notes[CoinbaseNoteColumn.VERB.value],
            product=product,
            transaction_type=transaction_type,
        )

    # Trade Grammar
    #   - Description: The `Trade Grammar` always consists of 6 tokens.
    #   - Grammar: `VERB SIZE BASE PREPOSITION DETERMINER QUOTE`
    #   - Sample: "Bought 0.00094589 BTC for $10.00 USD"
    if notes[CoinbaseNoteColumn.VERB.value] in [
        "Bought",
        "Sold",
        "Converted",
    ]:
        return CoinbaseNote(
            verb=notes[CoinbaseNoteColumn.VERB.value],
            size=notes[CoinbaseNoteColumn.SIZE.value],
            base=notes[CoinbaseNoteColumn.BASE.value],
            preposition=notes[CoinbaseNoteColumn.PREPOSITION.value],
            determiner=notes[CoinbaseNoteColumn.DETERMINER.value],
            quote=notes[CoinbaseNoteColumn.QUOTE.value],
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
        verb=notes[CoinbaseNoteColumn.VERB.value],
        size=notes[CoinbaseNoteColumn.SIZE.value],
        base=notes[CoinbaseNoteColumn.BASE.value],
        preposition=notes[CoinbaseNoteColumn.PREPOSITION.value],
        determiner=" ".join(notes[CoinbaseNoteColumn.DETERMINER.value :]),
        product=product,
        transaction_type=transaction_type,
    )


def scan_coinbase_transactions(
    filepath: str | Path,
) -> list[CoinbaseTransaction]:
    """Scan the CSV file and extract Coinbase transaction data."""
    transactions = []
    csv_table = read_csv(filepath)

    # omit the header from the conversion process
    for csv_row in csv_table[1:]:
        transaction = CoinbaseTransaction(
            timestamp=csv_row[CoinbaseColumn.TIMESTAMP.value],
            transaction_type=csv_row[CoinbaseColumn.TRANSACTION_TYPE.value],
            asset=csv_row[CoinbaseColumn.ASSET.value],
            quantity=csv_row[CoinbaseColumn.QUANTITY.value],
            currency=csv_row[CoinbaseColumn.CURRENCY.value],
            spot_price=csv_row[CoinbaseColumn.SPOT_PRICE.value],
            subtotal=csv_row[CoinbaseColumn.SUBTOTAL.value],
            total=csv_row[CoinbaseColumn.TOTAL.value],
            fees=csv_row[CoinbaseColumn.FEES.value],
            notes=csv_row_to_coinbase_note(csv_row),
        )

        transactions.append(transaction)

    return transactions
