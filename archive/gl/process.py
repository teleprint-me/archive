from pathlib import Path
from typing import Union

from archive.gl.parser import parse_gl
from archive.gl.scanner import get_gl_csv_table, scan_gl_transactions
from archive.tools.io import print_csv, write_csv


def process_gl(
    asset: str, label: str, directory: Union[str, Path]
) -> Union[str, Path]:
    gl_transactions = scan_gl_transactions(asset, directory)
    gl_transactions = parse_gl(gl_transactions)

    csv_gl_transactions = get_gl_csv_table(gl_transactions)
    print_csv(csv_gl_transactions)

    output_file_path = Path(f"data/gl/gl-{label}.csv")
    write_csv(output_file_path, csv_gl_transactions)

    return output_file_path
