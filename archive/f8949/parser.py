from archive.f8949.models import F8949Transaction


def calculate_gain_or_loss(transaction: F8949Transaction) -> F8949Transaction:
    gain_or_loss = transaction.proceeds - transaction.cost_or_other_basis
    transaction.gain_or_loss = gain_or_loss
    return transaction


def parse_f8949(
    transactions: list[F8949Transaction],
) -> list[F8949Transaction]:
    parsed_transactions = []

    for transaction in transactions:
        parsed_transaction = calculate_gain_or_loss(transaction)
        parsed_transactions.append(parsed_transaction)

    return parsed_transactions
