from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from archive.exchange.coinbase.ir import build_coinbase_ir
from archive.exchange.coinbase.scanner import scan_coinbase_transactions
from archive.exchange.coinbase_pro.ir import build_coinbase_pro_ir
from archive.exchange.coinbase_pro.scanner import (
    scan_coinbase_pro_accounts,
    scan_coinbase_pro_fills,
)
from archive.exchange.kraken.ir import build_kraken_ir
from archive.exchange.kraken.scanner import (
    scan_kraken_ledgers,
    scan_kraken_trades,
)
from archive.ir.models import IRTransaction


class BaseParser(ABC):
    @abstractmethod
    def parse(
        self,
        filepath: Union[str, Path],
        asset: str,
    ) -> list[IRTransaction]:
        raise NotImplementedError()


class Coinbase(BaseParser):
    def parse(
        self,
        filepath: Union[str, Path],
        asset: str,
    ) -> list[IRTransaction]:
        transactions = scan_coinbase_transactions(filepath)
        return build_coinbase_ir(transactions, [asset])


class CoinbaseProFill(BaseParser):
    def parse(
        self,
        filepath: Union[str, Path],
        asset: str,
    ) -> list[IRTransaction]:
        transactions = scan_coinbase_pro_fills(filepath)
        return build_coinbase_pro_ir(transactions, [asset])


class CoinbaseProAccount(BaseParser):
    def parse(
        self,
        filepath: Union[str, Path],
        asset: str,
    ) -> list[IRTransaction]:
        transactions = scan_coinbase_pro_accounts(filepath)
        return build_coinbase_pro_ir(transactions, [asset])


class KrakenTrade(BaseParser):
    def parse(
        self,
        filepath: Union[str, Path],
        asset: str,
    ) -> list[IRTransaction]:
        transactions = scan_kraken_trades(filepath)
        return build_kraken_ir(transactions, [asset])


class KrakenLedger(BaseParser):
    def parse(
        self,
        filepath: Union[str, Path],
        asset: str,
    ) -> list[IRTransaction]:
        transactions = scan_kraken_ledgers(filepath)
        return build_kraken_ir(transactions, [asset])


class Robinhood1099(BaseParser):
    def parse(
        self,
        filepath: Union[str, Path],
        asset: str,
    ) -> list[IRTransaction]:
        raise NotImplementedError()


def parser_factory(dataset_type):
    if dataset_type == "coinbase_transaction":
        return Coinbase()
    elif dataset_type == "coinbase_pro_fill":
        return CoinbaseProFill()
    elif dataset_type == "coinbase_pro_account":
        return CoinbaseProAccount()
    elif dataset_type == "kraken_trade":
        return KrakenTrade()
    elif dataset_type == "kraken_ledger":
        return KrakenLedger()
    elif dataset_type == "robinhood_1099":
        return Robinhood1099()
    else:
        raise ValueError(f"Invalid dataset type: {dataset_type}")
