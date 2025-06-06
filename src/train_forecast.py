# src/train_forecast.py

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import joblib

# Load and prepare data
df = pd.read_csv('D:/projects/weather forecasting/data/processed/live_weather.csv')
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.sort_values('datetime')

# Use only temperature for now
df['target'] = df['temperature']
for i in range(1, 4):  # 3 lag features: t-1, t-2, t-3
    df[f'lag_{i}'] = df['target'].shift(i)

df.dropna(inplace=True)

# Features and target
X = df[['lag_1', 'lag_2', 'lag_3']]
y = df['target']

# Split into train/test (80/20)
split = int(len(df) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print(f"Test MSE: {mse:.2f}")

# Plot actual vs predicted
plt.figure(figsize=(10, 5))
plt.plot(df['datetime'][split:], y_test, label='Actual', color='blue')
plt.plot(df['datetime'][split:], y_pred, label='Predicted', color='red')
plt.title('Temperature Forecasting')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

import os
import joblib

# Create models folder if it doesn't exist
model_dir = 'D:/projects/weather forecasting/models'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Save model
model_path = os.path.join(model_dir, 'temp_forecast_model.pkl')
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")
    