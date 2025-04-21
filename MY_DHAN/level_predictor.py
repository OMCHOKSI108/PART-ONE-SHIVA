import pandas as pd

def predict_levels(data_file="market_data.csv"):
    try:
        df = pd.read_csv(data_file)
        latest_df = df[df["timestamp"] == df["timestamp"].max()]
        
        # Find support (max Put OI) and resistance (max Call OI)
        support_strike = latest_df.loc[latest_df["put_oi"].idxmax()]["strike_price"]
        resistance_strike = latest_df.loc[latest_df["call_oi"].idxmax()]["strike_price"]
        
        print("\nKey Levels:")
        print(f"NIFTY Support: {support_strike}")
        print(f"NIFTY Resistance: {resistance_strike}")
        
        return {"support": support_strike, "resistance": resistance_strike}
    except Exception as e:
        print(f"Error predicting levels: {e}")
        return {}

if __name__ == "__main__":
    levels = predict_levels()