import time
from src.fetch_weather import get_weather, append_to_csv

API_KEY = "73e1de42f49bdd849faf6079d092ed74"
CITY = "Mumbai"
INTERVAL = 600  # time in seconds (600 = 10 minutes)

print("📡 Starting live weather logging... Press Ctrl+C to stop.")

try:
    while True:
        weather_data = get_weather(CITY, API_KEY)
        append_to_csv(weather_data)
        print("⏳ Waiting for next fetch...")
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    print("🛑 Logging stopped by user.")
