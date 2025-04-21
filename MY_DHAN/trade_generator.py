from predictor import train_and_predict, prepare_features
from technical_indicators import calculate_indicators
import pandas as pd
from datetime import datetime

def generate_trades(data_file="market_data.csv"):
    try:
        # Get predictions
        model, accuracy = train_and_predict(data_file)
        prediction = model.predict(prepare_features(pd.read_csv(data_file)).tail(1))[0] if model else 0
        
        # Get indicators and signals
        df, signals = calculate_indicators(data_file)
        latest = df.iloc[-1]
        
        trades = []
        for signal in signals:
            strategy_type = signal["type"]
            if prediction == 1 and "Buy" in signal["signal"]:  # Bullish prediction
                entry = latest["call_ltp"]
                atr = latest["atr"]
                trade = {
                    "timestamp": datetime.now(),
                    "instrument": f"NIFTY {latest['strike_price']} CE",
                    "action": "BUY",
                    "entry": entry,
                    "tp1": entry * (1.5 if strategy_type == "momentum" else 1.3),  # Higher TP for momentum
                    "tp2": entry * (2.0 if strategy_type == "momentum" else 1.6),
                    "sl": entry - (atr * 1.5 if strategy_type == "breakout" else atr),  # Wider SL for breakout
                    "expiry": "2025-04-24",
                    "strategy": strategy_type
                }
                trades.append(trade)
        
        print("\nGenerated Trades:")
        for trade in trades:
            print(f"Strategy: {trade['strategy']}, Expiry: {trade['expiry']}, {trade['action']}: {trade['instrument']}, Entry: {trade['entry']:.2f}, TP1: {trade['tp1']:.2f}, TP2: {trade['tp2']:.2f}, SL: {trade['sl']:.2f}")
        
        return trades
    except Exception as e:
        print(f"Error generating trades: {e}")
        return []

if __name__ == "__main__":
    trades = generate_trades()