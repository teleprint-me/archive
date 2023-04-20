from datetime import datetime
from os import getenv
from typing import Optional, Union
from uuid import uuid4

from dotenv import load_dotenv

from archive.average.factory import broker_factory
from archive.average.models import CostAverageColumn, CostAverageRecord
from archive.tools.io import print_csv, read_write_csv, write_csv

load_dotenv()


def convert_csv_to_records(
    records: list[list[str]],
) -> list[CostAverageRecord]:
    entries = []

    for record in records[1:]:
        entry = CostAverageRecord(
            exchange=record[CostAverageColumn.EXCHANGE.value],
            product_id=record[CostAverageColumn.PRODUCT_ID.value],
            principal_amount=float(
                record[CostAverageColumn.PRINCIPAL_AMOUNT.value]
            ),
            side=record[CostAverageColumn.SIDE.value],
            datetime=record[CostAverageColumn.DATETIME.value],
            market_price=float(record[CostAverageColumn.MARKET_PRICE.value]),
            current_target=float(
                record[CostAverageColumn.CURRENT_TARGET.value]
            ),
            current_value=float(record[CostAverageColumn.CURRENT_VALUE.value]),
            order_size=float(record[CostAverageColumn.ORDER_SIZE.value]),
            total_order_size=float(
                record[CostAverageColumn.TOTAL_ORDER_SIZE.value]
            ),
            interval=int(record[CostAverageColumn.INTERVAL.value]),
            gain_loss=float(record[CostAverageColumn.GAIN_OR_LOSS.value]),
        )

        entries.append(entry)

    return entries


def convert_records_to_csv(
    records: list[CostAverageRecord],
) -> list[list[str]]:
    entries: list[list[str]] = [
        [
            "Exchange",
            "Product ID",
            "Principal Amount",
            "Side",
            "Datetime",
            "Market Price",
            "Current Target",
            "Current Value",
            "Order Size",
            "Total Order Size",
            "Interval",
        ]
    ]

    for record in records:
        entry: list[str] = [
            record.exchange,
            record.product_id,
            str(record.principal_amount),
            record.side,
            record.datetime,
            str(record.market_price),
            str(record.current_target),
            str(record.current_value),
            str(record.order_size),
            str(record.total_order_size),
            str(record.interval),
            str(record.gain_loss),
        ]

        entries.append(entry)

    return entries


def create_cost_average_record(
    order: dict[str, Union[str, float]],
    last_record: Optional[CostAverageRecord] = None,
) -> CostAverageRecord:
    principal_amount = float(order["principal_amount"])
    market_price = float(order["market_price"])
    order_size = float(order["order_size"])

    interval = last_record.interval + 1 if last_record else 1

    current_value = market_price * order_size

    current_target = (
        last_record.current_target + principal_amount
        if last_record
        else principal_amount
    )

    total_order_size = (
        last_record.total_order_size + order_size
        if last_record
        else order_size
    )

    gain_loss = current_value - current_target

    return CostAverageRecord(
        str(order["exchange"]),
        str(order["product_id"]),
        principal_amount,
        str(order["side"]),
        str(order["datetime"]),
        float(order["market_price"]),
        current_target,
        current_value,
        float(order["order_size"]),
        total_order_size,
        interval,
        gain_loss,
    )


def execute_cost_average(file: str, execute: bool = False) -> None:
    exchange = getenv("EXCHANGE") or ""
    product_id = getenv("PRODUCT_ID") or ""
    principal_amount = float(getenv("PRINCIPAL_AMOUNT") or 0)

    broker = broker_factory(exchange)

    csv_table = read_write_csv(file, [])
    records = convert_csv_to_records(csv_table)

    last_record = records[-1] if records else None

    if execute:
        order = broker.post_order(principal_amount, product_id, side="BUY")
    else:
        order = broker.get_simulated_order(
            principal_amount, product_id, side="BUY"
        )

    new_record = create_cost_average_record(order, last_record)

    records.append(new_record)

    updated_csv_table = convert_records_to_csv(records)

    print_csv(updated_csv_table)

    write_csv(file, updated_csv_table)
