import csv
from pathlib import Path
from typing import Union

import texttable

from archive.tools.logger import setup_logger

logger = setup_logger("io_logger", "data/log/io.log")


def read_csv(filepath: Union[str, Path]) -> list[list[str]]:
    """Read data from a CSV file using the given filepath.

    Args:
        filepath: The path to the CSV file to read.

    Returns:
        A list of CSV rows, where each row is a list of column values.
    """
    csv_table = []

    with open(filepath, mode="r") as file:
        for csv_row in csv.reader(file, delimiter=","):
            csv_table.append(csv_row)

    logger.debug(f"CSV_READ: {filepath}")
    logger.debug(f"CSV_READ_TABLE: {csv_table}")

    return csv_table


def write_csv(
    filepath: Union[str, Path],
    csv_table: list[list[str]],
) -> None:
    """Write data to a CSV file.

    Args:
        filepath: The path to the CSV file to write to.
        csv_table: The data to write to the CSV file.

    Returns:
        None.
    """
    with open(filepath, mode="w") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerows(csv_table)

    logger.debug(f"CSV_WRITE: {filepath}")
    logger.debug(f"CSV_WRITE_TABLE: {csv_table}")


def read_write_csv(
    filepath: Union[str, Path],
    csv_table: list[list[str]],
) -> list[list[str]]:
    try:
        return read_csv(filepath)
    except (FileNotFoundError,) as error:
        logger.debug(f"CSV_READ_WRITE: {error}")

        write_csv(filepath, csv_table)
        return read_csv(filepath)


def print_csv(csv_table: list[list[str]], width: int = 240) -> None:
    """Prints a formatted table of the CSV contents to the console.

    Args:
        csv_table: The table to print.
        width (optional): The width of the table. Defaults to 240.
    """
    tt = texttable.Texttable(width)
    tt.set_deco(texttable.Texttable.HEADER)
    tt.set_cols_dtype(["t"] * len(csv_table[0]))
    tt.set_cols_align(["r"] * len(csv_table[0]))
    tt.add_rows(csv_table)
    print(tt.draw())
