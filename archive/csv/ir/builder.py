from archive.csv.ir.transaction import IRTransaction


def build_ir_csv_row(
    ir_transaction: IRTransaction,
) -> list[str]:
    return [
        ir_transaction.exchange,
        ir_transaction.product,
        ir_transaction.datetime,
        ir_transaction.transaction_type,
        f"{float(ir_transaction.order_size):.8f}",
        f"{float(ir_transaction.market_price):.8f}",
        f"{float(ir_transaction.order_fee):.8f}",
        ir_transaction.order_note,
    ]


def build_ir_csv_table(
    ir_table: list[IRTransaction],
) -> list[list[str]]:
    header = [
        [
            "Exchange",
            "Product",
            "Datetime",
            "Transaction Type",
            "Order Size",
            "Market Price",
            "Order Fee",
            "Order Note",
        ]
    ]
    transactions = [build_ir_csv_row(tx) for tx in ir_table]
    return header + transactions
