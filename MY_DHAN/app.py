import streamlit as st
from data_fetcher import fetch_data
from market_analyzer import analyze_market
from predictor import train_and_predict, prepare_features
from trade_generator import generate_trades
from level_predictor import predict_levels
from index_analyzer import analyze_indices
from fii_dii import fetch_fii_dii
import schedule
import time
import pandas as pd

st.title("SHIVA PART ONE: God of Stock Market")

# Initialize session state
if "data_fetched" not in st.session_state:
    st.session_state.data_fetched = False

def update_data():
    fetch_data()
    st.session_state.data_fetched = True

# Schedule data fetch
schedule.every(5).seconds.do(update_data)

# Run scheduler in background
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start scheduler in a separate thread
import threading
threading.Thread(target=run_scheduler, daemon=True).start()

# Display sections
if st.session_state.data_fetched:
    # Market Analysis
    st.header("Market Analysis")
    analysis = analyze_market()
    for line in analysis:
        st.write(line)
    
    # Predictions
    st.header("10-Minute Predictions")
    model, accuracy = train_and_predict()
    if model:
        direction = {1: "Up", -1: "Down", 0: "Flat"}[model.predict(prepare_features(pd.read_csv("market_data.csv")).tail(1))[0]]
        st.write(f"NIFTY Prediction: {direction} (Accuracy: {accuracy:.2f})")
    
    # Trades
    st.header("Generated Trades")
    trades = generate_trades()
    for trade in trades:
        st.write(f"Strategy: {trade['strategy'].capitalize()}, Expiry: {trade['expiry']}, {trade['action']}: {trade['instrument']}, Entry: {trade['entry']:.2f}, TP1: {trade['tp1']:.2f}, TP2: {trade['tp2']:.2f}, SL: {trade['sl']:.2f}")
    
    # Key Levels
    st.header("Key Levels")
    levels = predict_levels()
    if levels:
        st.write(f"NIFTY Support: {levels['support']}")
        st.write(f"NIFTY Resistance: {levels['resistance']}")
    
    # Index Analysis
    st.header("Index Analysis")
    index_analysis = analyze_indices()
    for line in index_analysis:
        st.write(line)
    
    # FII/DII Insights
    st.header("FII/DII Insights")
    fii_dii_data = fetch_fii_dii()
    for d in fii_dii_data:
        sentiment = "Bullish" if d["net"] > 0 else "Bearish"
        st.write(f"{d['name']} Net: ₹{d['net']} Cr ({sentiment})")

else:
    st.write("Fetching data... Please wait.")