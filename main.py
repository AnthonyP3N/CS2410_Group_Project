'''
Notes
df = main Zillow dataset (dataframe)
dallas_city = dallas only columns (dataframe)

'''

import pandas as pd
import matplotlib.pyplot as plt
from stats import *
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv("ZillowCityData.csv")

dallas = df[(df["RegionName"] == "Dallas") & (df["State"] == "TX")]

print(dallas)

# Keep only the date/value columns
date_columns = df.columns[8:]   # first 8 columns are metadata in csv file, not needed ex: (RegionName, State, Metro, and so on)

dallas_city = dallas[date_columns].T  # Flips rows and columns to be structure dates before value ex: 1/32/2000 96000
dallas_city.columns = ["HomeValue"]   # Name date_columns to home values to reflect the average value of homes for each month 

# Convert index to datetime objects, so from strings to actual datetimes, useful for later when plotting gets introduced
dallas_city.index = pd.to_datetime(dallas_city.index)

# Make values numeric
dallas_city["HomeValue"] = pd.to_numeric(dallas_city["HomeValue"])

# Remove missing values just in case
dallas_city = dallas_city.dropna()

print(dallas_city)

# Simple code to print out graph using matplot
plt.figure(figsize=(12,6))                              # Declares figure size
plt.plot(dallas_city.index, dallas_city['HomeValue'])   # Sets x axis to year, y axis to HomeValue corresponding to year
plt.title("Dallas Home Values Over Time")               # Title of graph
plt.xlabel("Year")                                      # Title of X-axis
plt.ylabel("Home Value ($)")                                # Title of Y-axis
plt.grid(True)                                          # Puts graph on grid structure
plt.show()                                              # Show graph

print("--- Statistics ---")
print(f"Mean: ${round(find_mean(dallas_city), 2)}")
print(f"Median: ${round(find_median(dallas_city), 2)}")
print(f"Minimum: ${round(find_min(dallas_city), 2)}")
print(f"Maximum: ${round(find_max(dallas_city), 2)}")
print(f"Range: ${round(find_range(dallas_city), 2)}")
print(f"Variance: {find_variance(dallas_city)}")
print(f"Standard Deviation: {round(find_stdev(dallas_city), 2)}")
print(f"Skewness: {find_skewness(dallas_city)}")
print(f"Kurtosis: {find_kurtosis(dallas_city)}")

# example of slicing to view only a range, user input way is below
# print(find_date_range(dallas_city, "2006", "2008"))

## Below is function to specify range of years to analyze
# startYear, endYear = get_year_input()
# dateRange = find_date_range(dallas_city, startYear, endYear)
# print_range_of_information(dateRange, startYear, endYear)

# Define upper and lower bounds for the standard inflation range
UPPER_STANDARD_INFLATION = 5.0
LOWER_STANDARD_INFLATION = 3.0

# Calculate year-over-year % change in home values using a 12-month rolling period
dallas_city["YtoY_rate"] = dallas_city["HomeValue"].pct_change(periods=12) * 100


#---------------------Inflation Graphs---------------------------- 

# Create figure and axes with a wide layout for readability
fig, ax = plt.subplots(figsize=(14, 6))

# Plot the year-to-year inflation rate as an orange line
ax.plot(dallas_city.index, dallas_city["YtoY_rate"], color="orange", linewidth=2, label="Year to Year % Change")

# Draw dashed horizontal lines marking the upper and lower standard inflation bounds
ax.axhline(y=UPPER_STANDARD_INFLATION, color="darkred", linewidth=1.4, linestyle="--", label=f"Standard Inflation Rate ({UPPER_STANDARD_INFLATION}%)")
ax.axhline(y=LOWER_STANDARD_INFLATION, color="darkred", linewidth=1.4, linestyle="--", label=f"Standard Inflation Rate ({LOWER_STANDARD_INFLATION}%)")

# Draw a solid baseline at y=0 to visually separate growth from deflation
ax.axhline(y=0, color="black", linewidth=0.8, linestyle="-")

# Highlight in red where inflation exceeds the upper standard (high inflation rates)
ax.fill_between(dallas_city.index,
                dallas_city["YtoY_rate"],
                UPPER_STANDARD_INFLATION,
                where=(dallas_city["YtoY_rate"] > UPPER_STANDARD_INFLATION),
                color="red", alpha=0.2, label="Above Standard")

# Highlight in orange where inflation is positive but below the lower standard (below standard inflation rate)
ax.fill_between(dallas_city.index,
                dallas_city["YtoY_rate"],
                LOWER_STANDARD_INFLATION,
                where=(dallas_city["YtoY_rate"] < LOWER_STANDARD_INFLATION) & (dallas_city["YtoY_rate"] > 0),
                color="orange", alpha=0.2, label="Below Standard, Above Zero")

# Highlight in green where inflation falls within the standard inflation range (3%–5%)
ax.fill_between(dallas_city.index,
                dallas_city["YtoY_rate"],
                UPPER_STANDARD_INFLATION,
                where=(dallas_city["YtoY_rate"] >= 3.0) & (dallas_city["YtoY_rate"] <= UPPER_STANDARD_INFLATION),
                color="green", alpha=0.2, label="Standard Inflation Rate")

# Highlight in blue where inflation is negative, indicating home value deflation
ax.fill_between(dallas_city.index,
                dallas_city["YtoY_rate"], 0,
                where=(dallas_city["YtoY_rate"] < 0),
                color="blue", alpha=0.2, label="Deflation (Below 0%)")

# Set graph title and axis labels
ax.set_title("Dallas Home Value Inflation Rate (Year-to-Year % Change)")
ax.set_xlabel("Year")
ax.set_ylabel("Inflation Rate (%)")

# Place the legend in the upper left to avoid overlapping the data
ax.legend(loc="upper left")

# Add a subtle grid for easier value estimation
ax.grid(True, alpha=0.1)


# Adjust layout to prevent clipping and show the plot graph
plt.tight_layout()
plt.show()

outlier_list = find_outliers(dallas_city)

print("\nOutliers:")
for date, price, Zscore in outlier_list:
    print(f"{date.date()} | ${price} | {Zscore:.2f}")

trend(dallas_city)

seasonal_analyze = seasonality(dallas_city)

seasonal_analyze.plot(kind="bar")

plt.title("Average Z-Score by month")
plt.xlabel("Month")
plt.ylabel("Average Z-Score")
plt.axhline(0)  # baseline

plt.show()

cagr = cagr_comp(dallas_city['HomeValue'])
print(f"Average yearly home price inflation: {cagr:.2%}")
print(f"Average inflation from 2005-2025: 2.5%")
print(f"Factor of home / general inflation: {cagr * 100 / 2.5 :.2f}")



# ---------- Bar Chart ----------

# Categorize each monthly reading into one of four inflation zones
deflation_rates      = (dallas_city["YtoY_rate"] < 0)
below_standard_rates = (dallas_city["YtoY_rate"] > 0) & (dallas_city["YtoY_rate"] < LOWER_STANDARD_INFLATION)
standard_rates       = (dallas_city["YtoY_rate"] >= LOWER_STANDARD_INFLATION) & (dallas_city["YtoY_rate"] <= UPPER_STANDARD_INFLATION)
above_standard_rates = (dallas_city["YtoY_rate"] > UPPER_STANDARD_INFLATION)

# Build a dictionary with category labels as keys and month counts as values
inflation_categories = {
    "Deflation\n(< 0%)":       deflation_rates.sum(),
    "Below Standard\n(0-3%)":  below_standard_rates.sum(),
    "Standard\n(3-5%)":        standard_rates.sum(),
    "Above Standard\n(> 5%)":  above_standard_rates.sum(),
}

# Create bar chart from dictionary
plt.figure(figsize=(10, 6))
plt.bar(inflation_categories.keys(), inflation_categories.values(), color=["blue", "orange", "green", "red"], alpha=0.7, edgecolor="black")

# Label each bar with its count
for i, (label, count) in enumerate(inflation_categories.items()):
    plt.text(i, count + 0.3, str(count), ha="center", va="bottom", fontweight="bold")

plt.title("Dallas Home Value Inflation — Months per Category")
plt.xlabel("Inflation Category")
plt.ylabel("Number of Months")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()

# ---------- Overlapping Graph ----------

fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot home values on the left y-axis in blue
ax1.plot(dallas_city.index, dallas_city["HomeValue"], color="blue", linewidth=2, label="Home Value ($)")
ax1.set_xlabel("Year")
ax1.set_ylabel("Home Value ($)", color="black")
ax1.tick_params(axis="y", labelcolor="black")

# Create a second y-axis sharing the same x-axis for the inflation rate
ax2 = ax1.twinx()
ax2.plot(dallas_city.index, dallas_city["YtoY_rate"], color="purple", linewidth=1.0, linestyle="--", label="Inflation Rate")
ax2.axhline(y=0, color="black", linewidth=1.0, linestyle="--")
ax2.set_ylabel("Inflation Rate (%)", fontweight = "bold", color="purple")
ax2.tick_params(axis="y", labelcolor="purple")


# Fill green where inflation is above zero, more generalize for simplicity
ax2.fill_between(dallas_city.index,
                 dallas_city["YtoY_rate"],
                 0,
                 where=(dallas_city["YtoY_rate"] >= 0),
                 color="green", alpha=0.4)


# Highlight in red where inflation is negative (deflation)
ax2.fill_between(dallas_city.index,
                dallas_city["YtoY_rate"],
                0,
                where=(dallas_city["YtoY_rate"] < 0),
                color="red", alpha=0.2)

# Combine both legends into one
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

ax1.set_title("Dallas Home Values vs Inflation Rate (Year-to-Year % Change)")
ax1.grid(True, alpha=0.1)

plt.tight_layout()
plt.show()
