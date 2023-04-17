**Disclaimer:**

_I am a **programmer** and I am **NOT** an accredited financial expert. You
should seek out an accredited financial expert for making serious investment
decisions. Do NOT take investment advice from random internet strangers and
always do your own research._

# Value Averaging

Value Averaging is similar to Cost Averaging. We set a Principle Amount and then
purchase an asset with the Principle Amount on a set interval based on Time
Period and Growth Rate.

We need to define our columns: Date, Market Price, Current Target, Current
Value, Trade Amount, Total Trade Amount, Order Size, Total Order Size, and Time
Period. This will allow us to keep track of the relevant data and show the
evaluated expressions as its set of results.

## Algorithm

We define the sequence of steps, as well as the expressions used, to evaluate
each value as the following:

1.  Define Principle Amount

        Principle Amount = Constant Float Value

2.  Define Interest Rate

        Interest Rate = Constant Float Value

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

        IF NOT Previous Current Target
            THEN Current Target = Principle Amount
        IF Previous Current Target
            THEN Current Target = Principle Amount * Time Period * pow(Interest Rate, Time Period)

7.  Get Previous Total Order Size

        IF NOT Previous Total Order Size
                THEN Previous Total Order Size = 0
        WHERE Previous Total Order Size = Total Order Size for each inserted record
                Previous Total Order Size = 0 or sum(Order Size) column excluding current record

8.  Get Order Size

        Order Size = Trade Amount / Market Price

9.  Get Total Order Size

        Total Order Size = Order Size + Previous Total Order Size

10. Get Current Value

        Current Value = Market Price * Previous Total Order Size

11. Get Previous Total Trade Amount

        IF NOT Previous Total Trade Amount
                THEN Previous Total Trade Amount = 0
        WHERE Previous Total Trade Amount = Total Trade Amount for each inserted record
                Previous Total Trade Amount = 0 or sum(Trade Amount) column excluding current record

12. Get Trade Amount

        Trade Amount = Current Target - Current Value

        IF Trade Amount > 0
            THEN buy Trade Amount
        IF Trade Amount < 0
            THEN sell Trade Amount

13. Get Total Trade Amount

        Total Trade Amount = Trade Amount + Previous Total Trade Amount

14. Update Previous Total Order Size and Previous Total Trade Amount

        Previous Total Order Size = Total Order Size
        Previous Total Trade Amount = Total Trade Amount

15. Repeat steps 3 through 14 until all records have been evaluated

## Walkthrough

I want to paper trade $100 per month on a yearly basis. I will paper trade $100
per month using the BTC-USD trade pair over a 1 year period. The 1 year period
will take place in 2020 on the first day of each month.

    Dollars smallest units are denominated in "pennies" and will use a precision
    of

        1 * 10 ^ -2 = 0.01

    Bitcoins smallest units are denominated in "satoshis" and will use a
    precision of

        1 * 10 ^ -8 = 0.00000001

Initialize the table and calculate the first record:

1.  Set Time Period, Previous Total Order Size, and Previous Total Trade Amount
    to 0

        Time Period = 0
        Previous Total Order Size = 0
        Previous Total Trade Amount = 0

2.  Set Principle Amount

        Principle Amount = 100.00

3.  Set the Interest Rate. We set the Interest Rate to 10% and add 1 to it to
    enforce the identity property of multiplication. This ensures that the
    Current Target is properly calculated and returns the expected values.

        Interest Rate = 1 + 0.10 = 1.10

4.  Get Date

        Date = "2020-01-01"

5.  Get Market Price

        Market Price = 7174.33

6.  Get Time Period

        Time Period = 1 + 0 = 1

7.  Get Current Target. The Current Target for the first record is always the
    Principle Amount. The rationale is to exclude the interest rate from the
    initial amount because there are no previous investments. The rest of the
    records evaluate the expression
    `Principle Amount * Time Period * POW(Interest Rate, Time Period)` to
    calculate the Current Target in order to include the interest rate from the
    2nd record forward on.

        Current Target = 100.00

8.  Get Order Size

        Order Size = 100.00 / 7174.33 ≅ 0.013938583812007533 ≅ 0.01393858

9.  Get Total Order Size

        Total Order Size = 0.01393858 + 0 = 0.01393858

10. Get Current Value

        Current Value = 7174.33 * 0 = 0

11. Get Trade Amount

        Trade Amount = 100.00 - 0 = 100.00

12. Get Total Trade Amount

        Total Trade Amount = 100.00 + 0

13. Update Previous Total Order Size and Previous Total Trade Amount

        Previous Total Order Size = 0.01393858
        Previous Total Trade Amount = 100.00

Now we can tabulate our Current Target, Current Value, Trade Amount, Total Trade
Amount, Order Size, and Total Order Size.

This allows us to track our investment over time and signals whether we should
buy, sell, or hold.

Holding is usually enforced via a minimum or maximum trade amount and varies
amongst brokerages and is outside of the scope of this strategy.

| Date       | Market Price | Current Target | Current Value | Trade Amount | Total Trade Amount | Order Size | Total Order Size | Time Period |
| ---------- | ------------ | -------------- | ------------- | ------------ | ------------------ | ---------- | ---------------- | ----------- |
| 2020-01-01 | 7174.33      | 100.00         | 0.00          | 100.00       | 100.00             | 0.01393858 | 0.01393858       | 1           |
| 2020-02-01 | 9380.18      | 200.00         |               |              |                    |            |                  | 2           |

---

1.  Get Date

        Date = "2020-02-01"

2.  Get Market Price

        Market Price = 9380.18

3.  Get Time Period

        Time Period = 1 + 1 = 2

4.  Get Current Target

        Current Target = 100.00 * 2 * pow(1.10, 2) ≅ 242.00000000000003 ≅ 242.00

5.  Get Current Value

        Current Value = 9380.18 * 0.01393858 ≅ 130.7463893444 ≅ 130.75

6.  Get Trade Amount

        Trade Amount = 242.00 - 130.75 = 111.25

7.  Get Total Trade Amount

        Total Trade Amount = 111.25 + 100.00 = 211.25

8.  Get Order Size

        Order Size = 111.25 / 9380.18 ≅ 0.011860113558588428 ≅ 0.01186011

9.  Get Total Order Size

        Total Order Size = 0.01186011 + 0.01393858 = 0.02579869

10. Update Previous Total Order Size and Previous Total Trade Amount

        Previous Total Order Size = 0.02579869
        Previous Total Trade Amount = 211.25

11. Repeat steps 1 through 10 until each record has been evaluated

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
