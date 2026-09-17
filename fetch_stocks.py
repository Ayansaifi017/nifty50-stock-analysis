import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 15 major Nifty 50 companies (Yahoo Finance uses .NS suffix for NSE stocks)
stocks = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Wipro": "WIPRO.NS",
    "HCL Tech": "HCLTECH.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Maruti": "MARUTI.NS",
    "Tata Motors": "TMPV.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "Larsen & Toubro": "LT.NS",
    "Axis Bank": "AXISBANK.NS"
}

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

all_data = []

for company_name, ticker in stocks.items():
    print(f"Downloading {company_name}...")
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    if df.empty:
        print(f"Skipping {company_name}: no data returned for {ticker}")
        continue
    df = df.reset_index()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [column[0] for column in df.columns]
    df["Company"] = company_name
    df["Ticker"] = ticker
    # Keep only useful columns
    df = df[["Date", "Company", "Ticker", "Open", "High", "Low", "Close", "Volume"]]
    all_data.append(df)

final_df = pd.concat(all_data, ignore_index=True)
final_df["Date"] = pd.to_datetime(final_df["Date"]).dt.date

# Save to Excel
output_file = "nifty_stocks_data.xlsx"
final_df.to_excel(output_file, index=False, sheet_name="Raw Data")
print(f"\nDone. File saved as: {output_file}")
print(f"Total rows: {len(final_df)}")