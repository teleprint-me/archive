**Disclaimer:**

_**I am a programmer and I am NOT an accredited financial expert. You should
seek out an accredited financial expert for making serious investment decisions.
Do NOT take investment advice from random internet strangers and always do your
own research**._

📝 **THIS SOFTWARE IS UNDER ACTIVE DEVELOPMENT AND IS SUBJECT TO CHANGE**

⚠️ **USE THIS SOFTWARE AT YOUR OWN RISK!**

🚨 **ALWAYS AUDIT THE OUTPUT!**

# Archive

Command-line tools for managing cryptocurrency investments.

## License

```plaintext
Archive - Command-line tools for managing cryptocurrency investments.
Copyright (C) 2023  teleprint-me

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

## Features

-   [x] Generate Intermediary Representations (IR) from CSV transaction data.
-   [x] Generate Gains and Losses (GL) from IR data.
-   [x] Generate Form-8949 from GL data.
-   [x] Generate Form-8949 from Form-1099.
-   [ ] Manage `systemd` services and timers.
-   [x] Generate Cost Average transactions.
-   [ ] Generate Dynamic Cost Average transactions.
-   [ ] Generate Value Average transactions.

## Supported Exchanges

Archive currently supports the following exchanges:

-   Coinbase (`coinbase`)
-   Coinbase Pro (`coinbase_pro`)
-   Kraken (`kraken`)
-   Robinhood (`robinhood`)

You can implement your own parsers for additional exchanges by following the
provided examples and updating the `parser_factory` in `archive/ir/factory.py`.

## Calculations

-   Gains and losses are calculated by a
    [Weighted Average](https://www.investopedia.com/ask/answers/09/weighted-average-fifo-lilo-accounting.asp).
-   Cost Averaging is determined by the principal amount.
-   Value Averaging is determined by the principal amount, interest rate, and
    interval.

## Installation and initialization

```sh
git clone https://github.com/teleprint-me/archive.git
cd archive
chmod +x init.sh
./init.sh
```

## Usage

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
python main.py --exchange-file coinbase_transaction data/in/coinbase.csv --robinhood1099 data/in/robinhood-1099.csv --asset BTC
```

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
python build_ir.py --exchange-file exchange_name data/in/exchange_name.csv --asset BTC
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
python build_gl.py data/ir/ --asset BTC
```

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
python build_f8949.py data/gl/gl-bitcoin.csv --start_date 2021-01-01 --end_date 2021-12-31
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
python build_f1099.py --form8949 data/f8949/f8949-bitcoin.csv --robinhood1099 data/in/robinhood-1099.csv --asset BTC
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
python link_f8949.py --form8949 data/f8949 --form1099 data/f1099 --year 2021
```

### env_manager.py

The `env_manager.py` script manages environment variables.

#### Arguments

-   `set`: Set a key-value pair.

```sh
python env_manager.py set EXCHANGE coinbase
```

-   `unset`: Unset a key.

```sh
python env_manager.py unset EXCHANGE
```

-   `--env-file`: Path the environment file (default: `.env`)

```sh
mkdir -pv ~/.config/archive
python env_manager.py -f ~/.config/archive/.env set EXCHANGE coinbase
```

### Environment Variables

Here is a list of environment variables that can be set using the
`env_manager.py` script:

-   `EXCHANGE`: The name of the exchange (e.g. 'coinbase', 'kraken', etc.).
-   `API_KEY`: The API key for the exchange (if applicable).
-   `API_SECRET`: The API secret for the exchange (if applicable).
-   `PASSPHRASE`: The passphrase for the exchange (if applicable).
-   `PRODUCT_ID`: The product ID of the cryptocurrency pair (e.g. 'BTC-USD',
    'ETH-USD', etc.).
-   `PRINCIPAL_AMOUNT`: The amount of money to invest in each purchase.
-   `FREQUENCY`: The frequency of the averaging strategy (e.g. 'daily',
    'weekly', 'monthly').
-   `INTEREST_RATE`: The interest rate for calculating the growth rate in the
    value averaging strategy.
-   `MAX_FACTOR`: The maximum factor for dynamic averaging (default is 5).

You can set or unset these variables using the `env_manager.py` script as shown
in the previous section. Make sure to store the variables in a secure location,
as they may contain sensitive information like API keys and secrets.

## Bots

### Cost Average Bot

The Cost Average Bot helps you automate your dollar-cost averaging strategy by
placing orders at a specified frequency.

To set up the Cost Average Bot, you need to have the environment variables
configured (as described in the Environment Variables section). Ensure you have
the `EXCHANGE`, `PRODUCT_ID`, and `PRINCIPAL_AMOUNT` variables set.

To execute the bot manually, run the following command:

```sh
python post_cost_average.py
```

This will simulate an order based on your configured environment variables and
update the records file without actually placing the order. By default, the
records file is `data/average/cost_average_records.csv`. You can change the file
path by passing the `-f` or `--file` option followed by the desired file path.

To actually place the order using the configured exchange API, use the `-x` or
`--execute` flag:

```sh
python post_cost_average.py -x
```

Please note that executing the script with the `-x` flag will place a real order
and update the records file accordingly. Use this option with caution and ensure
your environment variables are configured correctly.

### Dynamic Cost Average Bot

    TODO

### Value Average Bot

    TODO

### Manual Setup

The service defines the task to be executed (running your script), and the timer
specifies when and how often the service should be activated.

Here's a step-by-step guide to setting up a service and timer to automate your
script:

1. **Create a service unit file**: Write a `.service` file that defines the
   service responsible for running your averaging script. In this file, you'll
   specify the command to execute your script (using the appropriate Python
   interpreter) and any required environment variables.

```service
[Unit]
Description=Automated Averaging Service

[Service]
Type=simple
ExecStart=/path/to/python /path/to/your/averaging_script.py
User=username
EnvironmentFile=/path/to/your/env/file

[Install]
WantedBy=multi-user.target
```

2. **Create a timer unit file**: Write a `.timer` file that defines the timer
   responsible for activating your service. In this file, you'll specify the
   schedule (e.g., daily, weekly, monthly) and the service to be activated.

```service
[Unit]
Description=Automated Averaging Timer

[Timer]
OnCalendar=daily
Persistent=true
Unit=your_averaging_service.service

[Install]
WantedBy=timers.target
```

3. **Install and enable the service and timer**: Copy the service and timer unit
   files to the appropriate systemd directory (usually `/etc/systemd/system/`)
   and use `systemctl` to enable and start the timer. This will ensure that your
   service is executed according to the schedule specified in the timer.

```sh
sudo cp your_averaging_service.service /etc/systemd/system/
sudo cp your_averaging_timer.timer /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable your_averaging_timer.timer
sudo systemctl start your_averaging_timer.timer
```

4. **Check the status and logs**: To ensure that your service and timer are
   operating as intended, use `systemctl` to check their status and logs. The
   `status` subcommand will show you the current state of the service or timer,
   while the `journalctl` command will display the logs generated by your
   script.

```sh
systemctl status your_averaging_service.service
systemctl status your_averaging_timer.timer

journalctl -u your_averaging_service.service
```

By following these steps, you can create a systemd service and timer to automate
your averaging script and ensure it runs according to the desired schedule.
Remember to adjust the paths, names, and schedule to match your specific
requirements.

### Automated Setup

To set up the automated averaging service and timer, follow these steps:

1. Update the paths in `scripts/shell/setup_averaging_service.sh` and
   `scripts/shell/setup_averaging_timer.sh` to match your system's
   configuration:

-   `POST_AVERAGING_PATH`: Path to the `post_average.py` script.
-   `VENV_PATH`: Path to your virtual environment directory.
-   `ENV_FILE`: Path to your environment variables file (e.g., `.env`).

2. Run the `setup_averaging_service.sh` script to create and start the averaging
   service:

```sh
bash scripts/shell/setup_averaging_service.sh
```

This will create a systemd service that runs the `post_average.py` script. It
will also start the service and print its status.

3. Run the `setup_averaging_timer.sh` script to create and start the averaging
   timer:

```sh
bash scripts/shell/setup_averaging_timer.sh
```

This will create a systemd timer that triggers the averaging service at the
frequency specified in your environment variables (e.g., `FREQUENCY=weekly`). It
will also start the timer and print its status.

With these steps completed, your Averaging Bot will run automatically at the
specified frequency, executing orders based on your environment variables.

## Google Sheets Scripts

The included `scripts/` directory contains 2 scripts for formatting the contents
of the output in Google Sheets.

Each script is labeled as such:

-   `format-form-8949.js` - Formats the current active sheet containing
    Form-8949 data.
-   `format-gains-and-losses.js` - Formats the current active sheet containing
    Gains and Losses data.
-   `format-cost-average.js` - Formats the current active sheet containing Cost
    Averaging data.
-   `format-dynamic-average.js` - Formats the current active sheet containing
    Dynamic Cost Averaging data.
-   `format-value-average.js` - Formats the current active sheet containing
    Value Averaging data.

1. Create a new sheet.
2. File > Import > Upload > Browse > Open > Import Location: Insert new
   sheet(s) > Import data
3. Extensions > Apps Script > Code.gs > Copy and paste the relevant scripts >
   Save > Run (Follow security prompts)

Note that `format-gl.gs` depends on `format-f8949.gs` as they share some
dependent variables for consistency.
