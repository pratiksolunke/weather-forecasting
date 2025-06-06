import requests
import pandas as pd
from datetime import datetime
import os

def get_weather(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    weather = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "weather": data["weather"][0]["description"]
    }
    
    return weather

def append_to_csv(weather, filepath="data/processed/live_weather.csv"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df = pd.DataFrame([weather])
    try:
        old_df = pd.read_csv(filepath)
        df = pd.concat([old_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv(filepath, index=False)
    print("✅ Weather data saved.")

if __name__ == "__main__":
    API_KEY = "73e1de42f49bdd849faf6079d092ed74"  # Your API key
    CITY = "Mumbai"  # You can change to any city like "Delhi", "London", etc.
    
    weather_data = get_weather(CITY, API_KEY)
    append_to_csv(weather_data)
