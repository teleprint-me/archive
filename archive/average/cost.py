from os import getenv

from dotenv import load_dotenv

from archive.average.factory import broker_factory
from archive.average.models import CostAverageRecord
from archive.tools.io import print_csv, read_csv, write_csv

load_dotenv()


def execute_dca(file: str, execute: bool = False) -> None:
    EXCHANGE = getenv("EXCHANGE") or ""
    PRODUCT_ID = getenv("PRODUCT_ID") or ""
    PRINCIPAL_AMOUNT = float(getenv("PRINCIPAL_AMOUNT") or 0)

    broker = broker_factory(EXCHANGE)

    if execute:
        order_size = broker.order(PRINCIPAL_AMOUNT, PRODUCT_ID)

        # create dca record
        # print dca record
        # write dca record
    else:
        # simulate given order
        pass
