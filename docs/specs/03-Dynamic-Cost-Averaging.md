**Disclaimer:**

_I am a **programmer** and I am **NOT** an accredited financial expert. You
should seek out an accredited financial expert for making serious investment
decisions. Do NOT take investment advice from random internet strangers and
always do your own research._

# Dynamic Cost Averaging

Dynamic Cost Averaging is similar to Cost Averaging. We set a Principle Amount
and then purchase an asset with Principle Amount on a set interval based on Time
Period.

We include Target Value that assists in determining the amount to buy or sell
based on a Purchase Factor of the Principle Amount that falls within Min Factor
and Max Factor range. These expressions and variables are defined by the user.

We need to define our columns: Date, Market Price, Current Target, Current
Value, Principle Amount, Factor Purchase, Factor Amount, Total Factor Amount,
Order Size, Total Order Size, and Time Period. This will allow us to keep track
of the relevant data and show the evaluated expressions as its set of results.

We define the sequence of steps, as well as the expressions used, to evaluate
each value as the following:

1.  Define Principle Amount

        Principle Amount = Constant Float Value

2.  Define Factor Range

        Min Factor = Constant Integer Value of 1 or greater sets lower limit
        Max Factor = Constant Integer Value greater than Min Factor sets upper limit

3.  Get Date

        Date = Current Date

4.  Get Market Price

        Market Price = Current Market Price

5.  Get Time Period

        IF NOT Time Period
                THEN Time Period = 0
        WHERE increment(Time Period) for each inserted record
                Time Period = 1 + Time Period

6.  Get Current Target

        Current Target = Principle Amount * Time Period

7.  Get Previous Total Order Size

        IF NOT Previous Total Order Size
                THEN Previous Total Order Size = 0
        WHERE Previous Total Order Size = Total Order Size for each inserted record
                Previous Total Order Size = 0 or total sum (Σ) of Order Size column excluding current record

8.  Get Order Size

        Order Size = Principle Amount / Market Price

9.  Get Total Order Size

        Total Order Size = Order Size + Previous Total Order Size

10. Get Current Value

    Current Value = Market Price \* Previous Total Order Size

11. Get Factor Purchase

    How much should be bought or sold to get back to the Target Value.

        Target Difference = Current Target - Current Value

    Factor Purchase represents a value that is used to determine the size of the
    next trade.

        Factor Purchase = Target Difference / Principle Amount

    We also need to enforce the Min Factor and Max Factor limits.

        IF Factor Purchase = 0
            THEN RETURN 1
        IF Factor Purchase = 0
            THEN RETURN 1
        # Enforce Min Factor and Max Factor
        IF NOT -(Max Factor) <= Factor Purchase <= Max Factor
            IF Factor Purchase > Max Factor
                THEN RETURN Max Factor
            IF Factor Purchase < -(Max Factor)
                THEN RETURN -(Max Factor)
        RETURN min(max(Factor Purchase, Min Factor), Max Factor)

12. Get Factor Amount

        Factor Amount = Purchase Factor * Principle Amount

13. Get Previous Total Factor Amount

        IF NOT Previous Total Factor Amount
                THEN Previous Total Factor Amount = 0
        WHERE Previous Total Factor Amount = 0 or total sum (Σ) of Factor Amount column excluding current record

14. Get Total Factor Amount

        Total Factor Amount = Factor Amount + Previous Total Factor Amount

15. Update Previous Total Factor Amount and Previous Total Order Size

        Previous Total Factor Amount = Total Factor Amount
        Previous Total Order Size = Total Order Size

Let's set Time Period, Previous Total Order Size, and Previous Total Factor
Amount to 0.

    Time Period = 0
    Previous Total Factor Amount = 0
    Previous Total Order Size = 0

Example of how to calculate Target Difference, Factor Purchase, and Factor
Amount to buy:

    Target Difference = 200 - 91.11 = 108.89 (positive value is a buy signal)
    Factor Purchase = 108.89 / 100 ≈ 1.09 ≈ 1 (rounded to the nearest integer)
    Amount = 1 * 100 = 100 (buy $100)

Example of how to calculate Difference, Purchase Factor, and Amount to sell:

    Target Difference = 200 - 302.43 = -102.43 (inverse value is a sell signal)
    Purchase Factor = -102.43 / 100 ≈ -1.0243 ≈ -1 (rounded to the nearest integer)
    Amount = -1 * 100 = -100 (sell $100)

Now we can tabulate our Current Target, Current Value, Factor Purchase, Factor
Amount, Total Factor Amount, Amount*, \_Size*, _Total Size_, and _Period_. This
allows us to track the progress of our investment and gives us a "_birds eye_"
view of its performance over time.

I want to paper trade $100 per month on a yearly basis. I will paper trade $100
per month using the BTC-USD trade pair over a 1 year period. The 1 year period
will take place in 2020 on the first day of each month.

| Date       | Market Price | Current Target | Current Value | Principle Amount | Factor Purchase | Factor Amount | Total Factor Amount | Order Size | Total Order Size | Time Period |
| ---------- | ------------ | -------------- | ------------- | ---------------- | --------------- | ------------- | ------------------- | ---------- | ---------------- | ----------- |
| 2020-01-01 | 7174.33      | 100.00         | 0.00          | 100.00           | 1.00            | 100.00        | 100.00              | 0.01393858 | 0.01393858       | 1           |
| 2020-02-01 | 9380.18      | 200.00         | 130.75        |                  |                 |               |                     |            |                  | 2           |
| 2020-03-01 | 8522.31      | 300.00         | 209.64        |                  |                 |               |                     |            |                  | 3           |
| 2020-04-01 | 6666.11      | 400.00         | 242.20        |                  |                 |               |                     |            |                  | 4           |

---

| Date       | Market Price | Current Target | Current Value | Principle Amount | Factor Purchase | Factor Amount | Total Factor Amount | Order Size | Total Order Size | Time Period |
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
