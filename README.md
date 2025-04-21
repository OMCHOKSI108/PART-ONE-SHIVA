Below is the file structure for "SHIVA PART ONE" with the addition of new trading strategies, as discussed in the previous response. This structure includes all necessary files for the project, organized to maintain clarity and modularity. It reflects the existing files from your codebase (data fetching with Dhan API, analysis, prediction, and Streamlit app) plus the modifications for adding strategies (in `technical_indicators.py`, `trade_generator.py`, and `app.py`).

---

### File Structure

```
SHIVA_PART_ONE/
│
├── market_data.csv           # Stores live option chain and index data
├── performance_log.csv       # Logs model accuracy and trade counts
├── model_YYYYMMDD.pkl        # Saved ML models (generated daily)
│
├── data_fetcher.py           # Fetches live data from Dhan API
├── market_analyzer.py        # Analyzes market movements (PCR, OI)
├── predictor.py              # Trains ML model for 10-min predictions
├── technical_indicators.py   # Calculates technical indicators and strategy signals
├── trade_generator.py        # Generates trades based on predictions and strategies
├── level_predictor.py        # Predicts support/resistance levels
├── index_analyzer.py         # Analyzes NIFTY, BANKNIFTY, SENSEX
├── fii_dii.py               # Scrapes FII/DII data
├── logger.py                # Logs performance metrics
├── app.py                   # Streamlit web app for UI
│
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

---

### File Descriptions

1. **market_data.csv**:
   - Stores live data (option chain: strike price, Call/Put OI, LTP, volume; index: NIFTY, BANKNIFTY, SENSEX LTP, volume) fetched every 5 seconds.
   - Format: CSV with columns like `timestamp`, `strike_price`, `call_oi`, `put_oi`, `call_ltp`, `put_ltp`, `index`, `ltp`, `volume`.

2. **performance_log.csv**:
   - Logs daily model accuracy and number of trades.
   - Format: CSV with columns `date`, `accuracy`, `trades_count`.

3. **model_YYYYMMDD.pkl**:
   - Saved Decision Tree models from `predictor.py`, named by date (e.g., `model_20250421.pkl`).
   - Used for predictions and continuous learning.

4. **data_fetcher.py**:
   - Fetches live NSE option chain and index data using Dhan API every 5 seconds during market hours (9:20 AM to 3:32 PM IST).
   - Saves data to `market_data.csv`.

5. **market_analyzer.py**:
   - Analyzes market movements using Put-Call Ratio (PCR) and OI changes.
   - Outputs explanations (e.g., “NIFTY up due to Call buying”).

6. **predictor.py**:
   - Trains a Decision Tree model every 5 seconds to predict index direction (up/down/flat) 10 minutes ahead.
   - Saves model daily and logs accuracy.

7. **technical_indicators.py**:
   - Calculates technical indicators (RSI, MACD, ATR, EMA, SuperTrend, Bollinger Bands).
   - Generates signals for strategies (e.g., momentum: RSI > 70 + MACD crossover; breakout: price > upper Bollinger Band).
   - Updated to include new strategy signals.

8. **trade_generator.py**:
   - Combines predictions and indicator signals to generate option trades (e.g., “BUY NIFTY 76500 CE”).
   - Updated to support new strategies (momentum, breakout) with strategy-specific TP/SL logic.

9. **level_predictor.py**:
   - Predicts key levels (support/resistance) based on highest Put/Call OI.

10. **index_analyzer.py**:
    - Analyzes NIFTY, BANKNIFTY, SENSEX movements and correlates with option chain data.

11. **fii_dii.py**:
    - Scrapes FII/DII data from Moneycontrol to show institutional sentiment.

12. **logger.py**:
    - Logs model performance (accuracy, trade counts) to `performance_log.csv`.

13. **app.py**:
    - Streamlit web app displaying trades, predictions, levels, index analysis, and FII/DII insights.
    - Updated to show strategy types for trades (e.g., “Strategy: Momentum”).

14. **requirements.txt**:
    - Lists Python dependencies for easy installation.
    - Example content:
      ```
      pandas
      numpy
      scikit-learn
      pandas_ta
      joblib
      streamlit
      requests
      beautifulsoup4
      schedule
      dhanhq-py
      ```

15. **README.md**:
    - Documents the project setup, usage, and file purposes.
    - Example content:
      ```
      # SHIVA PART ONE
      A self-learning trading tool for NSE options and indices using Dhan API.

      ## Setup
      1. Install dependencies: `pip install -r requirements.txt`
      2. Update `data_fetcher.py` with your Dhan API credentials.
      3. Run `app.py`: `streamlit run app.py`

      ## Files
      - `data_fetcher.py`: Fetches live data.
      - `app.py`: Streamlit UI.
      ...
      ```

---

### Notes
- **Dynamic Files**: `market_data.csv`, `performance_log.csv`, and `model_YYYYMMDD.pkl` are generated during runtime.
- **No New Files**: Adding strategies modifies existing files (`technical_indicators.py`, `trade_generator.py`, `app.py`) without requiring new ones, keeping the structure lean.
- **Organization**: Place all Python scripts in the root directory for simplicity, or group related files (e.g., `data/`, `analysis/`) if the project grows.
- **Version Control**: Use Git to track changes, especially since you’re updating files like `technical_indicators.py` and `trade_generator.py`.

This file structure aligns with your existing project (from the March 21, 2025 conversation) and incorporates the strategy additions seamlessly. Let me know if you need further clarification or assistance with implementing any part!