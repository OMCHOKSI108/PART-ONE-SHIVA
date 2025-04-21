import pandas as pd
from datetime import datetime

def log_performance(accuracy, trades, file="performance_log.csv"):
    try:
        log_data = [{
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accuracy": accuracy,
            "trades_count": len(trades)
        }]
        df = pd.DataFrame(log_data)
        if os.path.exists(file):
            df.to_csv(file, mode="a", header=False, index=False)
        else:
            df.to_csv(file, index=False)
        print(f"Logged performance: Accuracy={accuracy}, Trades={len(trades)}")
    except Exception as e:
        print(f"Error logging performance: {e}")

if __name__ == "__main__":
    # Example usage
    log_performance(0.75, [{"sample": "trade"}])