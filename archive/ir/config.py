from archive.coinbase.ir import build_coinbase_ir
from archive.coinbase.scanner import scan_coinbase
from archive.coinbase_pro.ir import build_coinbase_pro_ir
from archive.coinbase_pro.scanner import scan_coinbase_pro
from archive.kraken.ir import build_kraken_ir
from archive.kraken.scanner import scan_kraken

# Configuration dictionary for each exchange
exchanges = {
    "coinbase": {
        "scan": scan_coinbase,
        "build_ir": build_coinbase_ir,
        # Add any additional output functions specific to Coinbase
    },
    "coinbase_pro": {
        "scan": scan_coinbase_pro,
        "build_ir": build_coinbase_pro_ir,
        # Add any additional output functions specific to Coinbase Pro
    },
    "kraken": {
        "scan": scan_kraken,
        "build_ir": build_kraken_ir,
        # Add any additional output functions specific to Coinbase Pro
    },
    # Add other exchanges with their respective functions
}
