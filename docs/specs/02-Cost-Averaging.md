**Disclaimer:**

_I am a **programmer** and I am **NOT** an accredited financial expert. You should seek out an accredited financial expert for making serious investment decisions. Do NOT take investment advice from random internet strangers and always do your own research._

# Cost Averaging

_Cost Averaging_ is just setting a _Principle Amount_ and then purchasing an asset with that _Fixed Amount_ on a _Set Interval_ based on a _Time Period_ that is defined by the investor.

I want to _Paper Trade_ $100 per month on a yearly basis. I will paper trade $100 per month using the BTC-USD trade pair over a 1 year period. The 1 year period will take place in 2020.

We define our columns as: Date, Price, Target, Value, Size, Total Size, and Period.

This keeps the tabulation of our data simple and compact.

We also need to define how each record is calculated by filling out each cell with the appropriate data.

-   If there is no previous **Period**, then set **Period** to **0** where
-   -   **Period** = 1 + Period
-   **Target** = Principle Amount \* Period
-   **Size** = Principle Amount / Price
-   If there is no **Previous Total Size**, then set **Pervious Total Size** to
    **0** where
-   -   **Previous Total Size** = **0** or the _Total Sum_ (Σ) of the **Size**
        column excluding the _Current Record_
-   **Total Size** = Size + Previous Total Size
-   **Value** = Price \* Previous Total Size

Let's start by setting both _Previous Total Size_ and _Period_ to 0.

-   **Previous Total Size** = 0
-   **Period** = 1 + 0 = 1

Now we can tabulate our _Target_, _Value_, _Size_, _Total Size_, and _Period_. This allows us to track the progress of our investment and gives us a "_birds eye_" view of its performance over time.

It's important to keep in mind that the current _Value_ excludes the current records _Total Size_.

-   If **Value** as (Price \* Current Total Size) **includes** current record,
    then **Value** = Price \* Current Total Size
-   Else **Value** = Price \* Previous Total Size **excludes** current record

| Date     | Price     | Target | Value   | Size       | Total Size | Period |
| -------- | --------- | ------ | ------- | ---------- | ---------- | ------ |
| 01/01/20 | $9334.98  | $100   | 0       | 0.01071240 | 0.01071240 | 01     |
| 02/01/20 | $8505.07  | $200   | $91.11  | 0.01175769 | 0.02247009 | 02     |
| 03/01/20 | $6424.35  | $300   | $144.36 | 0.01556578 | 0.03803587 | 03     |
| 04/01/20 | $8624.28  | $400   | $328.03 | 0.01159517 | 0.04963104 | 04     |
| 05/01/20 | $9446.57  | $500   | $468.84 | 0.01058585 | 0.06021689 | 05     |
| 06/01/20 | $9136.20  | $600   | $550.15 | 0.01094547 | 0.07116236 | 06     |
| 07/01/20 | $11351.62 | $700   | $807.81 |            |            | 07     |
| 08/01/20 | $11655.00 | $800   |         |            |            | 08     |
| 09/01/20 | $10779.63 | $900   |         |            |            | 09     |
| 10/01/20 | $13804.81 | $1000  |         |            |            | 10     |
| 11/01/20 | $19713.94 | $1100  |         |            |            | 11     |
| 12/01/20 | $28990.08 | $1200  |         |            |            | 12     |

See if you can finish the table as an exercise. It's already more than halfway there for you.

We opted for _excluding_ the current _Value_ and you can see that we remained in an _unrealized loss_ up until the 4th record entry.

-   **Gain/Loss** = Value - Previous Target
-   **Gain/Loss** = 328.03 - 300 ≈ 28.03

We can also see that we made an _unrealized gain_ of $28.03 by the 4th record entry. Our investment is only _realized_ once we sell.

We can define*Gain/Loss* as:

-   **Gain/Loss** = Value - Previous Target

-   If there is no **Value**, then set **Value** to **0**.
-   If there is no **Previous Target**, then set **Previous Target** to **0**.

-   A **Gain** is represented as a _positive value_ (+) while a **Loss** is
    represented as a _negative value_ (-).

-   First Row: **Gain/Loss** = 0 - 0 = 0
-   Second Row: **Gain/Loss** = 91.11 - 100 ≈ -8.89
-   Third Row: **Gain/Loss** = 144.36 - 200 ≈ -55.64
-   Forth Row: **Gain/Loss** = 328.03 - 300 ≈ 28.03
-   Fifth row: **Gain/Loss** = 468.84 - 400 ≈ 68.84

You'll notice that the _Previous Target_ is always the previous **Target** value and **Value** is always represents the current records **Value**.

| Date     | Price     | Target | Value   | Gain/Loss | Size       | Total Size | Period |
| -------- | --------- | ------ | ------- | --------- | ---------- | ---------- | ------ |
| 01/01/20 | $9334.98  | $100   | 0       | 0         | 0.01071240 | 0.01071240 | 01     |
| 02/01/20 | $8505.07  | $200   | $91.11  | -$8.89    | 0.01175769 | 0.02247009 | 02     |
| 03/01/20 | $6424.35  | $300   | $144.36 | -$55.64   | 0.01556578 | 0.03803587 | 03     |
| 04/01/20 | $8624.28  | $400   | $328.03 | $28.03    | 0.01159517 | 0.04963104 | 04     |
| 05/01/20 | $9446.57  | $500   | $468.84 | $68.84    | 0.01058585 | 0.06021689 | 05     |
| 06/01/20 | $9136.20  | $600   | $550.15 | $50.15    | 0.01094547 | 0.07116236 | 06     |
| 07/01/20 | $11351.62 | $700   | $807.81 | $207.81   | 0.00880932 | 0.07997168 | 07     |
| 08/01/20 | $11655.00 | $800   |         |           |            |            | 08     |
| 09/01/20 | $10779.63 | $900   |         |           |            |            | 09     |
| 10/01/20 | $13804.81 | $1000  |         |           |            |            | 10     |
| 11/01/20 | $19713.94 | $1100  |         |           |            |            | 11     |
| 12/01/20 | $28990.08 | $1200  |         |           |            |            | 12     |

See if you can finish the table as an exercise. Again, it's already more than halfway there for you.

You can also see that **Size** was affected by the **Price**. We bought less when the price was "**high**" and bought more when the price was "**low**". This becomes more apparent as the price increases or decreases.
