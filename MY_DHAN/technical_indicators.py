import pandas as pd
import pandas_ta as ta

def calculate_indicators(data_file="market_data.csv"):
    try:
        df = pd.read_csv(data_file)
        df = df[df["strike_price"] == df["strike_price"].iloc[-1]]  # Latest strike
        
        # Calculate indicators for Call LTP
        df["rsi"] = ta.rsi(df["call_ltp"], length=14)
        df["macd"], df["macd_signal"], _ = ta.macd(df["call_ltp"])
        df["atr"] = ta.atr(df["call_ltp"], df["call_ltp"], df["call_ltp"], length=14)
        df["ema"] = ta.ema(df["call_ltp"], length=20)
        supertrend = ta.supertrend(df["call_ltp"], df["call_ltp"], df["call_ltp"], length=10, multiplier=3)
        df["supertrend"] = supertrend["SUPERT_10_3.0"]
        
        # Generate signals
        latest = df.iloc[-1]
        signals = []
        if latest["rsi"] < 30:
            signals.append("Buy: RSI oversold")
        if latest["macd"] > latest["macd_signal"]:
            signals.append("Buy: MACD bullish crossover")
        if latest["call_ltp"] > latest["supertrend"]:
            signals.append("Buy: Above SuperTrend")
        
        print("\nTechnical Signals:")
        for signal in signals:
            print(signal)
        
        return df, signals
    except Exception as e:
        print(f"Error in indicators: {e}")
        return None, []

if __name__ == "__main__":
    df, signals = calculate_indicators()