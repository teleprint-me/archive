from archive.gl.models import GLTotalTransaction, GLTransaction


def calculate_buy_cost_basis(transaction: GLTransaction) -> GLTransaction:
    order_size = transaction.order_size
    market_price = transaction.market_price
    exchange_fee = transaction.exchange_fee
    cost_basis = (order_size * market_price) + exchange_fee
    transaction.cost_or_other_basis = cost_basis
    return transaction


def calculate_sell_cost_basis(transaction: GLTransaction) -> GLTransaction:
    order_size = transaction.order_size
    acb_per_share = transaction.acb_per_share
    transaction.cost_or_other_basis = order_size * acb_per_share
    return transaction


def calculate_adjusted_cost_basis(transaction: GLTransaction) -> GLTransaction:
    # NOTE: This is only used on the buy side of a transaction.
    # The sell side always inherits the last calculated ACB
    # from the last known `total_acb_per_share` which is out of
    # the scope or capability of this function.
    order_size = transaction.order_size
    cost_basis = transaction.cost_or_other_basis
    transaction.acb_per_share = cost_basis / order_size
    return transaction


def calculate_sales_proceeds(transaction: GLTransaction) -> GLTransaction:
    order_size = transaction.order_size
    market_price = transaction.market_price
    transaction.sales_proceeds = order_size * market_price
    return transaction


def calculate_gain_or_loss(transaction: GLTransaction) -> GLTransaction:
    sales_proceeds = transaction.sales_proceeds
    cost_basis = transaction.cost_or_other_basis
    exchange_fee = transaction.exchange_fee
    transaction.gain_or_loss = sales_proceeds - cost_basis - exchange_fee
    return transaction


def calculate_total_transaction(
    total: GLTotalTransaction,
    block: list[GLTransaction],
) -> GLTotalTransaction:
    # NOTE: A block is a contiguous sequence of `GLTransactions` that
    # have the same `transaction_type`.
    # e.g. All transactions within a given sequence are either
    # a "Buy" or "Sell" `transaction_type`, but not both.

    if block[0].is_buy:
        total.order_size += sum(tx.order_size for tx in block)
        total.cost_or_other_basis += sum(
            tx.cost_or_other_basis for tx in block
        )
    else:
        total.order_size += sum(-tx.order_size for tx in block)
        total.cost_or_other_basis += sum(
            -tx.cost_or_other_basis for tx in block
        )
        total.gain_or_loss += sum(tx.gain_or_loss for tx in block)

    total.acb_per_share = total.cost_or_other_basis / total.order_size

    return total


def build_total_transaction(
    total: GLTotalTransaction,
) -> GLTransaction:
    return GLTransaction(
        additional_description="total",
        description="",
        date_acquired="",
        transaction_type="",
        order_size=total.order_size,
        market_price=0.0,
        exchange_fee=0.0,
        cost_or_other_basis=total.cost_or_other_basis,
        acb_per_share=total.acb_per_share,
        gain_or_loss=total.gain_or_loss,
    )


def build_transaction_blocks(
    transactions: list[GLTransaction],
) -> list[list[GLTransaction]]:
    transaction_blocks = []
    current_block = []
    current_transaction_type = transactions[0].is_buy

    for transaction in transactions:
        if transaction.is_buy != current_transaction_type:
            transaction_blocks.append(current_block)
            current_block = []
            current_transaction_type = transaction.is_buy

        current_block.append(transaction)

    if current_block:
        transaction_blocks.append(current_block)

    return transaction_blocks


def parse_gl(transactions: list[GLTransaction]) -> list[GLTransaction]:
    gl_transactions = []
    total = GLTotalTransaction()
    blocks = build_transaction_blocks(transactions)

    for block in blocks:
        processed_transactions = []

        for transaction in block:
            if transaction.is_buy:
                transaction = calculate_buy_cost_basis(transaction)
                transaction = calculate_adjusted_cost_basis(transaction)

            else:
                transaction.acb_per_share = total.acb_per_share
                transaction = calculate_sell_cost_basis(transaction)
                transaction = calculate_sales_proceeds(transaction)
                transaction = calculate_gain_or_loss(transaction)

            processed_transactions.append(transaction)

        total = calculate_total_transaction(total, block)
        total_transaction = build_total_transaction(total)

        gl_transactions.extend(processed_transactions)
        gl_transactions.append(total_transaction)

    return gl_transactions