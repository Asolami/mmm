from quotexapi.stable_api import Quotex
import talib

def get_currency_pairs():
    return [
        "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD",
        "CADCHF", "CADJPY", "CHFJPY",
        "EURAUD", "EURCAD", "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURUSD",
        "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD", "GBPUSD",
        "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD",
        "USDCAD", "USDCHF", "USDJPY",
    ]

def calculate_rsi(closes, period):
    rsi = talib.RSI(closes, timeperiod=period)
    return rsi[-1]

def calculate_adx(highs, lows, closes, period):
    adx = talib.ADX(highs, lows, closes, timeperiod=period)
    return adx[-1]

def calculate_sma(closes, period):
    sma = sum(closes[-period:]) / period
    return sma

def moving_average_crossover_with_rsi(closes, rsi_value, short_period, long_period):
    short_sma = calculate_sma(closes, short_period)
    long_sma = calculate_sma(closes, long_period)
    
    if short_sma > long_sma and rsi_value > 50:
        return "buy"
    elif short_sma < long_sma and rsi_value < 50:
        return "sell"
    else:
        return "hold"

def bollinger_bands_squeeze_with_macd(closes, macd, signal, squeeze_threshold):
    bollinger_upper, bollinger_middle, bollinger_lower = talib.BBANDS(closes)
    squeeze_condition = bollinger_upper[-1] - bollinger_lower[-1] < squeeze_threshold
    
    if squeeze_condition and macd > signal:
        return "buy"
    elif not squeeze_condition and macd < signal:
        return "sell"
    else:
        return "hold"

def stochastic_oscillator_divergence_with_ma_cross(stoch_value, stoch_signal, ma_short, ma_long):
    if stoch_value > stoch_signal and ma_short > ma_long:
        return "buy"
    elif stoch_value < stoch_signal and ma_short < ma_long:
        return "sell"
    else:
        return "hold"

def volume_spike_with_rsi(volume, rsi_value):
    if volume > 0 and rsi_value > 50:
        return "buy"
    elif volume > 0 and rsi_value < 50:
        return "sell"
    else:
        return "hold"

# Add more trading strategy functions for other techniques...

def main():
    # Replace the placeholders with your actual Quotex account credentials
    email = "asolakhaleed@gmail.com"
    password = "TheKhaleed3."
    
    # Create an instance of the Quotex class and connect to the API
    account = Quotex(host="broker-qx.com", email=email, password=password)
    check_connect, message = account.connect()

    if check_connect:
        print("Connected to Quotex API successfully")
        
        # Get account balance
        account.change_balance("PRACTICE")  # Change balance type to PRACTICE or REAL
        balance = account.get_balance()
        print(f"Account balance: {balance}")

        # Implement your strategy here
        currency_pairs = get_currency_pairs()

        for asset in currency_pairs:
            candles = account.get_candle_v2(asset, 60)  # Get 1-minute candles

            # Extract candle data
            closes = [candle["close"] for candle in candles]
            volume = [candle["volume"] for candle in candles]

            # Calculate indicators
            rsi_value = calculate_rsi(closes, 14)
            ma_short = calculate_sma(closes, 20)
            ma_long = calculate_sma(closes, 50)

            # Example of using moving_average_crossover_with_rsi strategy
            signal = moving_average_crossover_with_rsi(closes, rsi_value, 20, 50)

            # Example of using bollinger_bands_squeeze_with_macd strategy
            macd, signal_line, _ = talib.MACD(closes)
            signal = bollinger_bands_squeeze_with_macd(closes, macd[-1], signal_line[-1], 0.05)

            # Example of using stochastic_oscillator_divergence_with_ma_cross strategy
            _, stoch_signal = talib.STOCH(highs, lows, closes)
            stoch_value = _, _ = talib.STOCHF(highs, lows, closes)
            signal = stochastic_oscillator_divergence_with_ma_cross(stoch_value[-1], stoch_signal[-1], ma_short, ma_long)

            # Example of using volume_spike_with_rsi strategy
            signal = volume_spike_with_rsi(volume[-1], rsi_value)

            # Add more strategies...

            if signal == "buy":
                amount = 1
                direction = "call"  # "call" for up
                duration = 60  # Duration of the option in seconds
                buy_response = account.buy(asset, amount, direction, duration)
                print(f"Buy response for {asset}: {buy_response}")
            elif signal == "sell":
                amount = 1
                direction = "put"  # "put" for down
                duration = 60  # Duration of the option in seconds
                sell_response = account.buy(asset, amount, direction, duration)
                print(f"Sell response for {asset}: {sell_response}")
            else: