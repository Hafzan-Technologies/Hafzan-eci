import yfinance as yf
import pandas as pd
import json

# Define weights
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

# Download price data
tickers = list(set(k for w in quarterly_weights.values() for k in w))
data = yf.download(tickers, start=start_date, end=end_date)["Close"].dropna()

# Normalize and build composite
normalized = data / data.iloc[0]
composite = pd.Series(index=normalized.index, dtype=float)

for i, (q_start, weights) in enumerate(sorted((pd.to_datetime(k), v) for k, v in quarterly_weights.items())):
    q_end = sorted((pd.to_datetime(k) for k in quarterly_weights.keys()))[i+1] if i+1 < len(quarterly_weights) else normalized.index[-1]
    mask = (normalized.index >= q_start) & (normalized.index <= q_end)
    sub_data = normalized.loc[mask, weights.keys()]
    composite.loc[mask] = (sub_data * pd.Series(weights)).sum(axis=1)

composite = composite / composite.iloc[0] * 1000

# Save as JSON
chart_data = {
    "dates": [d.strftime("%Y-%m-%d") for d in composite.index],
    "values": composite.round(2).tolist()
}
with open("data.json", "w") as f:
    json.dump(chart_data, f)