import pandas as pd


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

