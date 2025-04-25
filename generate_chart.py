import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Your tickers and weights
quarterly_weights = {
    "2025-04-01": {
        "PERSISTENT.NS": 0.0235,
        "TATAELXSI.NS": 0.0235,
        "HEROMOTOCO.NS": 0.0235,
        "MARUTI.NS": 0.0235,
        "DRREDDY.NS": 0.0278,
        "APOLLOHOSP.NS": 0.0278,
        "DIVISLAB.NS": 0.0321,
        "CIPLA.NS": 0.0321,
        "BRITANNIA.NS": 0.0364,
        "TATACONSUM.NS": 0.0407,
        "BAJAJ-AUTO.NS": 0.0450,
        "TECHM.NS": 0.0450,
        "ULTRACEMCO.NS": 0.0493,
        "HCLTECH.NS": 0.0535,
        "NESTLEIND.NS": 0.0535,
        "WIPRO.NS": 0.0578,
        "SUNPHARMA.NS": 0.0707,
        "ASIANPAINT.NS": 0.0750,
        "INFY.NS": 0.0836,
        "HINDUNILVR.NS": 0.0879,
        "TCS.NS": 0.0879
    }
}

start_date = "2025-04-01"
end_date = pd.Timestamp.today().strftime("%Y-%m-%d")

# Get full ticker list
all_tickers = set()
for weights in quarterly_weights.values():
    all_tickers.update(weights.keys())

# Download data
data = yf.download(list(all_tickers), start=start_date, end=end_date)["Close"]
data = data.dropna()

# Normalize from the start and use base value of 1000
normalized = data / data.iloc[0]
composite = pd.Series(index=normalized.index, dtype=float)

# Process quarterly weights
sorted_quarters = sorted((pd.to_datetime(k), v) for k, v in quarterly_weights.items())

# Apply weights for each time period
for i, (start, weights) in enumerate(sorted_quarters):
    end = sorted_quarters[i + 1][0] if i + 1 < len(sorted_quarters) else normalized.index[-1]
    mask = (normalized.index >= start) & (normalized.index <= end)
    temp_data = normalized.loc[mask, weights.keys()]
    composite.loc[mask] = (temp_data * pd.Series(weights)).sum(axis=1)

# Scale the index to base value 1000
composite = composite / composite.iloc[0] * 1000

# Plot using Matplotlib (Line Chart)
plt.figure(figsize=(12, 6))
plt.plot(composite.index, composite, label="Hafzan Composite Index", color="blue", linewidth=1.5)
plt.title("Hafzan Composite Index", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Index Value")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save the plot as an HTML file
plt.savefig("index.html")
