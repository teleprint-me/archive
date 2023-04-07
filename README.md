# Archive

Convert brokerage CSV transactions to a unified format, Calculate gains and losses, and create Form-8949 for filing taxes.

## Usage

### main.py

The `main.py` script processes input CSV files for each exchange, generates intermediate results (IR), processes the IR transactions to generate GL transactions, and then processes the GL transactions to generate the Form 8949 CSV output. Additionally, it also processes the Robinhood 1099 file if provided.

#### Arguments

-   `--exchange-file`: A list of exchange names and file paths for their respective input CSV files.
-   `--robinhood1099`: The file path for the Robinhood 1099 CSV file (optional).
-   `--asset`: The base asset symbol (default is "BTC").
-   `--label`: A label to be appended to the output file name (default is "bitcoin").
-   `--start-date`: The start date for transactions to be included (optional).
-   `--end-date`: The end date for transactions to be included (optional).

#### Example

```sh
$ python main.py --exchange-file exchange_name data/in/exchange_name.csv --robinhood1099 data/in/robinhood-1099.csv --asset BTC
```

### build_ir.py

The `build_ir.py` script processes exchange CSV files to generate intermediate results (IR) in a unified format.

#### Arguments

-   `--exchange-file`: A list of exchange names and file paths for their respective input CSV files.
-   `--asset`: The base asset symbol (default is "BTC").
-   `--label`: A label to be appended to the output file name (default is "bitcoin").

#### Example

```sh
$ python build_ir.py --exchange-file exchange_name data/in/exchange_name.csv --asset BTC
```

### build_gl.py

The `build_gl.py` script processes IR transactions and generates GL transactions in a unified format.

#### Arguments

-   `directory`: The directory containing the IR CSV files.
-   `--asset`: The base asset symbol (default is "BTC").
-   `--label`: A label to be appended to the output file name (default is "bitcoin").

#### Example

```sh
$ python build_gl.py data/ir/ --asset BTC
```

### build_f8949.py

The `build_f8949.py` script processes GL transactions and generates a Form 8949 CSV output.

#### Arguments

-   `filepath`: The filepath to the gains and losses CSV file.
-   `--label`: A label to append to the output file name (default is "bitcoin").
-   `--start_date`: The start date for the range of transactions (YYYY-MM-DD, optional).
-   `--end_date`: The end date for the range of transactions (YYYY-MM-DD, optional).

#### Example

```sh
$ python build_f8949.py data/gl/gl-bitcoin.csv --start_date 2021-01-01 --end_date 2021-12-31
```

### build_f1099.py

The `build_f1099.py` script merges the Form 8949 and Robinhood 1099 datasets.

#### Arguments

-   `--form8949`: The filepath to the existing Form 8949 CSV file.
-   `--robinhood1099`: The filepath to the Robinhood 1099 CSV file.
-   `--asset`: The base asset symbol to be included (e.g., BTC, ETH; default is "BTC").
-   `--label`: A label to append to the output file name (default is "bitcoin").
-   `--start_date`: The start date for the range of transactions (YYYY-MM-DD, optional).
-   `--end_date`: The end date for the range of transactions (YYYY-MM-DD, optional).

#### Example

```sh
$ python build_f1099.py --form8949 data/f8949/f8949-bitcoin.csv --robinhood1099 data/in/robinhood-1099.csv --asset BTC
```
