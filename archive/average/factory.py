from abc import ABC, abstractmethod

from archive.average.models import DCARecord


class BaseParser(ABC):
    @abstractmethod
    def dca_order(
        self,
        quote_size: float,
        product_id: str,
        side: str = "BUY",
    ) -> DCARecord:
        raise NotImplementedError()


class Coinbase(BaseParser):
    def parse(
        self,
        filepath: Union[str, Path],
        asset: str,
    ) -> list[IRTransaction]:
        transactions = scan_coinbase_transactions(filepath)
        return build_coinbase_ir(transactions, [asset])
