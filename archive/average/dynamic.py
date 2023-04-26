from os import getenv
from typing import Optional, Union

from dotenv import load_dotenv

from archive.average.factory import Broker, broker_factory
from archive.average.models import DynamicAverageColumn, DynamicAverageRecord
from archive.tools.io import print_csv, read_write_csv, write_csv

load_dotenv()


def convert_csv_to_records(
    records: list[list[str]],
) -> list[DynamicAverageRecord]:
    """Convert a list of lists representing CSV records into a list of
    DynamicAverageRecord objects.

    Args:
        records (list[list[str]]): A list of lists representing CSV records.

    Returns:
        list[DynamicAverageRecord]: A list of DynamicAverageRecord objects.
    """

    entries = []

    for record in records[1:]:
        entry = DynamicAverageRecord(
            exchange=record[DynamicAverageColumn.EXCHANGE.value],
            product_id=record[DynamicAverageColumn.PRODUCT_ID.value],
            principal_amount=float(
                record[DynamicAverageColumn.PRINCIPAL_AMOUNT.value]
            ),
            side=record[DynamicAverageColumn.SIDE.value],
            datetime=record[DynamicAverageColumn.DATETIME.value],
            market_price=float(
                record[DynamicAverageColumn.MARKET_PRICE.value]
            ),
            current_target=float(
                record[DynamicAverageColumn.CURRENT_TARGET.value]
            ),
            current_value=float(
                record[DynamicAverageColumn.CURRENT_VALUE.value]
            ),
            order_size=float(record[DynamicAverageColumn.ORDER_SIZE.value]),
            total_order_size=float(
                record[DynamicAverageColumn.TOTAL_ORDER_SIZE.value]
            ),
            interval=int(record[DynamicAverageColumn.INTERVAL.value]),
            multiplier=float(record[DynamicAverageColumn.MULTIPLIER.value]),
            trade_amount=float(
                record[DynamicAverageColumn.TRADE_AMOUNT.value]
            ),
            total_trade_amount=float(
                record[DynamicAverageColumn.TOTAL_TRADE_AMOUNT.value]
            ),
        )

        entries.append(entry)

    return entries


def convert_records_to_csv(
    records: list[DynamicAverageRecord],
) -> list[list[str]]:
    """Convert a list of DynamicAverageRecord objects into a list of lists
    representing CSV records.

    Args:
        records (list[DynamicAverageRecord]): A list of DynamicAverageRecord objects.

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
            "Multiplier",
            "Trade Amount",
            "Total Trade Amount",
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
            str(record.multiplier),
            str(record.trade_amount),
            str(record.total_trade_amount),
        ]

        entries.append(entry)

    return entries


def calculate_trade_amount_and_multiplier(
    principal_amount: float,
    product_id: str,
    broker: Broker,
    last_record: Optional[DynamicAverageRecord],
) -> tuple[float, int]:
    max_multiplier = int(getenv("MAX_MULTIPLIER") or 5)
    min_multiplier = 1

    # Simulate the order to get the current market price
    simulated_order = broker.get_simulated_order(principal_amount, product_id)
    market_price = float(simulated_order["market_price"])

    # Set default values if no previous record exists
    last_total_order_size = last_record.total_order_size if last_record else 0
    interval = last_record.interval + 1 if last_record else 1

    current_target = principal_amount * interval
    current_value = market_price * last_total_order_size

    target_difference = current_target - current_value
    raw_multiplier = target_difference / principal_amount

    # Enforce the min_multiplier and max_multiplier limits
    if raw_multiplier == 0:
        multiplier = min_multiplier
    elif raw_multiplier > max_multiplier:
        multiplier = max_multiplier
    elif raw_multiplier < -max_multiplier:
        multiplier = -max_multiplier
    elif raw_multiplier < 0:
        multiplier = -round(
            max(min_multiplier, min(abs(raw_multiplier), max_multiplier))
        )
    else:
        multiplier = round(
            max(min_multiplier, min(raw_multiplier, max_multiplier))
        )

    trade_amount = multiplier * principal_amount

    return trade_amount, multiplier


def create_dynamic_cost_average_record(
    order: dict[str, Union[str, float]],
    multiplier: int = 1,
    last_record: Optional[DynamicAverageRecord] = None,
) -> DynamicAverageRecord:
    """Create a new DynamicAverageRecord using the provided order, the last record, and the multiplier.

    Args:
        order: A dictionary containing the order details, including exchange, product_id, principal_amount, side, datetime, market_price, and order_size.
        last_record: The last DynamicAverageRecord in the series, or None if there's no previous record.
        multiplier: The calculated multiplier value for the trade.

    Returns:
        A new DynamicAverageRecord instance with the calculated fields based on the provided order, last record, and multiplier.
    """

    # Extract the order information to calculate the record
    principal_amount = float(order["principal_amount"])
    market_price = float(order["market_price"])
    order_size = float(order["order_size"])

    # Set default values if no previous record exists
    last_total_order_size = last_record.total_order_size if last_record else 0
    interval = last_record.interval + 1 if last_record else 1

    current_target = principal_amount * interval
    current_value = market_price * last_total_order_size

    trade_amount = multiplier * principal_amount

    total_trade_amount = (
        last_record.total_trade_amount + trade_amount
        if last_record
        else trade_amount
    )

    total_order_size = (
        last_record.total_order_size + order_size
        if last_record
        else order_size
    )

    return DynamicAverageRecord(
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
        multiplier=multiplier,
        trade_amount=trade_amount,
        total_trade_amount=total_trade_amount,
    )


def execute_dynamic_cost_averaging(file: str, execute: bool = False) -> None:
    """Execute a dynamic cost averaging order, update the records, and write the results to a CSV file.

    Args:
        file: The path to the CSV file to read and update with the new DynamicAverageRecord.
        execute: A boolean flag indicating whether to execute a real order (True) or simulate one (False).
    """

    exchange = getenv("EXCHANGE") or ""
    product_id = getenv("PRODUCT_ID") or ""
    principal_amount = float(getenv("PRINCIPAL_AMOUNT") or 0)

    broker = broker_factory(exchange)

    min_trade_amount = broker.get_min_order_size(product_id)

    csv_table = read_write_csv(file, [])
    records = convert_csv_to_records(csv_table)

    last_record = records[-1] if records else None

    # Calculate the trade amount using the helper function
    trade_amount, multiplier = calculate_trade_amount_and_multiplier(
        principal_amount, product_id, broker, last_record
    )

    # Check if the trade amount is below the minimum trade amount
    if abs(trade_amount) < min_trade_amount:
        print(
            f"Hold: Calculated trade amount ({trade_amount}) is below the minimum trade amount ({min_trade_amount})."
        )
        return None

    # Determine the side based on the trade amount's sign
    side = "SELL" if trade_amount < 0 else "BUY"

    # Update trade_amount to its absolute value
    trade_amount = abs(trade_amount)

    if execute:
        order = broker.post_order(trade_amount, product_id, side)
    else:
        order = broker.get_simulated_order(trade_amount, product_id, side)

    new_record = create_dynamic_cost_average_record(
        order, multiplier, last_record
    )

    records.append(new_record)

    updated_csv_table = convert_records_to_csv(records)

    print_csv(updated_csv_table)

    write_csv(file, updated_csv_table)
