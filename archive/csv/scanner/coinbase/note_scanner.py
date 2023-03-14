from archive.csv.coinbase.note import CoinbaseNote


class CoinbaseNoteScanner:
    """Class for building Coinbase transaction notes.

    This class takes a row from a Coinbase CSV file, which contains information about a transaction, and converts it into a CoinbaseNote object.
    """

    def __init__(self, row: list[str]):
        """Create a CoinbaseNoteBuilder instance.

        Args:
            row: A list of strings representing a row from a Coinbase CSV file.
        """
        self.timestamp = row[0]
        self.transaction_type = row[1]
        self.asset = row[2]
        self.quantity = float(row[3])
        self.price_currency = row[4]
        self.price = float(row[5])
        self.subtotal = float(row[6])
        self.total = float(row[7])
        self.fees = float(row[8])
        self.notes = row[9]

    def scan(self) -> CoinbaseNote:
        """Build a CoinbaseNote object based on the notes field.

        Returns:
            CoinbaseNote: A CoinbaseNote object representing the transaction.
        """
        note_parts = self.notes.split(" ")
        determiner = note_parts[0]
        verb = note_parts[1].lower() if len(note_parts) > 1 else None
        if verb == "sent":
            address = note_parts[-1]
            return CoinbaseNote(
                determiner=determiner,
                verb=verb,
                asset=self.asset,
                quantity=self.quantity,
                price_currency=self.price_currency,
                price=self.price,
                subtotal=self.subtotal,
                total=self.total,
                fees=self.fees,
                address=address,
                transaction_type=self.transaction_type,
            )
        elif verb in ["bought", "sold", "converted"]:
            size = float(note_parts[2])
            base = note_parts[3]
            preposition = note_parts[4]
            quote = note_parts[5]
            return CoinbaseNote(
                determiner=determiner,
                verb=verb,
                size=size,
                base=base,
                preposition=preposition,
                quote=quote,
                asset=self.asset,
                quantity=self.quantity,
                price_currency=self.price_currency,
                price=self.price,
                subtotal=self.subtotal,
                total=self.total,
                fees=self.fees,
                transaction_type=self.transaction_type,
            )
        else:
            description = " ".join(note_parts[1:])
            return CoinbaseNote(
                determiner=determiner,
                asset=self.asset,
                quantity=self.quantity,
                price_currency=self.price_currency,
                price=self.price,
                subtotal=self.subtotal,
                total=self.total,
                fees=self.fees,
                description=description,
                transaction_type=self.transaction_type,
            )
