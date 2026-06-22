#-----------------------------------------------------------------------------------------------------------
#Simon Ackermann
#-----------------------------------------------------------------------------------------------------------
import pandas as pd

URL = "https://data.bitcoinity.org/export_data.csv?c=e&currency=USD&data_type=price&t=l&timespan=all"

df = pd.read_csv(URL)

# First column is time, remaining columns are exchanges
df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], utc=True)
df["price"] = df.iloc[:, 1:].mean(axis=1, skipna=True)

# Convert to daily average
daily = (
    df.set_index(df.columns[0])["price"]
    .resample("1D")
    .mean()
    .dropna()
)

with open("bitcoinity_data.txt", "w") as f:
    for date, price in daily.items():
        f.write(f"{date.strftime('%d.%m.%Y')}\t{price:.8f}\n")
