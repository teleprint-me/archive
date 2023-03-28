from archive.csv.coinbase.ir import get_coinbase_ir_list
from archive.csv.coinbase.scanner.builder import build_coinbase_transactions
from archive.csv.ir.builder import build_ir_csv_table
from archive.csv.tools import print_csv, sort_csv

if __name__ == "__main__":
    file_path = "data/in/coinbase-transactions.csv"
    included_assets = ["BTC"]
    excluded_types = ["Send", "Receive"]

    transactions = build_coinbase_transactions(file_path)
    ir_transactions = get_coinbase_ir_list(
        transactions, included_assets, excluded_types
    )
    csv_ir_transactions = build_ir_csv_table(ir_transactions)
    csv_sorted = sort_csv(csv_ir_transactions, column=2)
    print_csv(csv_sorted)
