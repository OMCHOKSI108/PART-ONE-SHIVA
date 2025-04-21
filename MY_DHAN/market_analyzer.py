import pandas as pd
from datetime import datetime, timedelta

def analyze_market(data_file="market_data.csv"):
    try:
        df = pd.read_csv(data_file)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        
        # Last 5 minutes of data
        time_threshold = datetime.now() - timedelta(minutes=5)
        recent_df = df[df["timestamp"] >= time_threshold]
        
        # Calculate PCR
        call_oi_sum = recent_df["call_oi"].sum()
        put_oi_sum = recent_df["put_oi"].sum()
        pcr = put_oi_sum / call_oi_sum if call_oi_sum > 0 else 0
        
        # OI changes
        call_oi_change = recent_df["call_oi"].diff().sum()
        put_oi_change = recent_df["put_oi"].diff().sum()
        
        # Simple market direction logic
        analysis = []
        if pcr > 1:
            analysis.append("Bearish: High Put-Call Ratio (PCR = {:.2f})".format(pcr))
        elif pcr < 1:
            analysis.append("Bullish: Low Put-Call Ratio (PCR = {:.2f})".format(pcr))
        else:
            analysis.append("Neutral: PCR near 1 (PCR = {:.2f})".format(pcr))
        
        if call_oi_change > put_oi_change:
            analysis.append("Bullish: Call OI increasing faster")
        elif put_oi_change > call_oi_change:
            analysis.append("Bearish: Put OI increasing faster")
        
        print("\nMarket Analysis:")
        for line in analysis:
            print(line)
        
        return analysis
    except Exception as e:
        print(f"Error in analysis: {e}")
        return []

if __name__ == "__main__":
    analyze_market()