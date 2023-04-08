from typing import Optional

from archive.exchange.kraken.api import get_asset_info, get_spot_price
from archive.exchange.kraken.models import KrakenTransaction


def filter_transactions(
    transactions: list[KrakenTransaction],
    included_assets: list[str],
) -> list[KrakenTransaction]:
    """Filter transactions based on asset.

    Args:
        transactions: A list of transactions.
        included_assets: A list of strings representing the desired assets.

    Returns:
        A list of filtered transactions.
    """
    filtered_transactions = []

    for transaction in transactions:
        if transaction.should_keep(included_assets):
            filtered_transactions.append(transaction)

    return filtered_transactions


def get_missing_crypto_to_crypto(
    transaction: KrakenTransaction,
) -> list[KrakenTransaction]:
    """Get missing transaction data for the given crypto-to-crypto transaction.

    Args:
        transaction: A KrakenTransaction instance.

    Returns:
        A list containing missing KrakenTransaction's.
    """

    # 1. Determine the Product, Base Product, and Quote Product
    product_info = get_asset_info(transaction.pair)
    if len(transaction.pair) == 6 or len(transaction.pair) == 7:
        base_product = f"{product_info['base']}USD"
        quote_product = f"{product_info['quote']}USD"
    else:
        base_product = f"{product_info['base']}ZUSD"
        quote_product = f"{product_info['quote']}ZUSD"

    # 2. Determine Market Price for both Base and Quote Products
    base_response = get_spot_price(base_product, transaction.time)
    quote_response = get_spot_price(quote_product, transaction.time)
    # Extract the market price from the responses
    base_price = float(base_response["data"]["amount"])
    quote_price = float(quote_response["data"]["amount"])

    # 3. Determine the Transaction Total for both Base and Quote Products
    base_total = base_price * transaction.vol
    quote_total = quote_price * transaction.cost

    # 4. Determine the Transaction Fee for both Base and Quote Products
    quote_fee = quote_price * transaction.fee
    base_fee = 0.0

    # 5. Get the order size for the Base and Quote Products
    base_size = transaction.vol
    quote_size = transaction.cost

    # 6. Create KrakenTransaction for the missing BUY or SELL side
    if transaction.type == "buy":
        missing_buy_notes = (
            f"Bought {base_size:.8f} {transaction.base} "
            f"with {quote_size:.8f} {transaction.quote}"
        )
        # BUY side is missing selling the quote product for fiat
        # and buying the base product with fiat
        missing_sell = KrakenTransaction(
            txid=transaction.txid,
            order_txid=transaction.order_txid,
            pair=quote_product,
            time=transaction.time,
            type="sell",
            order_type=transaction.order_type,
            price=quote_price,
            cost=quote_total,
            fee=quote_fee,
            vol=quote_size,
            margin=transaction.margin,
            misc=transaction.misc,
            ledgers=transaction.ledgers,
            notes=missing_buy_notes,
        )
        missing_buy = KrakenTransaction(
            txid=transaction.txid,
            order_txid=transaction.order_txid,
            pair=base_product,
            time=transaction.time,
            type="buy",
            order_type=transaction.order_type,
            price=base_price,
            cost=base_total,
            fee=base_fee,
            vol=base_size,
            margin=transaction.margin,
            misc=transaction.misc,
            ledgers=transaction.ledgers,
            notes=missing_buy_notes,
        )
    elif transaction.type == "sell":
        missing_sell_notes = (
            f"Sold {base_size:.8f} {transaction.base} "
            f"for {quote_size:.8f} {transaction.quote}"
        )
        # SELL side is missing selling the base product for fiat
        # and buying the quote product with fiat
        missing_sell = KrakenTransaction(
            txid=transaction.txid,
            order_txid=transaction.order_txid,
            pair=base_product,
            time=transaction.time,
            type="sell",
            order_type=transaction.order_type,
            price=base_price,
            cost=base_total,
            fee=base_fee,
            vol=base_size,
            margin=transaction.margin,
            misc=transaction.misc,
            ledgers=transaction.ledgers,
            notes=missing_sell_notes,
        )
        missing_buy = KrakenTransaction(
            txid=transaction.txid,
            order_txid=transaction.order_txid,
            pair=quote_product,
            time=transaction.time,
            type="buy",
            order_type=transaction.order_type,
            price=quote_price,
            cost=quote_total,
            fee=quote_fee,
            vol=quote_size,
            margin=transaction.margin,
            misc=transaction.misc,
            ledgers=transaction.ledgers,
            notes=missing_sell_notes,
        )
    else:
        raise ValueError(f"Invalid transaction type {transaction.type}")

    return [missing_sell, missing_buy]


def get_missing_crypto_to_stablecoin(
    transaction: KrakenTransaction,
) -> list[KrakenTransaction]:
    """Get missing transaction for a crypto-to-stablecoin transaction in Kraken.

    Args:
        transaction: A KrakenTransaction.

    Returns:
        A list of KrakenTransaction's derived from the transaction.
    """

    # 1. Determine the Product, Base Product, and Quote Product
    product_info = get_asset_info(transaction.pair)
    if len(transaction.pair) == 6 or len(transaction.pair) == 7:
        base_product = f"{product_info['base']}USD"
        quote_product = f"{product_info['quote']}USD"
    else:
        base_product = f"{product_info['base']}ZUSD"
        quote_product = f"{product_info['quote']}ZUSD"

    # 2. Determine the Transaction Size for both Base and Quote Products
    base_size = transaction.vol
    quote_size = transaction.cost

    # 3. Determine Market Price for the Quote Product
    quote_response = get_spot_price(quote_product, transaction.time)
    quote_price = float(quote_response["data"]["amount"])

    # 4. Calculate base transaction variables based on quote_price
    base_price = transaction.price / quote_price
    base_fee = transaction.fee / quote_price
    base_total = quote_size / quote_price

    # 5. Calculate quote_total based on base_total
    quote_total = base_total

    # Label each product transaction as a BUY or SELL
    if transaction.type == "buy":
        base_side = "buy"
        quote_side = "sell"
    else:
        base_side = "sell"
        quote_side = "buy"

    # Create the missing transactions for base product and quote product
    base_transaction = KrakenTransaction(
        txid=transaction.txid,
        order_txid=transaction.order_txid,
        pair=base_product,
        time=transaction.time,
        type=base_side,
        order_type=transaction.order_type,
        price=base_price,
        cost=base_total,
        fee=base_fee,
        vol=base_size,
        margin=transaction.margin,
        misc=transaction.misc,
        ledgers=transaction.ledgers,
        notes=transaction.notes,
    )

    quote_transaction = KrakenTransaction(
        txid=transaction.txid,
        order_txid=transaction.order_txid,
        pair=quote_product,
        time=transaction.time,
        type=quote_side,
        order_type=transaction.order_type,
        price=quote_price,
        cost=quote_total,
        fee=0.0,
        vol=quote_size,
        margin=transaction.margin,
        misc=transaction.misc,
        ledgers=transaction.ledgers,
        notes=transaction.notes,
    )

    return [base_transaction, quote_transaction]


def get_missing_transactions(
    transactions: list[KrakenTransaction],
) -> list[KrakenTransaction]:
    """Get missing transaction dataset for Kraken transactions.

    Args:
        transactions: A list of KrakenTransaction's.

    Returns:
        A list of KrakenTransaction's derived from a KrakenNote's.
    """

    crypto_to_crypto = []
    crypto_to_stablecoin = []
    missing_transactions = []

    # classify transactions
    for transaction in transactions:
        if not transaction.is_fiat:
            if transaction.is_stablecoin:
                crypto_to_stablecoin.append(transaction)
            else:
                crypto_to_crypto.append(transaction)

    # process crypto-to-crypto transactions
    for convert in crypto_to_crypto:
        missing_transaction = get_missing_crypto_to_crypto(convert)
        missing_transactions.extend(missing_transaction)

    # process crypto-to-stablecoin transactions
    for convert in crypto_to_stablecoin:
        missing_transaction = get_missing_crypto_to_stablecoin(convert)
        missing_transactions.extend(missing_transaction)

    return missing_transactions


def exclude_crypto_to_crypto_transactions(
    transactions: list[KrakenTransaction],
) -> list[KrakenTransaction]:
    """Exclude crypto-to-crypto transactions from the list of transactions.

    Args:
        transactions: A list of KrakenTransaction's.

    Returns:
        A list of KrakenTransaction's with crypto-to-crypto transactions excluded.
    """

    processed_transactions = []

    for transaction in transactions:
        if transaction.is_fiat:
            processed_transactions.append(transaction)

    return processed_transactions


def parse_kraken(
    transactions: list[KrakenTransaction],
    included_assets: list[str],
    include_missing: Optional[bool] = True,
) -> list[KrakenTransaction]:
    """Get filtered transactions from KrakenTransaction's dataset.

    Args:
        transactions: A list of KrakenTransaction's.
        included_assets: A list of strings representing the desired assets.
        include_missing: Include crypto-to-crypto transaction dataset.

    Returns:
        A list of filtered KrakenTransaction's.
    """

    filtered_transactions = filter_transactions(transactions, included_assets)

    if include_missing:
        missing_transactions = get_missing_transactions(filtered_transactions)
        filtered_transactions.extend(missing_transactions)

    return exclude_crypto_to_crypto_transactions(filtered_transactions)
