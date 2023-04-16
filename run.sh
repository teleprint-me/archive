#!/usr/bin/env bash

declare STDERR="data/log/stderr.out"

declare -A assets=(
    ["USDC"]="usdcoin"
    ["DAI"]="dai"
    ["BTC"]="bitcoin"
    ["ETH"]="ethereum"
    ["LTC"]="litecoin"
    ["DOT"]="polkadot"
    ["00"]="00"
    ["1INCH"]="1inch"
    ["ALGO"]="algorand"
    ["ALEPH"]="aleph"
    ["AMP"]="amp"
    ["ANKR"]="ankr"
    ["AUCTION"]="auction"
    ["BAL"]="balancer"
    ["BAND"]="band"
    ["BOND"]="bond"
    ["CGLD"]="cgld"
    ["CHZ"]="chiliz"
    ["CLV"]="clover"
    ["COMP"]="compound"
    ["CTSI"]="cartesi"
    ["CTX"]="cryptex"
    ["EOS"]="eos"
    ["ERN"]="ethernity"
    ["FET"]="fetchai"
    ["FIL"]="filecoin"
    ["FORTH"]="forth"
    ["GAL"]="galxe"
    ["GRT"]="graph"
    ["KAVA"]="kava"
    ["LCR"]="loopring"
    ["LINK"]="chainlink"
    ["MANA"]="mana"
    ["MATIC"]="matic"
    ["MKR"]="maker"
    ["MLN"]="enzyme"
    ["NEAR"]="near"
    ["NU"]="nucypher"
    ["RNDR"]="render"
    ["SAND"]="sandbox"
    ["SKL"]="skale"
    ["UNI"]="uniswap"
    ["XCN"]="onyxcoin"
    ["XMR"]="monero"
    ["XLM"]="stellar"
    ["XRP"]="ripple"
    ["YFI"]="yearn"
    ["ZEC"]="zcash"
)

for asset in "${!assets[@]}"; do
    label="${assets[$asset]}"

    case "$asset" in
        # Add specific cases for different assets if needed
        # "SOME_ASSET")
        #    custom_command
        #    ;;
        "BTC"|"LTC"|"ETH")
            python main.py \
                --exchange-file coinbase_transaction data/in/coinbase-transaction.csv \
                --exchange-file coinbase_pro_fill data/in/coinbase-pro-fill.csv \
                --exchange-file kraken_trade data/in/kraken-trade.csv \
                --robinhood1099 data/in/robinhood-crypto-1099.csv \
                --asset "$asset" --label "$label"

            if [ $? -ne 0 ]; then
                echo "Error occurred while processing asset $asset ($label)" >> $STDERR
            fi
            ;;        
        "USDC")
            python main.py \
                --exchange-file coinbase_transaction data/in/coinbase-transaction.csv \
                --exchange-file coinbase_pro_fill data/in/coinbase-pro-fill.csv \
                --exchange-file coinbase_pro_account data/in/coinbase-pro-account.csv \
                --exchange-file kraken_trade data/in/kraken-trade.csv \
                --asset "$asset" --label "$label"
            
            if [ $? -ne 0 ]; then
                echo "Error occurred while processing asset $asset ($label)" >> $STDERR
            fi
            ;;        
        "DOT")
            python main.py \
                --exchange-file coinbase_transaction data/in/coinbase-transaction.csv \
                --exchange-file coinbase_pro_fill data/in/coinbase-pro-fill.csv \
                --exchange-file kraken_trade data/in/kraken-trade.csv \
                --exchange-file kraken_ledger data/in/kraken-ledger.csv \
                --asset "$asset" --label "$label"

            if [ $? -ne 0 ]; then
                echo "Error occurred while processing asset $asset ($label)" >> $STDERR
            fi
            ;;
        *)
            python main.py \
                --exchange-file coinbase_transaction data/in/coinbase-transaction.csv \
                --exchange-file coinbase_pro_fill data/in/coinbase-pro-fill.csv \
                --exchange-file kraken_trade data/in/kraken-trade.csv \
                --asset "$asset" --label "$label"

            if [ $? -ne 0 ]; then
                echo "Error occurred while processing asset $asset ($label)" >> $STDERR
            fi
            ;;
    esac

done

# Will run the previous tax year by default.
# e.g. If the current filing year is 2023, then it will output for 2022.
python link_f8949.py --form8949 data/f8949 --form1099 data/f1099
