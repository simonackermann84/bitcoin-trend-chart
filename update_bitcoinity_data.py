#-----------------------------------------------------------------------------------------------------------
#Simon Ackermann
#-----------------------------------------------------------------------------------------------------------
import pandas as pd

URL = "https://data.bitcoinity.org/export_data.csv?c=e&currency=USD&data_type=price&t=l&timespan=all"

df = pd.read_csv(URL)

time_col = df.columns[0]

# Do not assign this back into df[time_col]; keep it as a separate datetime series
time = pd.to_datetime(df[time_col], utc=True)

# Convert all exchange columns to numeric
price_columns = df.columns[1:]
prices = df[price_columns].apply(pd.to_numeric, errors="coerce")

# Average across exchanges
df_numeric = pd.DataFrame({
    "time": time,
    "price": prices.mean(axis=1, skipna=True)
})

# Convert to daily average
daily = (
    df_numeric
    .set_index("time")["price"]
    .resample("1D")
    .mean()
    .dropna()
)

with open("bitcoinity_data.txt", "w", encoding="utf-8") as f:
    for date, price in daily.items():
        f.write(f"{date.strftime('%d.%m.%Y')}\t{price:.8f}\n")

print("Updated bitcoinity_data.txt")
print("First rows:")
print(daily.head())
print("Last rows:")
print(daily.tail())
