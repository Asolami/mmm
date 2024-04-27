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

# Check strategy conditions for binary options with expiration time
def check_strategy_binary_with_expiration(data, strategy, expiration_days=1):
    sma_10 = calculate_sma(data, 10)
    sma_30 = calculate_sma(data, 30)
    sma_50 = calculate_sma(data, 50)
    sma_200 = calculate_sma(data, 200)
    macd, signal_line = calculate_macd(data)

    # Check conditions based on the data at expiration time
    data_expiration = data.iloc[-expiration_days:]  # Data at expiration time
    sma_10_exp = calculate_sma(data_expiration, 10)
    sma_30_exp = calculate_sma(data_expiration, 30)
    sma_50_exp = calculate_sma(data_expiration, 50)
    sma_200_exp = calculate_sma(data_expiration, 200)
    macd_exp, signal_line_exp = calculate_macd(data_expiration)

    if strategy == 'A':
        return (sma_10[-1] < sma_30[-1] and
                macd[-1] > signal_line[-1] and
                macd[-1] < 0 and
                sma_10[-1] > sma_50[-1] and
                sma_30[-1] > sma_50[-1] and
                sma_50[-1] < sma_200[-1] and
                sma_10_exp[-1] > sma_30_exp[-1])

    elif strategy == 'B':
        return (sma_10[-1] < sma_30[-1] and
                macd[-1] > signal_line[-1] and
                macd[-1] < 0 and
                sma_10[-1] > sma_50[-1] and
                sma_30[-1] > sma_50[-1] and
                sma_50[-1] > sma_200[-1] and
                sma_10_exp[-1] > sma_30_exp[-1])

    elif strategy == 'C':
        return (sma_10[-1] > sma_30[-1] and
                macd[-1] > signal_line[-1] and
                macd[-1] < 0 and
                sma_10[-1] > sma_50[-1] and
                sma_30[-1] > sma_50[-1] and
                sma_50[-1] < sma_200[-1] and
                sma_10_exp[-1] < sma_30_exp[-1])

    elif strategy == 'D':
        return (sma_10[-1] > sma_30[-1] and
                macd[-1] < signal_line[-1] and
                macd[-1] > 0 and
                sma_10[-1] < sma_50[-1] and
                sma_30[-1] < sma_50[-1] and
                sma_50[-1] < sma_200[-1] and
                sma_10_exp[-1] < sma_30_exp[-1])

# Main function to execute strategies for binary options with expiration time
def main_binary_with_expiration():
    ticker = 'EURUSD=X'  # Example currency pair
    start_date = '2023-01-01'
    end_date = '2024-01-01'
    expiration_days = 1  # Expiration time in days

    data = download_data(ticker, start_date, end_date)

    # Check Strategy A
    if check_strategy_binary_with_expiration(data, 'A', expiration_days):
        print("Strategy A: Call Option Signal")
    else:
        print("Strategy A: No Call Option Signal")

    # Check Strategy B
    if check_strategy_binary_with_expiration(data, 'B', expiration_days):
        print("Strategy B: Call Option Signal")
    else:
        print("Strategy B: No Call Option Signal")

    # Check Strategy C
    if check_strategy_binary_with_expiration(data, 'C', expiration_days):
        print("Strategy C: Call Option Signal")
    else:
        print("Strategy C: No Call Option Signal")

    # Check Strategy D
    if check_strategy_binary_with_expiration(data, 'D', expiration_days):
        print("Strategy D: Call Option Signal")
    else:
        print("Strategy D: No Call Option Signal")

if __name__ == "__main__":
    main_binary_with_expiration()