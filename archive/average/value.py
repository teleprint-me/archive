from os import getenv
from typing import Optional, Union

from dotenv import load_dotenv

from archive.average.factory import Broker, broker_factory
from archive.average.models import ValueAverageColumn, ValueAverageRecord
from archive.tools.io import print_csv, read_write_csv, write_csv

load_dotenv()


def convert_csv_to_records(
    records: list[list[str]],
) -> list[ValueAverageRecord]:
    """Convert a list of lists representing CSV records into a list of
    ValueAverageRecord objects.

    Args:
        records (list[list[str]]): A list of lists representing CSV records.

    Returns:
        list[ValueAverageRecord]: A list of ValueAverageRecord objects.
    """

    entries = []

    for record in records[1:]:
        entry = ValueAverageRecord(
            exchange=record[ValueAverageColumn.EXCHANGE.value],
            product_id=record[ValueAverageColumn.PRODUCT_ID.value],
            principal_amount=float(
                record[ValueAverageColumn.PRINCIPAL_AMOUNT.value]
            ),
            side=record[ValueAverageColumn.SIDE.value],
            datetime=record[ValueAverageColumn.DATETIME.value],
            market_price=float(record[ValueAverageColumn.MARKET_PRICE.value]),
            current_target=float(
                record[ValueAverageColumn.CURRENT_TARGET.value]
            ),
            current_value=float(
                record[ValueAverageColumn.CURRENT_VALUE.value]
            ),
            order_size=float(record[ValueAverageColumn.ORDER_SIZE.value]),
            total_order_size=float(
                record[ValueAverageColumn.TOTAL_ORDER_SIZE.value]
            ),
            interval=int(record[ValueAverageColumn.INTERVAL.value]),
            growth_rate=float(record[ValueAverageColumn.GROWTH_RATE.value]),
            trade_amount=float(record[ValueAverageColumn.TRADE_AMOUNT.value]),
            total_trade_amount=float(
                record[ValueAverageColumn.TOTAL_TRADE_AMOUNT.value]
            ),
        )

        entries.append(entry)

    return entries


def convert_records_to_csv(
    records: list[ValueAverageRecord],
) -> list[list[str]]:
    """Convert a list of ValueAverageRecord objects into a list of lists
    representing CSV records.

    Args:
        records (list[ValueAverageRecord]): A list of ValueAverageRecord objects.

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
            "Growth Rate",
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
            str(record.growth_rate),
            str(record.trade_amount),
            str(record.total_trade_amount),
        ]

        entries.append(entry)

    return entries


def calculate_trade_amount(
    principal_amount: float,
    product_id: str,
    broker: Broker,
    last_record: Optional[ValueAverageRecord],
) -> float:
    frequency = {"daily": 365, "weekly": 52, "monthly": 12}.get(
        getenv("FREQUENCY") or "monthly", 12
    )
    interest_rate = float(getenv("INTEREST_RATE") or 0.05)  # default is 5%
    growth_rate = 1 + (interest_rate / frequency)

    # Simulate the order to get the current market price
    simulated_order = broker.get_simulated_order(principal_amount, product_id)
    market_price = float(simulated_order["market_price"])

    # Set default values if no previous record exists
    last_total_order_size = last_record.total_order_size if last_record else 0
    interval = last_record.interval + 1 if last_record else 1

    current_target = principal_amount * interval * pow(growth_rate, interval)

    current_value = market_price * last_total_order_size

    trade_amount = current_target - current_value

    return trade_amount


def create_value_average_record(
    order: dict[str, Union[str, float]],
    last_record: Optional[ValueAverageRecord] = None,
) -> ValueAverageRecord:
    """Create a new ValueAverageRecord using the provided order and the last record.

    Args:
        order: A dictionary containing the order details, including exchange, product_id, principal_amount, side, datetime, market_price, and order_size.
        last_record: The last ValueAverageRecord in the series, or None if there's no previous record.

    Notes:
        The growth rate used in the Value Averaging algorithm is calculated based on the interest rate and frequency environment variables.
        The default growth rate is 0.0041667 (5% per month) if no interest rate or frequency is provided.

    Returns:
        A new ValueAverageRecord instance with the calculated fields based on the provided order and last record.
    """

    # Calculate the growth rate
    frequency = {"daily": 365, "weekly": 52, "monthly": 12}.get(
        getenv("FREQUENCY") or "monthly", 12
    )
    interest_rate = float(getenv("INTEREST_RATE") or 0.05)  # default is 5%
    growth_rate = 1 + (interest_rate / frequency)

    # Extract the order information to calculate the record
    principal_amount = float(order["principal_amount"])
    market_price = float(order["market_price"])
    order_size = float(order["order_size"])

    # Set default values if no previous record exists
    last_total_order_size = last_record.total_order_size if last_record else 0
    interval = last_record.interval + 1 if last_record else 1

    current_target = principal_amount * interval * pow(growth_rate, interval)

    current_value = market_price * last_total_order_size

    trade_amount = current_target - current_value

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

    return ValueAverageRecord(
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
        growth_rate=growth_rate,
        trade_amount=trade_amount,
        total_trade_amount=total_trade_amount,
    )


def execute_value_average(file: str, execute: bool = False) -> None:
    """Execute a cost averaging order, update the records, and write the results to a CSV file.

    Args:
        file: The path to the CSV file to read and update with the new ValueAverageRecord.
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
    trade_amount = calculate_trade_amount(
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

    new_record = create_value_average_record(order, last_record)

    records.append(new_record)

    updated_csv_table = convert_records_to_csv(records)

    print_csv(updated_csv_table)

    write_csv(file, updated_csv_table)
