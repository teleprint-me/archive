import csv
from pathlib import Path
from typing import Any

import texttable


def read_csv(filepath: str | Path) -> list[list[str]]:
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
        return csv_table


def write_csv(filepath: str | Path, csv_table: list[list[str]]):
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


def print_csv(csv_table: list[list[str]], width: int = 240):
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


def sort_csv(
    csv_table: list[list[str]], column: int = 0, reverse: bool = False
) -> list[list[str]]:
    """Sort CSV rows by a given column in ascending or descending order.

    Args:
        csv_table (list[list[str]]): The list of CSV rows to sort.
        column (int, optional): The index of the column to sort by.
        reverse (bool, optional): If True, the rows are sorted in descending order. Defaults to False.

    Returns:
        A sorted list of CSV rows.
    """
    table_temp = [csv_table[0]]
    table_sorted = sorted(
        csv_table[1:], key=lambda row: row[column], reverse=reverse
    )
    table_temp.extend(table_sorted)
    return table_temp


def sort_csv_by_header(
    csv_table: list[list[str]], reverse: bool = False
) -> list[list[str]]:
    """Sorts a CSV table by column header in ascending or descending order.

    Args:
        csv_table: The list of CSV rows to sort.
        reverse (optional): If True, the table is sorted in descending order. Defaults to False.

    Returns:
        A sorted list of CSV rows with headers in ascending or descending order.
    """
    header = csv_table[0]
    header_indices = sorted(
        range(len(header)), key=lambda i: header[i], reverse=reverse
    )
    header = [header[i] for i in header_indices]
    sorted_data = []
    for index in header_indices:
        col_data = [row[index] for row in csv_table[1:]]
        sorted_data.append(col_data)
    return [header] + list(map(list, zip(*sorted_data)))


def filter_csv(
    csv_table: list[list[str]], column: int, value: str
) -> list[list[str]]:
    """Filter the CSV table by the given column and value.

    Args:
        csv_table: The CSV table to filter.
        column: The index of the column to filter by.
        value: The value to filter by.

    Returns:
        The filtered CSV table.
    """
    filtered_table = [csv_table[0]]
    for row in csv_table[1:]:
        if row[column] == value:
            filtered_table.append(row)
    return filtered_table


def filter_csv_by_unique_values(
    csv_table: list[list[str]],
    column: int = 0,
    reverse: bool = False,
) -> list[str]:
    """Get a list of unique values in a column of the given CSV table.

    Args:
        csv_table: The CSV table to get the unique values from.
        column: The index of the column to filter unique values by.
        reverse: Sort in ascending order when False and descending when True.

    Returns:
        A list of unique values in the specified column of the CSV table.
    """
    try:
        return sorted(
            list(set(row[column] for row in csv_table[1:])), reverse=reverse
        )
    except (IndexError,):
        return []
