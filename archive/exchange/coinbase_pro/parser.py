from typing import Optional

from archive.exchange.coinbase.api import get_spot_price
from archive.exchange.coinbase_pro.models import CoinbaseProTransaction


def get_missing_crypto_to_crypto(
    transaction: CoinbaseProTransaction,
) -> list[CoinbaseProTransaction]:
    """Get missing transaction data for the given crypto-to-crypto transaction.

    Args:
        transaction: A CoinbaseProTransaction instance.

    Returns:
        A list containing missing CoinbaseProTransaction's.
    """

    # Determine the Product, Base Product, and Quote Product
    base_product = f"{transaction.base}-USD"
    quote_product = f"{transaction.quote}-USD"

    # Determine Market Price for both Base and Quote Products
    base_price = get_spot_price(base_product, transaction.created_at)
    quote_price = get_spot_price(quote_product, transaction.created_at)

    # Determine the Transaction Total for both Base and Quote Products
    base_total = base_price * transaction.size
    quote_total = quote_price * transaction.total

    # Determine the Transaction Fee for both Base and Quote Products
    quote_fee = quote_price * transaction.fee
    base_fee = 0.0

    # Get the order size for the Base and Quote Products
    base_size = transaction.size
    quote_size = transaction.total

    # Create CoinbaseProTransaction for the missing BUY or SELL side
    if transaction.side == "BUY":
        missing_buy_notes = (
            f"Bought {base_size:.8f} {transaction.base} "
            f"with {quote_size:.8f} {transaction.quote}"
        )
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
            notes=missing_buy_notes,
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
        missing_sell_notes = (
            f"Sold {base_size:.8f} {transaction.base} "
            f"for {quote_size:.8f} {transaction.quote}"
        )
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
            notes=missing_sell_notes,
        )
    else:
        raise ValueError(f"Invalid side {transaction.side}")

    return [missing_sell, missing_buy]


def get_missing_crypto_to_stablecoin(
    transaction: CoinbaseProTransaction,
) -> list[CoinbaseProTransaction]:
    """Get missing transaction for a crypto-to-stablecoin transaction.

    Args:
        transaction: A CoinbaseProTransaction.

    Returns:
        A list of CoinbaseTransaction's derived from the transaction.
    """

    # Determine the Product, Base Product, and Quote Product
    base_product = f"{transaction.base}-USD"
    quote_product = f"{transaction.quote}-USD"

    # Determine the Transaction Size for both Base and Quote Products
    base_size = transaction.size
    quote_size = transaction.total

    # Calculate quote_price
    quote_price = get_spot_price(quote_product, transaction.created_at)

    # Calculate base transaction variables based on quote_price
    base_price = transaction.price / quote_price
    base_fee = transaction.fee / quote_price
    base_total = quote_size / quote_price

    # Calculate quote_total based on base_total
    quote_total = base_total

    # Label each product transaction as a BUY or SELL
    if transaction.side == "BUY":
        base_side = "BUY"
        quote_side = "SELL"
    else:
        base_side = "SELL"
        quote_side = "BUY"

    # Create the missing transactions for base product and quote product
    base_transaction = CoinbaseProTransaction(
        portfolio=transaction.portfolio,
        trade_id=transaction.trade_id,
        product=base_product,
        side=base_side,
        created_at=transaction.created_at,
        size=base_size,
        size_unit=transaction.base,
        price=base_price,
        fee=base_fee,
        total=base_total,
        total_unit="USD",
        notes=f"Bought {base_size} {transaction.base} with {quote_size} {transaction.quote}",
    )

    quote_transaction = CoinbaseProTransaction(
        portfolio=transaction.portfolio,
        trade_id=transaction.trade_id,
        product=quote_product,
        side=quote_side,
        created_at=transaction.created_at,
        size=quote_size,
        size_unit=transaction.quote,
        price=quote_price,
        fee=0.0,
        total=quote_total,
        total_unit="USD",
        notes=f"Sold {quote_size} {transaction.quote} for {base_size} {transaction.base}",
    )

    return [base_transaction, quote_transaction]


def get_missing_transactions(
    transactions: list[CoinbaseProTransaction],
) -> list[CoinbaseProTransaction]:
    """Get missing transaction dataset for Coinbase Pro transactions.

    Args:
        transactions: A list of CoinbaseProTransaction's.

    Returns:
        A list of CoinbaseTransaction's derived from a CoinbaseNote's.
    """

    crypto_to_crypto = []
    crypto_to_stablecoin = []
    missing_transactions = []

    # Classify transactions
    for transaction in transactions:
        if not transaction.is_fiat:
            if transaction.is_stablecoin:
                crypto_to_stablecoin.append(transaction)
            else:
                crypto_to_crypto.append(transaction)

    # Process crypto-to-crypto transactions
    for convert in crypto_to_crypto:
        missing_transaction = get_missing_crypto_to_crypto(convert)
        missing_transactions.extend(missing_transaction)

    # Process crypto-to-stablecoin transactions
    for convert in crypto_to_stablecoin:
        missing_transaction = get_missing_crypto_to_stablecoin(convert)
        missing_transactions.extend(missing_transaction)

    return missing_transactions


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

    # Include user selected assets
    included_transactions = [
        tx for tx in transactions if tx.should_keep(included_assets)
    ]

    # Construct tx's from extracted data for crypto-to-crypto tx's
    if include_missing:
        missing_transactions = get_missing_transactions(included_transactions)
        included_transactions.extend(missing_transactions)

    # Exclude crypto-to-crypto assets
    processed_transactions = [tx for tx in included_transactions if tx.is_fiat]

    return processed_transactions
