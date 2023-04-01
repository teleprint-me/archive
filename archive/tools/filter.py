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
