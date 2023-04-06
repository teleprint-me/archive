from archive.exchange.robinhood.models import RobinhoodTransaction


def filter_transactions(
    transactions: list[RobinhoodTransaction], included_assets: list[str]
) -> list[RobinhoodTransaction]:
    return [
        transaction
        for transaction in transactions
        if transaction.should_keep(included_assets)
    ]


def parse_robinhood(
    transactions: list[RobinhoodTransaction], included_assets: list[str]
) -> list[RobinhoodTransaction]:
    return filter_transactions(transactions, included_assets)
