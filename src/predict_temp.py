import pandas as pd
import joblib
import os

# Use absolute paths
model_path = r'D:\projects\weather forecasting\models\temp_forecast_model.pkl'
data_path = r'D:\projects\weather forecasting\data\processed\live_weather.csv'

# Load model
if not os.path.exists(model_path):
    print("Model file not found!")
    exit()

model = joblib.load(model_path)

# Load data
if not os.path.exists(data_path):
    print("Weather data not found!")
    exit()

df = pd.read_csv(data_path)
df = df.sort_values('datetime')

# Create lag features
df['target'] = df['temperature']
for i in range(1, 4):
    df[f'lag_{i}'] = df['target'].shift(i)

# Drop NA rows (due to shifting)
df.dropna(inplace=True)

# Get the latest valid row
latest = df.iloc[-1]

# Prepare input features
features = [[
    latest['lag_1'],
    latest['lag_2'],
    latest['lag_3']
]]

# Predict
predicted_temp = model.predict(features)[0]
print(f"Predicted next temperature: {predicted_temp:.2f} °C")
