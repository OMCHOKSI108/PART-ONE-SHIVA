import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from datetime import datetime, timedelta

def prepare_features(df):
    df["pcr"] = df["put_oi"] / df["call_oi"].replace(0, 1)
    df["call_oi_change"] = df["call_oi"].diff()
    df["put_oi_change"] = df["put_oi"].diff()
    return df[["pcr", "call_oi_change", "put_oi_change"]].fillna(0)

def prepare_target(df, index_data, minutes=10):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    index_data["timestamp"] = pd.to_datetime(index_data["timestamp"])
    targets = []
    for i, row in df.iterrows():
        future_time = row["timestamp"] + timedelta(minutes=minutes)
        future_price = index_data[index_data["timestamp"] >= future_time]["ltp"].iloc[0] if not index_data[index_data["timestamp"] >= future_time].empty else None
        current_price = index_data[index_data["timestamp"] <= row["timestamp"]]["ltp"].iloc[-1] if not index_data[index_data["timestamp"] <= row["timestamp"]].empty else None
        if future_price and current_price:
            if future_price > current_price * 1.005:
                targets.append(1)  # Up
            elif future_price < current_price * 0.995:
                targets.append(-1)  # Down
            else:
                targets.append(0)  # Flat
        else:
            targets.append(0)
    return targets

def train_and_predict(data_file="market_data.csv", index_file="market_data.csv"):
    try:
        df = pd.read_csv(data_file)
        index_data = pd.read_csv(index_file)  # Filter for NIFTY
        index_data = index_data[index_data["index"] == "13"]
        
        X = prepare_features(df)
        y = prepare_target(df, index_data)
        
        if len(X) < 10 or len(y) < 10:
            print("Not enough data for training")
            return None, 0
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = DecisionTreeClassifier(max_depth=5)
        model.fit(X_train, y_train)
        
        # Predict and evaluate
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Prediction Accuracy: {accuracy:.2f}")
        
        # Save model
        joblib.dump(model, f"model_{datetime.now().strftime('%Y%m%d')}.pkl")
        
        # Latest prediction
        latest_features = X.tail(1)
        prediction = model.predict(latest_features)[0]
        direction = {1: "Up", -1: "Down", 0: "Flat"}[prediction]
        print(f"Next 10-min Prediction: NIFTY will go {direction}")
        
        return model, accuracy
    except Exception as e:
        print(f"Error in prediction: {e}")
        return None, 0

if __name__ == "__main__":
    model, accuracy = train_and_predict()