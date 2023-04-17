**Disclaimer:**

_I am a **programmer** and I am **NOT** an accredited financial expert. You should seek out an accredited financial expert for making serious investment decisions. Do NOT take investment advice from random internet strangers and always do your own research._

# Data Tracking

Data is usually tracked as it's created alongside the execution of these strategies. The tracked data creates a data set. A **data set** is a collection of data. [[3]](https://en.wikipedia.org/wiki/Data_set) This data is then [tabulated](https://www.merriam-webster.com/dictionary/tabulate). The tabulated data consists of columns where every column of a table represents a variable. Each row corresponds to a given record of the data set. This becomes a data table. [[4]](https://en.wikipedia.org/wiki/Table_(database))

A table cell is one grouping within a table used for storing information or data. Cells are grouped horizontally (rows of cells) and vertically (columns of cells). Each cell contains information relating to the combination of the row and column headings it is [collinear](https://www.merriam-webster.com/dictionary/collinear) with. [[5]](https://en.wikipedia.org/wiki/Table_cell) You use a series of simple mathematical formulas to determine the value that resides within each cell. Each cell may be the result of a constant or variable.

## Tabulating data sets

---

A table may contain any set of columns that is relevant to the data set. This causes every table to vary from the way it may be utilized by another investor. The table columns will typically be chosen to reflect the information the investor is interested in.

We will set up our own custom table and then build off of it starting with Cost Averaging, then moving onto Dynamic Cost Averaging, and then finish off with Value Averaging.

Our initial table will be kept as simple as possible and then we'll add to it once we've completed covering [First Principles](https://fs.blog/first-principles/).

We'll use Bitcoin's 2020 _closing prices_ as our sample data set. This will allow us to _paper trade_ with the data set provided from 2020. The volatility in Bitcoin will help showcase how each strategy performs. Bitcoin will be our _base currency_ and the Dollar will be our _quote currency_. The base and quote product create the _trade pair_ "_BTC-USD_".

A **trade pair** refers to the two currencies that are being traded against each other in a currency exchange. In this case, BTC-USD represents a trade in which Bitcoin (BTC) is being traded for United States dollars (USD).

The **base currency** is the first currency listed in a _currency pair_ and it is the currency that you are buying or selling. In the BTC-USD trade pair, BTC is the base currency and you are either buying or selling Bitcoin.

The **quote currency** is the second currency listed in a _currency pair_, and it is the currency that you are using to buy or sell the base currency. In the BTC-USD trade pair, USD is the quote currency and you are buying or selling Bitcoin with US dollars.

## Gathering data sets

---

The following data set represents the _closing prices_ for Bitcoin for the _first day of each month_ in the year 2020.

| Month | Day | Year | Closing Price |
| ----- | --- | ---- | ------------- |
| Jan   | 01  | 2020 | $9334.98      |
| Feb   | 01  | 2020 | $8505.07      |
| Mar   | 01  | 2020 | $6424.35      |
| Apr   | 01  | 2020 | $8624.28      |
| May   | 01  | 2020 | $9446.57      |
| Jun   | 01  | 2020 | $9136.20      |
| Jul   | 01  | 2020 | $11351.62     |
| Aug   | 01  | 2020 | $11655.00     |
| Sep   | 01  | 2020 | $10779.63     |
| Oct   | 01  | 2020 | $13804.81     |
| Nov   | 01  | 2020 | $19713.94     |
| Dec   | 01  | 2020 | $28990.08     |

Here, we use a smaller data set to keep things simple for now. We will use the MM/DD/YY format in the proceeding examples as well as expand on this data set later on to include 2021 and 2022 monthly market prices as well.

## Defining data sets

---

Our columns will be the following: Date, Market Price, Principle Amount, Target Value, Current Value, Order Size, Total Order Size, and Time Period.

-   **Date** will represent the date for the current record (row).
-   **Market Price** will represent the current price at which each unit of
    Bitcoin was bought or sold.
-   **Principle Amount** will represent the amount of money that was put into
    the investment.
-   **Target Value** will represent our desired projected value for our current
    overall investment.
-   **Current Value** will represent the most recent total value of our
    investment.
-   **Order Size** will represent the amount that we purchased.
-   **Total Order Size** will represent the total amount that we purchased.
-   **Time Period** will represent the total number of times we've invested.

_Principle Amount_ will be the only _constant value_. A **constant value** is a
_fixed value_. A fixed value is a value that does not change. The rest will be
_variable_. A variable represents an unknown, or yet to be calculated, value.
The variables will be calculated based on whether certain _conditions_ are met.

I like using small numbers and using multiples of 10 tends to keep things very
simple. This allows us to catch errors when we make mistakes. The mistake will
be more apparent and easy to backtrack as a result. Our _Principle Amount_ will
be $10 as a result of this reasoning.

The _Market Price_ for the _Date_ Jan 01, 2020 was $9334.98.

The following will be the outline for our first record entry:

| Date     | Market Price | Current Target | Current Value | Principle Amount | Order Size | Total Order Size | Time Period |
| -------- | ------------ | -------------- | ------------- | ---------------- | ---------- | ---------------- | ----------- |
| 01/01/20 | $9334.98     |                |               | $10              |            |                  |             |

This allows us to set up our first record.

We also need to define how we will calculate the rest of the columns.

-   **Time Period** = 1 + Time Period
-   **Current Target** = Principle Amount \* Time Period
-   **Order Size** = Principle Amount / Market Price
-   **Total Order Size** = Order Size + Previous Total Order Size
-   **Current Value** = Market Price \* Previous Total Order Size

-   If there is no **Previous Total Order Size**, then set **Pervious Total
    Order Size** to **0**.
-   If there is no previous **Time Period**, then set **Time Period** to **0**.

Let's start by setting both _Previous Total Order Size_ and _Time Period_ to 0.

-   **Previous Total Order Size** = 0
-   **Time Period** = 0

Now we can calculate our _Current Target_, _Current Value_, _Order Size_, and
_Time Period_.

-   **Time Period** = 1 + 0 = 1
-   **Current Target** = 10 \* 1 = 10
-   **Order Size** = 10 / 9334.98 ≈ 0.00107124
-   **Total Order Size** = 0.00107124 + 0 ≈ 0.00107124
-   **Current Value** = 9334.98 \* 0 = 0

The following would be the result for our first record entry:

| Date     | Market Price | Current Target | Current Value | Principle Amount | Order Size | Total Order Size | Time Period |
| -------- | ------------ | -------------- | ------------- | ---------------- | ---------- | ---------------- | ----------- |
| 01/01/20 | $9334.98     | $10            | 0             | $10              | 0.00107124 | 0.00107124       | 1           |

It's important to keep in mind that **Current Value** evaluates to **0** because
_we had no previous investment_. This will only ever be true for the first
record entry while operating under the assumption that the investment remains
_solvent_.

Let's create the second record to see how each cell is evaluated and then
recorded.

| Date     | Market Price | Current Target | Current Value | Principle Amount | Order Size | Total Order Size | Time Period |
| -------- | ------------ | -------------- | ------------- | ---------------- | ---------- | ---------------- | ----------- |
| 01/01/20 | $9334.98     | $10            | 0             | $10              | 0.00107124 | 0.00107124       | 1           |
| 02/01/20 | $8505.07     |                |               | $10              |            |                  |             |

All we have to do is follow the same pattern as before while updating each
variable using the given information.

-   **Time Period** = 1 + 1 = 2
-   **Current Target** = 10 \* 2 = 20
-   **Order Size** = 10 / 8505.07 ≈ 0.00117577
-   **Total Order Size** = 0.00117577 + 0.00107124 ≈ 0.00224701
-   **Current Value** = 8505.07 \* 0.00107124 = 9.11

| Date     | Market Price | Current Target | Current Value | Principle Amount | Order Size | Total Order Size | Time Period |
| -------- | ------------ | -------------- | ------------- | ---------------- | ---------- | ---------------- | ----------- |
| 01/01/20 | $9334.98     | $10            | 0             | $10              | 0.00107124 | 0.00107124       | 1           |
| 02/01/20 | $8505.07     | $20            | $9.11         | $10              | 0.00117577 | 0.00224701       | 2           |

We follow these steps every time we invest from this point forward and never
deviate from the investment plan.

This table isn't displaying our gain or loss. Let's define a new expression to
evaluate our gain or loss in a new column. We can place it in between our
**Current Value** and **Principle Amount** columns.

-   **Gain/Loss** = Current Value - Previous Current Target

-   If there is no **Current Value**, then set **Current Value** to **0**.
-   If there is no **Previous Current Target**, then set **Previous Current
    Target** to **0**.

-   A **Gain** is represented as a _positive value_ (\+) while a **Loss** is
    represented as a _negative value_ (\-).

-   First Row: **Gain/Loss** = 0 - 0 = 0
-   Second Row: **Gain/Loss** = 9.11 - 10 ≈ -0.89

| Date     | Market Price | Current Target | Current Value | Gain/Loss | Principle Amount | Order Size | Total Order Size | Time Period |
| -------- | ------------ | -------------- | ------------- | --------- | ---------------- | ---------- | ---------------- | ----------- |
| 01/01/20 | $9334.98     | $10            | 0             | 0         | $10              | 0.00107124 | 0.00107124       | 1           |
| 02/01/20 | $8505.07     | $20            | $9.11         | -$0.89    | $10              | 0.00117577 | 0.00224701       | 2           |
