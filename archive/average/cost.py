from os import getenv
from typing import Optional, Union

from dotenv import load_dotenv

from archive.average.factory import broker_factory
from archive.average.models import CostAverageColumn, CostAverageRecord
from archive.tools.io import print_csv, read_write_csv, write_csv

load_dotenv()


def convert_csv_to_records(
    records: list[list[str]],
) -> list[CostAverageRecord]:
    """Convert a list of lists representing CSV records into a list of
    CostAverageRecord objects.

    Args:
        records (list[list[str]]): A list of lists representing CSV records.

    Returns:
        list[CostAverageRecord]: A list of CostAverageRecord objects.
    """

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
            gain_or_loss=float(record[CostAverageColumn.GAIN_OR_LOSS.value]),
        )

        entries.append(entry)

    return entries


def convert_records_to_csv(
    records: list[CostAverageRecord],
) -> list[list[str]]:
    """Convert a list of CostAverageRecord objects into a list of lists
    representing CSV records.

    Args:
        records (list[CostAverageRecord]): A list of CostAverageRecord objects.

    Returns:
        list[list[str]]: A list of lists representing CSV records.
    """

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
            "Gain or (Loss)",
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
            str(record.gain_or_loss),
        ]

        entries.append(entry)

    return entries


def create_cost_average_record(
    order: dict[str, Union[str, float]],
    last_record: Optional[CostAverageRecord] = None,
) -> CostAverageRecord:
    """Create a new CostAverageRecord using the provided order and the last record.

    Args:
        order: A dictionary containing the order details, including exchange, product_id, principal_amount, side, datetime, market_price, and order_size.
        last_record: The last CostAverageRecord in the series, or None if there's no previous record.

    Returns:
        A new CostAverageRecord instance with the calculated fields based on the provided order and last record.
    """

    principal_amount = float(order["principal_amount"])
    market_price = float(order["market_price"])
    order_size = float(order["order_size"])

    last_total_order_size = last_record.total_order_size if last_record else 0
    last_current_target = last_record.current_target if last_record else 0
    interval = last_record.interval + 1 if last_record else 1

    current_value = market_price * last_total_order_size

    gain_loss = current_value - last_current_target

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

    return CostAverageRecord(
        exchange=str(order["exchange"]),
        product_id=str(order["product_id"]),
        principal_amount=principal_amount,
        side=str(order["side"]),
        datetime=str(order["datetime"]),
        market_price=float(order["market_price"]),
        current_target=current_target,
        current_value=current_value,
        order_size=float(order["order_size"]),
        total_order_size=total_order_size,
        interval=interval,
        gain_or_loss=gain_loss,
    )


def execute_cost_average(file: str, execute: bool = False) -> None:
    """Execute a cost averaging order, update the records, and write the results to a CSV file.

    Args:
        file: The path to the CSV file to read and update with the new CostAverageRecord.
        execute: A boolean flag indicating whether to execute a real order (True) or simulate one (False).
    """

    exchange = getenv("EXCHANGE") or ""
    product_id = getenv("PRODUCT_ID") or ""
    principal_amount = float(getenv("PRINCIPAL_AMOUNT") or 0)

    broker = broker_factory(exchange)

    csv_table = read_write_csv(file, [])
    records = convert_csv_to_records(csv_table)

    last_record = records[-1] if records else None

    if execute:
        order = broker.post_order(principal_amount, product_id)
    else:
        order = broker.get_simulated_order(principal_amount, product_id)

    new_record = create_cost_average_record(order, last_record)

    records.append(new_record)

    updated_csv_table = convert_records_to_csv(records)

    print_csv(updated_csv_table)

    write_csv(file, updated_csv_table)
