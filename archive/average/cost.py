from os import getenv
from typing import Optional

from dotenv import load_dotenv

from archive.average.factory import broker_factory

load_dotenv()


def execute_dca(execute: Optional[bool] = False) -> None:
    EXCHANGE = getenv("EXCHANGE")
    PRODUCT_ID = getenv("PRODUCT_ID")
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
