import yfinance as yf
import pandas as pd
import json
import plotly.express as px  # For visualizing the data in Python (optional)

# Quarterly weights for the Hafzan Composite Index
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

# Get tickers and download price data
tickers = set()
for weights in quarterly_weights.values():
    tickers.update(weights.keys())
data = yf.download(list(tickers), start=start_date, end=end_date)["Close"].dropna()

# Normalize and calculate composite index
normalized = data / data.iloc[0]
composite = pd.Series(index=normalized.index, dtype=float)

sorted_quarters = sorted((pd.to_datetime(k), v) for k, v in quarterly_weights.items())

for i, (start, weights) in enumerate(sorted_quarters):
    end = sorted_quarters[i + 1][0] if i + 1 < len(sorted_quarters) else normalized.index[-1]
    mask = (normalized.index >= start) & (normalized.index <= end)
    temp_data = normalized.loc[mask, weights.keys()]
    composite.loc[mask] = (temp_data * pd.Series(weights)).sum(axis=1)

composite = composite / composite.iloc[0] * 1000

# Save to data.json
output = {
    "dates": composite.index.strftime("%Y-%m-%d").tolist(),
    "values": composite.round(2).tolist()
}
with open("data.json", "w") as f:
    json.dump(output, f)

# Optional: Save a Plotly graph to file (if you want to visualize it in Python as well)
fig = px.line(
    x=composite.index,
    y=composite.values,
    labels={'x': 'Date', 'y': 'Index Value'},
    title="Hafzan Equity Composite Index (HECI) Base - 1000"
)
fig.write_html("chart.html")
