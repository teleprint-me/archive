**Disclaimer:**

_**I am a programmer and I am NOT an accredited financial expert. You should
seek out an accredited financial expert for making serious investment decisions.
Do NOT take investment advice from random internet strangers and always do your
own research.**_

# Dynamic Cost Averaging

Dynamic Cost Averaging (DCA) is a variation of Cost Averaging that encourages
both buying and selling. Like Cost Averaging, DCA involves setting a Principal
Amount and purchasing an asset at a regular interval, called the Interval.
However, DCA also includes selling assets when certain conditions are met.

In DCA, a Target Value helps determine the amount to buy or sell based on a
Multiplier of the Principal Amount. This Multiplier falls within a range defined
by the Min Multiplier and Max Multiplier. These factors and variables can be
customized by the user. Let's briefly describe each term:

-   Principal Amount: The initial investment or the base amount for purchasing
    the asset.
-   Interval: The regular interval at which the asset is bought or sold.
-   Target Value: A predefined value that helps determine when to buy or sell.
-   Multiplier: A multiplier applied to the Principal Amount to calculate the
    buying or selling amount.
-   Min Multiplier and Max Multiplier: The lower and upper bounds of the
    Multiplier range, respectively.

# Algorithm

We need to define our columns: Datetime, Market Price, Current Target, Current
Value, Principal Amount, Multiplier, Trade Amount, Total Trade Amount, Order
Size, Total Order Size, and Interval. This will allow us to keep track of the
relevant data and show the evaluated expressions as its set of results.

We define the sequence of steps, as well as the expressions used, to evaluate
each value as the following:

1.  Define Principal Amount

        Principal Amount = Constant Float Value

2.  Define Multiplier Range

        Min Multiplier = 1 (sets lower limit)
        Max Multiplier = Constant Integer Value greater than Min Multiplier sets upper limit (default is 5)

3.  Get Datetime

        Datetime = Current Date

4.  Get Market Price

        Market Price = Current Market Price

5.  Get Interval

        IF no previous records
            THEN Interval = 1
        ELSE
            Interval = Previous Record Interval + 1

6.  Get Current Target

        Current Target = Principal Amount * Interval

7.  Get Previous Total Order Size

        IF no previous records
            THEN Previous Total Order Size = 0
        ELSE
            Previous Total Order Size = sum of Order Size column for all previous records

8.  Get Order Size

        Order Size = Principal Amount / Market Price

9.  Get Total Order Size

        Total Order Size = Order Size + Previous Total Order Size

10. Get Current Value

        Current Value = Market Price * Previous Total Order Size

11. Get Multiplier

    How much should be bought or sold to get back to the Target Value.

        Target Difference = Current Target - Current Value

    Multiplier represents a value that is used to determine the size of the next
    trade.

        Multiplier = Target Difference / Principal Amount

    We also need to enforce the Min Multiplier and Max Multiplier limits.

        IF Multiplier = 0
            THEN RETURN 1
        IF Multiplier > Max Multiplier
            THEN RETURN Max Multiplier
        IF Multiplier < -Max Multiplier
            THEN RETURN -Max Multiplier
        RETURN max(Min Multiplier, min(Multiplier, Max Multiplier))

12. Get Trade Amount

        Trade Amount = Multiplier * Principal Amount

13. Get Previous Total Trade Amount

        IF no previous records
            THEN Previous Total Trade Amount = 0
        ELSE
            Previous Total Trade Amount = sum of Trade Amount column for all previous records

14. Get Total Trade Amount

        Total Trade Amount = Trade Amount + Previous Total Trade Amount

15. Update Previous Total Trade Amount and Previous Total Order Size

        Previous Total Trade Amount = Total Trade Amount
        Previous Total Order Size = Total Order Size

## Walkthrough

I want to paper trade a Value Averaging strategy, investing $10 per month in the
BTC-USD trading pair over a 1-year period. I will make the investments on the
first day of each month in 2020.

The smallest units for US dollars are denominated in "cents" and will use a
precision of:

        1 * 10 ^ -2 = 0.01

The smallest units for Bitcoin are denominated in "satoshis" and will use a
precision of:

        1 * 10 ^ -8 = 0.00000001

### Creating the Initial Record

Let's initialize the table and calculate the first record:

1.  Initialize Interval, Previous Total Order Size, and Previous Total Trade
    Amount. There are no previous records and we set the following variables as
    a result. This omits steps 5 (Set or Calculate Interval), 7 (Set or
    Calculate Previous Total Order Size), and step 13 (Get Previous Total Trade
    Amount).

        Interval = 1
        Previous Total Order Size = 0
        Previous Total Trade Amount = 0

2.  Define the Multiplier Range for the algorithm

        Min Multiplier = 1 (sets lower limit)
        Max Multiplier = Constant Integer Value greater than Min Multiplier sets upper limit (default is 5)

        Min Multiplier = 1
        Max Multiplier = 5

3.  Set the Principal Amount for the investment

        Principal Amount = Constant Float Value
        Principal Amount = 10.00

4.  Initialize Datetime with the date of the first record

        Datetime = Current Date
        Datetime = "2020-01-01"

5.  Get the Market Price for the first record

        Market Price = Current Market Price
        Market Price = 9334.98

6.  Calculate the Current Target

        Current Target = Principal Amount * Interval
        Current Target = 10 * 1 = 10

7.  Calculate the Order Size

        Order Size = Principal Amount / Market Price
        Order Size = 10 / 9334.98 ≈ 0.0010712395741608446 ≈ 0.00107124

8.  Calculate the Total Order Size

        Total Order Size = Order Size + Previous Total Order Size
        Total Order Size = 0.00107124 + 0 = 0.00107124

9.  Calculate the Current Value

        Current Value = Market Price * Previous Total Order Size
        Current Value = 9334.98 * 0 = 0

10. Calculate the Multiplier

    Determine how much should be bought or sold to get back to the Target Value.

    Target Difference = Current Target - Current Value Target Difference = 10 -
    0 = 10

    Multiplier represents a value that is used to determine the size of the next
    trade.

        Multiplier = Target Difference / Principal Amount
        Multiplier = 10 / 10 = 1

    Enforce the Min Multiplier and Max Multiplier limits.

        IF Multiplier = 0
            THEN RETURN 1
        IF Multiplier > Max Multiplier
            THEN RETURN Max Multiplier
        IF Multiplier < -Max Multiplier
            THEN RETURN -Max Multiplier
        RETURN max(Min Multiplier, min(Multiplier, Max Multiplier))

    In this case, the Multiplier is within the limits:

        Multiplier = 1

11. Get Trade Amount

        Trade Amount = Multiplier * Principal Amount
        Trade Amount = 1 * 10 = 10

-   Example of how to calculate Target Difference, Multiplier, and Trade Amount
    to buy:

        Target Difference = 20 - 9.11 = 10.89 (positive value is a buy signal)
        Multiplier = 10.89 / 10 ≈ 1.09 ≈ 1 (rounded to the nearest integer)
        Trade Amount = 1 * 10 = 10 (buy $10 worth)

-   Example of how to calculate Target Difference, Multiplier, and Trade Amount
    to sell:

        Target Difference = 20 - 30.24 = -10.24 (negative value is a sell signal)
        Multiplier = -10.24 / 10 ≈ -1.024 ≈ -1 (rounded to the nearest integer)
        Trade Amount = -1 * 10 = -10 (sell $10 worth)

12. Get Previous Total Trade Amount

        Since there are no previous records:
        Previous Total Trade Amount = 0

13. Get Total Trade Amount

        Total Trade Amount = Trade Amount + Previous Total Trade Amount
        Total Trade Amount = 10 + 0 = 10

14. Update Previous Total Trade Amount and Previous Total Order Size

        Previous Total Trade Amount = Total Trade Amount
        Previous Total Trade Amount = 10

        Previous Total Order Size = Total Order Size
        Previous Total Order Size = 0.00107124

### Calculating Record Entries

Now we can tabulate our Current Target, Current Value, Multiplier, Trade Amount,
Total Trade Amount, Principal Amount, Order Size, Total Order Size, and
Interval. This allows us to track the progress of our investment and gives us a
bird's-eye view of its performance over time.

Holding is usually enforced via a minimum or maximum trade amount and varies
amongst brokerages and is outside of the scope of this strategy.

**Note:** When implementing this strategy, be aware of the specific minimum and
maximum trade amounts enforced by the exchange you are using. These limits can
affect the execution of trades and should be taken into account when developing
your trading bot. Consider adding an environment variable or configuration
setting to handle these requirements, allowing you to easily adjust the values
based on the exchange's rules and restrictions.

| Datetime   | Market Price | Current Target | Current Value | Principal Amount | Multiplier | Trade Amount | Total Trade Amount | Order Size | Total Order Size | Interval |
| ---------- | ------------ | -------------- | ------------- | ---------------- | ---------- | ------------ | ------------------ | ---------- | ---------------- | -------- |
| 2020-01-01 | 9334.98      | 10.00          | 0.00          | 10.00            | 1.00       | 10.00        | 10.00              | 0.00107124 | 0.00107124       | 1        |
| 2020-02-01 | 9334.98      | 20.00          |               |                  |            |              |                    |            |                  | 2        |

---

| Date       | Market Price | Current Target | Current Value | Principal Amount | Factor Purchase | Factor Amount | Total Factor Amount | Order Size | Total Order Size | Time Period |
| ---------- | ------------ | -------------- | ------------- | ---------------- | --------------- | ------------- | ------------------- | ---------- | ---------------- | ----------- |
| 2020-01-01 | 7174.33      | 100.00         | 0.00          | 100.00           | 1.00            | 100.00        | 100.00              | 0.01393858 | 0.01393858       | 1           |
| 2020-02-01 | 9380.18      | 200.00         | 130.75        | 100.00           | 1.00            | 100.00        | 200.00              | 0.01066078 | 0.02459936       | 2           |
| 2020-03-01 | 8522.31      | 300.00         | 209.64        | 100.00           | 1.00            | 100.00        | 300.00              | 0.01173391 | 0.03633327       | 3           |
| 2020-04-01 | 6666.11      | 400.00         | 242.20        | 100.00           | 2.00            | 200.00        | 500.00              | 0.01500125 | 0.05133452       | 4           |
| 2020-05-01 | 8829.42      | 500.00         | 453.25        | 100.00           | 1.00            | 100.00        | 600.00              | 0.01132577 | 0.06266029       | 5           |
| 2020-06-01 | 10208.96     | 600.00         | 639.70        | 100.00           | 1.00            | 100.00        | 700.00              | 0.00979532 | 0.07245561       | 6           |
| 2020-07-01 | 9239.97      | 700.00         | 669.49        | 100.00           | 1.00            | 100.00        | 800.00              | 0.01082255 | 0.08327816       | 7           |
| 2020-08-01 | 11810.07     | 800.00         | 983.52        | 100.00           | 1.00            | 100.00        | 900.00              | 0.00846735 | 0.09174551       | 8           |
| 2020-09-01 | 11924.22     | 900.00         | 1093.99       | 100.00           | 1.00            | 100.00        | 1000.00             | 0.00838629 | 0.10013180       | 9           |
| 2020-10-01 | 10617.63     | 1000.00        | 1063.16       | 100.00           | 1.00            | 100.00        | 1100.00             | 0.00941830 | 0.10955010       | 10          |
| 2020-11-01 | 13771.59     | 1100.00        | 1508.68       | 100.00           | 1.00            | 100.00        | 1200.00             | 0.00726133 | 0.11681142       | 11          |
| 2020-12-01 | 18782.97     | 1200.00        | 2194.07       | 100.00           | 1.00            | 100.00        | 1300.00             | 0.00532397 | 0.12213539       | 12          |
