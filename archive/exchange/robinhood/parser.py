from archive.exchange.robinhood.models import RobinhoodTransaction


def parse_robinhood(
    transactions: list[RobinhoodTransaction], included_assets: list[str]
) -> list[RobinhoodTransaction]:
    return [
        transaction
        for transaction in transactions
        if transaction.should_keep(included_assets)
    ]
