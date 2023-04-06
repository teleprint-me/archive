from archive.exchange.robinhood.models import RobinhoodTransaction
from archive.f8949.models import F8949Transaction
from archive.f8949.parser import calculate_gain_or_loss


def convert_robinhood_to_f8949_transactions(
    robinhood_transactions: list[RobinhoodTransaction],
) -> list[F8949Transaction]:
    f8949_transactions = []

    for transaction in robinhood_transactions:
        description = f"{transaction.asset} - {transaction.exchange}"

        f8949_transaction = F8949Transaction(
            description_of_property=description,
            date_acquired=transaction.received_date,
            date_sold=transaction.date_sold,
            proceeds=transaction.proceeds,
            cost_or_other_basis=transaction.cost_basis,
        )

        f8949_transaction = calculate_gain_or_loss(f8949_transaction)

        f8949_transactions.append(f8949_transaction)

    return f8949_transactions


def merge_f8949_transactions(
    existing_transactions: list[F8949Transaction],
    new_transactions: list[F8949Transaction],
) -> list[F8949Transaction]:
    existing_transactions.extend(new_transactions)
    return existing_transactions
