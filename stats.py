import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

def find_min(df):
    return df["HomeValue"].min()

def find_min_range(subset):
    return subset.min()

def find_max(df):
    return df["HomeValue"].max()

def find_max_range(subset):
    return subset.max()

def find_mean(df):
    return df["HomeValue"].mean()

def find_mean_range(subset):
    return subset.mean()

def find_median(df):
    return df["HomeValue"].median()

def find_median_range(subset):
    return subset.median()

def find_stdev(df):
    return df["HomeValue"].std()

def find_variance(df):
    return df["HomeValue"].var()

def find_skewness(df):
    return df["HomeValue"].skew()

def find_kurtosis(df):
    return df["HomeValue"].kurtosis()

def find_percentile(df, percentile):
    return df["HomeValue"].quantile(q=percentile)

def find_range(df):
    return df["HomeValue"].max() - df["HomeValue"].min()

def find_date_range(df, start_date, end_date):
    return df["HomeValue"].loc[start_date:end_date]

def get_year_input():
    start_year = int(input("Please enter the first year of prices you would like to view: "))
    while start_year < 2000 or start_year > 2025:
        start_year = int(input("We do not have access to those years, please select another year: "))
    end_year = int(input("Please enter the last year of prices you would like to view: "))
    while end_year < 2000 or end_year > 2025 or end_year < start_year:
        if end_year < start_year:
            end_year = int(input("Your final year is less than the starting year, please select another: "))
        else:
            end_year = int(input("We do not have access to those years, please select another year: "))

    start_year = str(start_year)
    end_year = str(end_year)
    return start_year, end_year

def print_range_of_information(subset, start_year, end_year):
    print(f"Mean from year {start_year} to {end_year}: ${round(find_mean_range(subset), 2)}")
    print(f"Median from year {start_year} to {end_year}: ${round(find_median_range(subset), 2)}")
    print(f"The lowest average home price in your range was ${round(find_min_range(subset), 2)}")
    print(f"The highest average home price in your range was ${round(find_max_range(subset), 2)}")

def find_outliers(df):
    if isinstance(df, pd.Series):
        s = df.dropna()
    else:
        s = df['HomeValue'].dropna()

    X = np.arange(len(s)).reshape(-1, 1)
    y = s.values

    model = LinearRegression()
    model.fit(X, y)

    trend = model.predict(X)
    res = y - trend

    res_z_score = (res - res.mean()) / res.std(ddof=1)

    out = pd.DataFrame({
        "price": s,
        "residual_z": res_z_score
    }, index=s.index)

    outliers = out[out["residual_z"].abs() > 1.62]

    result = list(zip(outliers.index, outliers["price"]))
    return result

def trend(df):
    if isinstance(df, pd.Series):
        s = df.dropna()
    else:
        s = df["HomeValue"].dropna()

    s = s.sort_index()

    X = np.arange(len(s)).reshape(-1, 1)
    y = s.values

    model = LinearRegression()
    model.fit(X, y)

    trend = model.predict(X)

    plt.figure(figsize=(10, 5))

    # Actual prices
    plt.plot(s.index, y, label="Actual Prices")

    # Trend line
    plt.plot(s.index, trend, linestyle="--", label="Trend Line")

    plt.title("Home Prices with Trend Line")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()

    plt.show()


