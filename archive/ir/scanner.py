from os import scandir
from pathlib import Path

from archive.ir.transaction import IRColumns
from archive.tools.io import read_csv


def get_merged_ir_dataset(dir_path: str | Path) -> list[list[str]]:
    header: list[list[str]] = []
    table: list[list[str]] = []

    for entry in scandir(dir_path):
        if entry.is_file:
            csv_table = read_csv(entry.path)
            if not header:
                header = [csv_table[0]]
            table.extend(csv_table[1:])

    sorted_table = sorted(table, key=lambda row: row[IRColumns.DATETIME.value])

    return header + sorted_table
