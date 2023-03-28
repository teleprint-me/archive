from archive.csv.coinbase.ir import build_coinbase_ir
from archive.csv.coinbase.scanner import scan_coinbase

# Add other imports for other exchanges as needed

# Configuration dictionary for each exchange
exchanges = {
    "coinbase": {
        "scan": scan_coinbase,
        "build_ir": build_coinbase_ir,
        # Add any additional output functions specific to Coinbase
    },
    # Add other exchanges with their respective functions
}
