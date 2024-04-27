import pandas as pd
import numpy as np
import yfinance as yf

# Download historical data for a currency pair
def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Calculate moving averages
def calculate_sma(data, window):
    sma = data['Close'].rolling(window=window).mean()
    return sma

# Calculate MACD
def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    exp1 = data['Close'].ewm(span=fast_period, adjust=False).mean()
    exp2 = data['Close'].ewm(span=slow_period, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, signal_line

# Check strategy conditions
def check_strategy(data, strategy):
    sma_10 = calculate_sma(data, 10)
    sma_30 = calculate_sma(data, 30)
    sma_50 = calculate_sma(data, 50)
    sma_200 = calculate_sma(data, 200)
    macd, signal_line = calculate_macd(data)

    if strategy == 'A':
        return (sma_10[-1] < sma_30[-1] and
                macd[-1] > signal_line[-1] and
                macd[-1] < 0 and
                sma_10[-1] > sma_50[-1] and
                sma_30[-1] > sma_50[-1] and
                sma_50[-1] < sma_200[-1])

    elif strategy == 'B':
        return (sma_10[-1] < sma_30[-1] and
                macd[-1] > signal_line[-1] and
                macd[-1] < 0 and
                sma_10[-1] > sma_50[-1] and
                sma_30[-1] > sma_50[-1] and
                sma_50[-1] > sma_200[-1])

    elif strategy == 'C':
        return (sma_10[-1] > sma_30[-1] and
                macd[-1] > signal_line[-1] and
                macd[-1] < 0 and
                sma_10[-1] > sma_50[-1] and
                sma_30[-1] > sma_50[-1] and
                sma_50[-1] < sma_200[-1])

    elif strategy == 'D':
        return (sma_10[-1] > sma_30[-1] and
                macd[-1] < signal_line[-1] and
                macd[-1] > 0 and
                sma_10[-1] < sma_50[-1] and
                sma_30[-1] < sma_50[-1] and
                sma_50[-1] < sma_200[-1])

# Main function to execute strategies
def main():
    ticker = 'EURUSD=X'  # Example currency pair
    start_date = '2023-01-01'
    end_date = '2024-01-01'

    data = download_data(ticker, start_date, end_date)

    # Check Strategy A
    if check_strategy(data, 'A'):
        print("Strategy A: Buy Signal")
    else:
        print("Strategy A: No Buy Signal")

    # Check Strategy B
    if check_strategy(data, 'B'):
        print("Strategy B: Buy Signal")
    else:
        print("Strategy B: No Buy Signal")

    # Check Strategy C
    if check_strategy(data, 'C'):
        print("Strategy C: Buy Signal")
    else:
        print("Strategy C: No Buy Signal")

    # Check Strategy D
    if check_strategy(data, 'D'):
        print("Strategy D: Buy Signal")
    else:
        print("Strategy D: No Buy Signal")

if __name__ == "__main__":
    main()