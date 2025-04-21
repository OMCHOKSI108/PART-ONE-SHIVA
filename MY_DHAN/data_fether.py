import pandas as pd
from dhanhq import DhanContext, dhanhq
import schedule
import time
from datetime import datetime, time as dt_time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch API key from environment variables
client_id = os.getenv("DHAN_API_KEY")
if not client_id:
    raise ValueError("DHAN_API_KEY is not set in the .env file")


access_token = os.getenv("C_ID")
if not access_token:
    raise ValueError("C_ID is not set in the .env file")


# Initialize Dhan API
dhan_context = DhanContext(client_id, access_token)
dhan = dhanhq(dhan_context)

# Market hours (9:20 AM to 3:32 PM IST)
MARKET_OPEN = dt_time(9, 20)
MARKET_CLOSE = dt_time(15, 32)

# Data storage
data_file = "market_data.csv"
option_chain_data = []

def is_market_open():
    now = datetime.now().time()
    return MARKET_OPEN <= now <= MARKET_CLOSE

def fetch_data():
    if not is_market_open():
        print("Market is closed.")
        return

    try:
        # Fetch option chain for NIFTY
        option_chain = dhan.option_chain(
            under_security_id=13,  # NIFTY
            under_exchange_segment="IDX_I",
            expiry="2025-04-24"  # Adjust to nearest expiry
        )
        
        # Fetch index LTP (NIFTY, BANKNIFTY, SENSEX)
        indices = [
            (dhan.NSE, "13"),  # NIFTY
            (dhan.NSE, "25"),  # BANKNIFTY
            (dhan.BSE, "1")    # SENSEX
        ]
        market_data = []
        for exchange, security_id in indices:
            quote = dhan.get_market_quote(security_id, exchange)
            market_data.append({
                "timestamp": datetime.now(),
                "index": security_id,
                "ltp": quote.get("last_price", 0),
                "volume": quote.get("volume", 0)
            })

        # Process option chain
        for strike in option_chain["data"]["oc"]:
            option_chain_data.append({
                "timestamp": datetime.now(),
                "strike_price": strike["strike_price"],
                "call_oi": strike.get("call_oi", 0),
                "put_oi": strike.get("put_oi", 0),
                "call_ltp": strike.get("call_ltp", 0),
                "put_ltp": strike.get("put_ltp", 0),
                "call_volume": strike.get("call_volume", 0),
                "put_volume": strike.get("put_volume", 0)
            })

        # Save to CSV
        df_option = pd.DataFrame(option_chain_data)
        df_market = pd.DataFrame(market_data)
        if os.path.exists(data_file):
            df_option.to_csv(data_file, mode="a", header=False, index=False)
        else:
            df_option.to_csv(data_file, index=False)
        print(f"Data saved at {datetime.now()}")

    except Exception as e:
        print(f"Error fetching data: {e}")

# Schedule data fetch every 5 seconds during market hours
schedule.every(5).seconds.do(fetch_data)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()