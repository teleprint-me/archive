# Importing the Matplotlib library for plotting
import matplotlib.pyplot as plt


# Redefining the functions and constants, and running the code block for graphing
def calculate_periodic_interest_rate(interest_rate, frequency):
    return 1 + (interest_rate / frequency)


def calculate_principal_amount(
    target_amount, interval, periodic_interest_rate
):
    return target_amount / (interval * pow(periodic_interest_rate, interval))


# Constants for the simulation
daily_interest_rate = 5 / 100  # 5% daily interest rate
frequency = 365  # daily compounding
interval_range = 30  # 30 days
target_amount_goal = 3_000_000  # Target Amount of 3,000,000 Sats

# Lists to store the results for graphing
principal_days = []
principal_satoshis = []

# Calculate the periodic interest rate
periodic_rate = calculate_periodic_interest_rate(
    daily_interest_rate, frequency
)

# Calculate the principal amount needed to reach the target amount for each interval in the range
for interval in range(1, interval_range + 1):
    principal_amount = calculate_principal_amount(
        target_amount_goal, interval, periodic_rate
    )

    principal_days.append(interval)
    principal_satoshis.append(principal_amount)

# Displaying the results in a graph
plt.plot(principal_days, principal_satoshis, marker="o", color="blue")
plt.title("Principal Amount Needed to Reach 3,000,000 Sats (Daily Trading)")
plt.xlabel("Days")
plt.ylabel("Principal Amount (Sats)")
plt.grid(True)
plt.show()
