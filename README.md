# Archive

Convert brokerage CSV transactions to a unified format, Calculate gains and
losses, and create Form-8949 for filing taxes.

## License

```plaintext
Archive - Convert brokerage CSV transactions to a unified format, Calculate gains and losses, and create Form-8949 for filing taxes.
Copyright (C) 2022  teleprint-me

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.
```

## Supported Exchanges

Archive currently supports the following exchanges:

-   Coinbase (`coinbase`)
-   Coinbase Pro (`coinbase_pro`)
-   Kraken (`kraken`)
-   Robinhood (`robinhood`)

You can implement your own parsers for additional exchanges by following the
provided examples and updating the `parser_factory` in `archive/ir/factory.py`.

## Gains and Losses Calculations

Gains and losses are calculated as a
[Weighted Average Cost](https://www.investopedia.com/ask/answers/09/weighted-average-fifo-lilo-accounting.asp).

## Installation and initialization

```shell
git clone https://github.com/teleprint-me/archive.git
cd archive
chmod +x init.sh
./init.sh
```

## Usage

⚠️ **USE AT YOUR OWN RISK!**

🚨 **ALWAYS AUDIT THE OUTPUT!**

### main.py

The `main.py` script processes input CSV files for each exchange, generates
intermediate results (IR), processes the IR transactions to generate gains and
losses (GL) transactions, and then processes the GL transactions to generate the
Form-8949 CSV output. Additionally, it also processes the Robinhood Form-1099
CSV if provided.

#### Arguments

-   `--exchange-file`: A list of exchange names and file paths for their
    respective input CSV files.
    -   Allowed exchanges are: `coinbase_transaction`, `coinbase_pro_fill`,
        `coinbase_pro_account`, `kraken_trade`, and `kraken_ledger`.
-   `--robinhood1099`: The file path for the Robinhood 1099 CSV file (optional).
-   `--asset`: The base asset symbol (default is "BTC").
-   `--label`: A label to be appended to the output file name (default is
    "bitcoin").
-   `--start-date`: The start date for transactions to be included (optional).
-   `--end-date`: The end date for transactions to be included (optional).

#### Example

```sh
$ python main.py --exchange-file coinbase_transaction data/in/coinbase.csv --robinhood1099 data/in/robinhood-1099.csv --asset BTC
```

#### Note

Gains and losses are calculated as a
[Weighted Average Cost](https://www.investopedia.com/ask/answers/09/weighted-average-fifo-lilo-accounting.asp).

### build_ir.py

The `build_ir.py` script processes exchange CSV files to generate intermediate
results (IR) in a unified format.

#### Arguments

-   `--exchange-file`: A list of exchange names and file paths for their
    respective input CSV files.
    -   Allowed exchanges are: `coinbase_transaction`, `coinbase_pro_fill`,
        `coinbase_pro_account`, `kraken_trade`, and `kraken_ledger`.
        -   `coinbase_pro_account` only handles conversions.
        -   `kraken_ledger` only handles staking.
-   `--asset`: The base asset symbol (default is "BTC").
-   `--label`: A label to be appended to the output file name (default is
    "bitcoin").

#### Example

```sh
$ python build_ir.py --exchange-file exchange_name data/in/exchange_name.csv --asset BTC
```

### build_gl.py

The `build_gl.py` script processes IR transactions and generates GL transactions
in a unified format.

#### Arguments

-   `directory`: The directory containing the IR CSV files.
-   `--asset`: The base asset symbol (default is "BTC").
-   `--label`: A label to be appended to the output file name (default is
    "bitcoin").

#### Example

```sh
$ python build_gl.py data/ir/ --asset BTC
```

#### Note

Gains and losses are calculated as a
[Weighted Average Cost](https://www.investopedia.com/ask/answers/09/weighted-average-fifo-lilo-accounting.asp).

### build_f8949.py

The `build_f8949.py` script processes GL transactions and generates a Form 8949
CSV output.

#### Arguments

-   `filepath`: The filepath to the gains and losses CSV file.
-   `--label`: A label to append to the output file name (default is "bitcoin").
-   `--start_date`: The start date for the range of transactions (YYYY-MM-DD,
    optional).
-   `--end_date`: The end date for the range of transactions (YYYY-MM-DD,
    optional).

#### Example

```sh
$ python build_f8949.py data/gl/gl-bitcoin.csv --start_date 2021-01-01 --end_date 2021-12-31
```

### build_f1099.py

The `build_f1099.py` script merges the Form 8949 and Robinhood 1099 datasets.

#### Arguments

-   `--form8949`: The filepath to the existing Form 8949 CSV file.
-   `--robinhood1099`: The filepath to the Robinhood 1099 CSV file.
-   `--asset`: The base asset symbol to be included (e.g., BTC, ETH; default is
    "BTC").
-   `--label`: A label to append to the output file name (default is "bitcoin").
-   `--start_date`: The start date for the range of transactions (YYYY-MM-DD,
    optional).
-   `--end_date`: The end date for the range of transactions (YYYY-MM-DD,
    optional).

#### Example

```sh
$ python build_f1099.py --form8949 data/f8949/f8949-bitcoin.csv --robinhood1099 data/in/robinhood-1099.csv --asset BTC
```

### link_f8949.py

The `link_f8949.py` script joins the Form-8949 and Robinhood-1099 datasets and
outputs a single unified Form-8949.

#### Arguments

-   `--form8949`: The directory containing the Form-8949 files.
-   `--form1099`: The directory containing the Form-1099 CSV files.
-   `--year YEAR`: The year for the range of transactions (YYYY).
-   `--label`: A label to append to the output file name.

#### Example

```sh
$ python link_f8949.py --form8949 data/f8949 --form1099 data/f1099 --year 2021
```

### Google Sheets Scripts

The included `scripts/` directory contains 2 scripts for formatting the contents of the output in Google Sheets.

Each script is labeled as such:

- `format-f8949.js` - Formats the current active sheet containing Form-8949 data. 
- `format-gl.js` - Formats the current active sheet containing Gains and Losses data.

1. Create a new sheet.
2. File > Import > Upload > Browse > Open > Import Location: Insert new sheet(s) > Import data
3. Extensions > Apps Script > Code.gs > Copy and paste the relevant scripts > Save > Run (Follow security prompts)

Note that `format-gl.gs` depends on `format-f8949.gs` as they share some dependent variables for consistency.
