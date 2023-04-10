from archive.exchange.coinbase.ir import build_coinbase_ir
from archive.exchange.coinbase.scanner import scan_coinbase
from archive.exchange.coinbase_pro.ir import build_coinbase_pro_ir
from archive.exchange.coinbase_pro.scanner import scan_coinbase_pro_fills
from archive.exchange.kraken.ir import build_kraken_ir
from archive.exchange.kraken.scanner import scan_kraken

# Configuration dictionary for each exchange
exchanges = {
    "coinbase": {
        "scan": scan_coinbase,
        "build_ir": build_coinbase_ir,
        # Add any additional output functions specific to Coinbase
    },
    "coinbase_pro": {
        "scan": scan_coinbase_pro_fills,
        "build_ir": build_coinbase_pro_ir,
        # Add any additional output functions specific to Coinbase Pro
    },
    "kraken": {
        "scan": scan_kraken,
        "build_ir": build_kraken_ir,
        # Add any additional output functions specific to Kraken
    },
    # Add other exchanges with their respective functions
}
