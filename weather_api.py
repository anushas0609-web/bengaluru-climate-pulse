import requests
import pandas as pd
from datetime import datetime

# 1. Set up the API URL for Bengaluru (Latitude: 12.97, Longitude: 77.59)
# We are asking for current temp, humidity, and today's max/min temp.
url = "https://api.open-meteo.com/v1/forecast?latitude=12.97&longitude=77.59&current=temperature_2m,relative_humidity_2m&daily=temperature_2m_max,temperature_2m_min&timezone=Asia%2FKolkata"

print("Fetching live data from Bengaluru...")

# 2. Make the request to the API
response = requests.get(url)
data = response.json()

# 3. Extract the specific data we want
current_temp = data['current']['temperature_2m']
humidity = data['current']['relative_humidity_2m']
max_temp = data['daily']['temperature_2m_max'][0]
min_temp = data['daily']['temperature_2m_min'][0]
date_today = data['daily']['time'][0]

# 4. Print the results beautifully
print("\n--- Live Bengaluru Weather ---")
print(f"Date: {date_today}")
print(f"Current Temperature: {current_temp}°C")
print(f"Current Humidity: {humidity}%")
print(f"Today's Max Temp: {max_temp}°C")
print(f"Today's Min Temp: {min_temp}°C")
print("------------------------------")

# 5. (Optional) Save it to a CSV file so you can open it in Excel later!
weather_df = pd.DataFrame({
    'Date': [date_today],
    'Current_Temp_C': [current_temp],
    'Humidity_%': [humidity],
    'Max_Temp_C': [max_temp],
    'Min_Temp_C': [min_temp]
})

weather_df.to_csv('bengaluru_live_weather.csv', index=False)
print("\nData saved to 'bengaluru_live_weather.csv'!")