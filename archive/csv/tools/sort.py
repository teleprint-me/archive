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
