import streamlit as st
import time  # for countdown
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

# Paths
model_path = os.path.join('models', 'temp_forecast_model.pkl')
data_path = r'D:\projects\weather forecasting\data\processed\live_weather.csv'

# Load model and data
model = joblib.load(model_path)
df = pd.read_csv(data_path)
df = df.sort_values('datetime')

# Prepare past data (last 12 entries)
recent_data = df.tail(12)
times = pd.to_datetime(recent_data['datetime'])
temps = recent_data['temperature']

# Get last 3 temperatures for forecasting
latest_temps = list(df['temperature'].tail(3).values)
n_steps = 6
predictions = []
for i in range(n_steps):
    features = [latest_temps[-1], latest_temps[-2], latest_temps[-3]]
    features.reverse()
    pred = model.predict([features])[0]
    predictions.append(pred)
    latest_temps.append(pred)

# Generate future timestamps (10 mins apart)
last_time = pd.to_datetime(df['datetime'].iloc[-1])
future_times = [last_time + pd.Timedelta(minutes=10 * (i+1)) for i in range(n_steps)]

# Streamlit App UI
st.set_page_config(page_title="Weather Forecast Dashboard", layout="centered")

# Auto-refresh every 60 seconds
st.markdown("""
    <script>
        function refreshPage() {
            window.location.reload();
        }
        setTimeout(refreshPage, 60000);  // 60 sec
    </script>
""", unsafe_allow_html=True)


st.title("🌦️ Real-time Weather Forecast")
st.markdown("Displays current data and forecasted temperature for the next 60 minutes.")

# Current weather
st.subheader("📌 Current Weather")
st.metric("Latest Temperature (°C)", f"{temps.values[-1]:.2f}")

# Forecast
st.subheader("📈 Forecast (Next 60 mins)")
forecast_df = pd.DataFrame({
    "Time": future_times,
    "Predicted Temp (°C)": predictions
})
st.dataframe(forecast_df.set_index("Time"))

# Plot
st.subheader("📊 Temperature Trend")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(times, temps, label="Actual", marker='o')
ax.plot(future_times, predictions, label="Forecast", linestyle='--', marker='x', color='orange')
ax.set_xlabel("Time")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Temperature: Past vs Forecast")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)
