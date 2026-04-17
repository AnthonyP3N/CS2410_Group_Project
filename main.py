'''
Notes
df = main Zillow dataset (dataframe)
dallas_city = dallas only columns (dataframe)

'''

import pandas as pd
import matplotlib.pyplot as plt
from stats import *

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
plt.ylabel("Home Value")                                # Title of Y-axis
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

startYear, endYear = get_year_input()
dateRange = find_date_range(dallas_city, startYear, endYear)
print_range_of_information(dateRange, startYear, endYear)


