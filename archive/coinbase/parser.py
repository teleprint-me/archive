from typing import Optional

from archive.coinbase.api import get_spot_price
from archive.coinbase.models import CoinbaseTransaction


def filter_transactions(
    transactions: list[CoinbaseTransaction],
    included_assets: list[str],
    excluded_types: Optional[list[str]] = None,
) -> list[CoinbaseTransaction]:
    """Filter transactions based on product and type.

    Args:
        transactions: A list of CoinbaseTransactions.
        included_products: A list of strings representing the desired products.
        excluded_types: A list of strings representing the excluded transaction types.

    Returns:
        A list of filtered CoinbaseTransaction's.
    """

    filtered_transactions = []

    for transaction in transactions:
        if excluded_types and transaction.should_skip(excluded_types):
            continue

        if transaction.should_keep(included_assets):
            filtered_transactions.append(transaction)

    return filtered_transactions


def get_missing_transaction(
    transaction: CoinbaseTransaction,
) -> CoinbaseTransaction:
    """Get missing transaction data for a specific CoinbaseTransaction.

    Args:
        transaction: A dataclass representing a CoinbaseTransaction.

    Returns:
        A CoinbaseTransaction derived from a CoinbaseNote.
    """

    asset = transaction.notes.quote  # base
    currency = transaction.currency  # quote
    product = f"{asset}-{currency}"  # base-quote
    response = get_spot_price(product, transaction.timestamp)
    spot_price = float(response["data"]["amount"])
    # fees = float(transaction.fees)
    quantity = float(transaction.notes.determiner)
    subtotal = spot_price * quantity
    # total = subtotal + fees
    return CoinbaseTransaction(
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

    # extract converted transactions
    for transaction in transactions:
        if transaction.transaction_type == "Convert":
            conversions.append(transaction)

    # extract missing transactions
    for convert in conversions:
        missing_transaction = get_missing_transaction(convert)
        missing_transactions.append(missing_transaction)

    return missing_transactions


def process_special_transactions(
    transactions: list[CoinbaseTransaction],
) -> list[CoinbaseTransaction]:
    transaction_types = [
        "CardBuyBack",
        "CardSpend",
        "Rewards Income",
        "Learning Reward",
    ]

    for transaction in transactions:
        if transaction.transaction_type in transaction_types:
            spot_price = float(transaction.spot_price)
            quantity = float(transaction.quantity)
            total = spot_price * quantity
            transaction.subtotal = "0.00"
            transaction.fees = "0.00"
            transaction.total = f"{total:.2f}"

    return transactions


def simplify_transaction_types(
    transactions: list[CoinbaseTransaction],
) -> list[CoinbaseTransaction]:
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

    for transaction in transactions:
        original_type = transaction.transaction_type

        if original_type in buy_types:
            transaction.transaction_type = "Buy"
        elif original_type in sell_types:
            transaction.transaction_type = "Sell"
        elif original_type in skip_types:
            continue
        else:
            raise ValueError(f"Unknown transaction type: {original_type}")

    return transactions


def parse_coinbase(
    transactions: list[CoinbaseTransaction],
    included_products: list[str],
    excluded_types: Optional[list[str]] = None,
    include_missing: Optional[bool] = True,
) -> list[CoinbaseTransaction]:
    """Get filtered transactions from CoinbaseTransaction's dataset.

    Args:
        transactions: A list of CoinbaseTransaction's.
        included_products: A list of strings representing the desired products.
        excluded_types: A list of strings representing the excluded transaction types.

    Returns:
        A list of filtered CoinbaseTransaction's.

    Notes:
        If 'convert' is not in the list of excluded types, this method also includes any missing transactions that are associated with a 'convert' transaction, which are labeled as 'Buy' in the output. This is because 'convert' is primarily an alternative to the 'sell' transaction type, and the missing transactions represent the currency bought in exchange for the one sold.
    """

    filtered_transactions = filter_transactions(
        transactions, included_products, excluded_types
    )

    if include_missing:
        missing_transactions = get_missing_transactions(filtered_transactions)
        filtered_transactions.extend(missing_transactions)

    processed_transactions = process_special_transactions(
        filtered_transactions
    )

    return simplify_transaction_types(processed_transactions)
