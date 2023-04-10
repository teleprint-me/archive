from typing import Optional

from archive.exchange.coinbase.api import get_spot_price
from archive.exchange.coinbase.models import CoinbaseTransaction


def get_missing_transactions(
    transactions: list[CoinbaseTransaction],
) -> list[CoinbaseTransaction]:
    """Get missing transaction dataset for coinbase transactions.

    Args:
        transactions: A list of CoinbaseTransaction's.

    Returns:
        A list of CoinbaseTransaction's derived from a CoinbaseNote's.
    """

    conversions = []
    missing_transactions = []

    # Extract converted transactions
    for transaction in transactions:
        if transaction.transaction_type == "Convert":
            conversions.append(transaction)

    # Extract missing transactions
    for transaction in conversions:
        asset = transaction.notes.quote  # base
        currency = transaction.currency  # quote
        product = f"{asset}-{currency}"  # base-quote
        spot_price = get_spot_price(product, transaction.timestamp)

        # fees = float(transaction.fees)
        quantity = float(transaction.notes.determiner)
        subtotal = spot_price * quantity

        # total = subtotal + fees
        missing_transaction = CoinbaseTransaction(
            timestamp=transaction.timestamp,
            transaction_type="Buy",
            asset=asset,
            quantity=f"{quantity:.8f}",
            currency=currency,
            spot_price=f"{spot_price:.2f}",
            subtotal="0.00",
            total=f"{subtotal:.2f}",
            fees="0.00",
            notes=transaction.notes,
        )

        missing_transactions.append(missing_transaction)

    return missing_transactions


def parse_coinbase(
    transactions: list[CoinbaseTransaction],
    included_assets: list[str],
    excluded_types: Optional[list[str]] = None,
    include_missing: Optional[bool] = True,
) -> list[CoinbaseTransaction]:
    """Get filtered transactions from CoinbaseTransaction's dataset.

    Args:
        transactions: A list of CoinbaseTransaction's.
        included_assets: A list of strings representing the desired products.
        excluded_types: A list of strings representing the excluded transaction types.

    Returns:
        A list of filtered CoinbaseTransaction's.

    Notes:
        If 'convert' is not in the list of excluded types, this method also includes any missing transactions that are associated with a 'convert' transaction, which are labeled as 'Buy' in the output. This is because 'convert' is primarily an alternative to the 'sell' transaction type, and the missing transactions represent the currency bought in exchange for the one sold.
    """

    processed_transactions = []

    buy_types = [
        "Advanced Trade Buy",
        "Buy",
        "CardBuyBack",
        "Learning Reward",
        "Rewards Income",
    ]

    sell_types = [
        "Advanced Trade Sell",
        "CardSpend",
        "Convert",
        "Sell",
    ]

    skip_types = [
        "Send",
        "Receive",
    ]

    transaction_types = [
        "CardBuyBack",
        "CardSpend",
        "Rewards Income",
        "Learning Reward",
    ]

    # Filter transactions by asset and type
    for transaction in transactions:
        # Exclude user selected transaction types
        if excluded_types and transaction.should_skip(excluded_types):
            continue

        # Include user selected assets
        if transaction.should_keep(included_assets):
            processed_transactions.append(transaction)

    # Fetch and build crypto-to-crypto transactions
    if include_missing:
        missing_transactions = get_missing_transactions(processed_transactions)
        processed_transactions.extend(missing_transactions)

    # Process special transactions
    for transaction in processed_transactions:
        if transaction.transaction_type in transaction_types:
            spot_price = float(transaction.spot_price)
            quantity = float(transaction.quantity)
            total = spot_price * quantity
            transaction.subtotal = "0.00"
            transaction.fees = "0.00"
            transaction.total = f"{total:.2f}"

    # Simplify transaction types
    for transaction in processed_transactions:
        original_type = transaction.transaction_type

        if original_type in buy_types:
            transaction.transaction_type = "Buy"
        elif original_type in sell_types:
            transaction.transaction_type = "Sell"
        elif original_type in skip_types:
            continue
        else:
            raise ValueError(f"Unknown transaction type: {original_type}")

    return processed_transactions
