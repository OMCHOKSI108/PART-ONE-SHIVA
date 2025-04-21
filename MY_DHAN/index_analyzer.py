import pandas as pd
from predictor import prepare_features

def analyze_indices(data_file="market_data.csv", index_file="market_data.csv"):
    try:
        df = pd.read_csv(data_file)
        index_data = pd.read_csv(index_file)
        
        indices = {"13": "NIFTY", "25": "BANKNIFTY", "1": "SENSEX"}
        analysis = []
        
        for idx in indices:
            idx_data = index_data[index_data["index"] == idx]
            if idx_data.empty:
                continue
            latest_price = idx_data["ltp"].iloc[-1]
            price_change = idx_data["ltp"].diff().iloc[-1]
            
            # Correlate with option chain
            call_oi_change = df["call_oi"].diff().sum()
            put_oi_change = df["put_oi"].diff().sum()
            
            if price_change > 0 and call_oi_change > put_oi_change:
                analysis.append(f"{indices[idx]} Up: Correlated with rising Call OI")
            elif price_change < 0 and put_oi_change > call_oi_change:
                analysis.append(f"{indices[idx]} Down: Correlated with rising Put OI")
            else:
                analysis.append(f"{indices[idx]} Flat: No clear OI trend")
        
        print("\nIndex Analysis:")
        for line in analysis:
            print(line)
        
        return analysis
    except Exception as e:
        print(f"Error in index analysis: {e}")
        return []

if __name__ == "__main__":
    analysis = analyze_indices()