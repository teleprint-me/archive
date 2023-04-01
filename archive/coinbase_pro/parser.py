from typing import Optional

from archive.coinbase.api import get_spot_price
from archive.coinbase_pro.transaction import CoinbaseProTransaction


def filter_transactions(
    transactions: list[CoinbaseProTransaction],
    included_assets: list[str],
) -> list[CoinbaseProTransaction]:
    """Filter transactions based on product.

    Args:
        transactions: A list of CoinbaseProTransactions.
        included_products: A list of strings representing the desired products.

    Returns
        A list of filtered CoinbaseProTransaction's.
    """

    filtered_transactions = []

    for transaction in transactions:
        if transaction.should_keep(included_assets):
            filtered_transactions.append(transaction)

    return filtered_transactions


def get_missing_transaction(
    transaction: CoinbaseProTransaction,
) -> tuple[CoinbaseProTransaction, CoinbaseProTransaction]:
    """Get missing transaction data for the given crypto-to-crypto transaction.

    Args:
        transaction: A CoinbaseProTransaction instance.

    Returns:
        A 2-tuple containing missing CoinbaseProTransaction's.
    """

    # 1. Determine the Product, Base Product, and Quote Product
    base_product = f"{transaction.base}-USD"
    quote_product = f"{transaction.quote}-USD"

    # 2. Determine Market Price for both Base and Quote Products
    base_response = get_spot_price(base_product, transaction.created_at)
    quote_response = get_spot_price(quote_product, transaction.created_at)
    # Extract the market price from the responses
    base_price = float(base_response["data"]["amount"])
    quote_price = float(quote_response["data"]["amount"])

    # 3. Determine the Transaction Total for both Base and Quote Products
    base_total = base_price * transaction.size
    quote_total = quote_price * transaction.total

    # 4. Determine the Transaction Fee for both Base and Quote Products
    quote_fee = quote_price * transaction.fee
    base_fee = 0.0

    # 5. Get the order size for the Base and Quote Products
    base_size = transaction.size
    quote_size = transaction.total

    missing_buy_notes = (
        f"Bought {base_size:.8f} {transaction.base} "
        f"with {quote_size:.8f} {transaction.quote}"
    )

    missing_sell_notes = (
        f"Sold {base_size:.8f} {transaction.base} "
        f"for {quote_size:.8f} {transaction.quote}"
    )

    # 6. Create CoinbaseProTransaction for the missing BUY or SELL side
    if transaction.side == "BUY":
        # BUY side is missing selling the quote product for fiat
        # and buying the base product with fiat
        missing_sell = CoinbaseProTransaction(
            portfolio=transaction.portfolio,
            trade_id=transaction.trade_id,
            product=quote_product,
            side="SELL",
            created_at=transaction.created_at,
            size=quote_size,
            size_unit=transaction.total_unit,
            price=quote_price,
            fee=quote_fee,
            total=quote_total,
            total_unit="USD",
            notes=missing_sell_notes,
        )
        missing_buy = CoinbaseProTransaction(
            portfolio=transaction.portfolio,
            trade_id=transaction.trade_id,
            product=base_product,
            side="BUY",
            created_at=transaction.created_at,
            size=base_size,
            size_unit=transaction.size_unit,
            price=base_price,
            fee=base_fee,
            total=base_total,
            total_unit="USD",
            notes=missing_buy_notes,
        )
    elif transaction.side == "SELL":
        # SELL side is missing selling the base product for fiat
        # and buying the quote product with fiat
        missing_sell = CoinbaseProTransaction(
            portfolio=transaction.portfolio,
            trade_id=transaction.trade_id,
            product=base_product,
            side="SELL",
            created_at=transaction.created_at,
            size=base_size,
            size_unit=transaction.size_unit,
            price=base_price,
            fee=base_fee,
            total=base_total,
            total_unit="USD",
            notes=missing_sell_notes,
        )
        missing_buy = CoinbaseProTransaction(
            portfolio=transaction.portfolio,
            trade_id=transaction.trade_id,
            product=quote_product,
            side="BUY",
            created_at=transaction.created_at,
            size=quote_size,
            size_unit=transaction.total_unit,
            price=quote_price,
            fee=quote_fee,
            total=quote_total,
            total_unit="USD",
            notes=missing_buy_notes,
        )
    else:
        raise ValueError(f"Invalid side {transaction.side}")

    return missing_sell, missing_buy


def get_missing_transactions(
    transactions: list[CoinbaseProTransaction],
) -> list[CoinbaseProTransaction]:
    """Get missing transaction dataset for Coinbase Pro transactions.

    Args:
        transactions: A list of CoinbaseProTransaction's.

    Returns:
        A list of CoinbaseTransaction's derived from a CoinbaseNote's.
    """

    conversions = []
    missing_transactions = []

    # extract converted transactions
    for transaction in transactions:
        if not transaction.is_fiat:
            conversions.append(transaction)

    # extract missing transactions
    for convert in conversions:
        missing_transaction = get_missing_transaction(convert)
        missing_transactions.extend(missing_transaction)

    return missing_transactions


def exclude_crypto_to_crypto_transactions(
    transactions: list[CoinbaseProTransaction],
) -> list[CoinbaseProTransaction]:
    """Exclude crypto-to-crypto transactions from the list of transactions.

    Args:
        transactions: A list of CoinbaseProTransaction's.

    Returns:
        A list of CoinbaseProTransaction's with crypto-to-crypto transactions excluded.
    """

    processed_transactions = []

    for transaction in transactions:
        if transaction.is_fiat:
            processed_transactions.append(transaction)

    return processed_transactions


def parse_coinbase_pro(
    transactions: list[CoinbaseProTransaction],
    included_assets: list[str],
    include_missing: Optional[bool] = True,
) -> list[CoinbaseProTransaction]:
    """Get filtered transactions from CoinbaseProTransaction's dataset.

    Args:
        transactions: A list of CoinbaseProTransaction's.
        included_products: A list of strings representing the desired products.
        include_missing: Include crypto-to-crypto transaction dataset.

    Returns:
        A list of filtered CoinbaseProTransaction's.
    """

    filtered_transactions = filter_transactions(transactions, included_assets)

    if include_missing:
        missing_transactions = get_missing_transactions(filtered_transactions)
        filtered_transactions.extend(missing_transactions)

    return exclude_crypto_to_crypto_transactions(filtered_transactions)
