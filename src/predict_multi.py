import pandas as pd
import joblib
import os

# Setup paths
model_path = r'D:\projects\weather forecasting\models\temp_forecast_model.pkl'
data_path = r'D:\projects\weather forecasting\data\processed\live_weather.csv'

# Load model
model = joblib.load(model_path)

# Load latest temperature data
df = pd.read_csv(data_path)
df = df.sort_values('datetime')

# Get last 3 temperature values
latest_temps = list(df['temperature'].tail(3).values)

# Forecast horizon (how many steps ahead)
n_steps = 6
predictions = []

# Recursive multi-step forecast
for i in range(n_steps):
    features = [latest_temps[-1], latest_temps[-2], latest_temps[-3]]
    features.reverse()  # Because model expects [lag_1, lag_2, lag_3]
    pred = model.predict([features])[0]
    predictions.append(pred)
    latest_temps.append(pred)  # Add prediction to list

# Show results
for i, temp in enumerate(predictions, 1):
    print(f"Predicted temperature at T+{i*10} min: {temp:.2f} °C")
