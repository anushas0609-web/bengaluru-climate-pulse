import requests
import mysql.connector
from datetime import datetime

# --- 1. FETCH HISTORICAL WEATHER & AQI (Last 2 Years) ---
print("Fetching 2 years of historical data for Bengaluru...")

start_date = "2024-01-01"
end_date = datetime.now().strftime('%Y-%m-%d')

# Historical Weather API
weather_url = f"https://archive-api.open-meteo.com/v1/archive?latitude=12.97&longitude=77.59&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min&timezone=Asia%2FKolkata"
weather_data = requests.get(weather_url).json()

dates = weather_data['daily']['time']
max_temps = weather_data['daily']['temperature_2m_max']
min_temps = weather_data['daily']['temperature_2m_min']

# Historical AQI API (with safety check)
aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude=12.97&longitude=77.59&start_date={start_date}&end_date={end_date}&daily=us_aqi_max,us_aqi_min&timezone=Asia%2FKolkata"
aqi_response = requests.get(aqi_url).json()

# THE FIX: Check if 'daily' exists in the AQI response. If not, create empty lists.
if 'daily' in aqi_response and 'us_aqi_max' in aqi_response['daily']:
    aqi_max = aqi_response['daily']['us_aqi_max']
    aqi_min = aqi_response['daily']['us_aqi_min']
else:
    print("⚠️ Historical AQI data is currently unavailable from the API. Proceeding with weather data only.")
    aqi_max = [None] * len(dates)
    aqi_min = [None] * len(dates)

print(f"Fetched {len(dates)} days of data. Now saving to MySQL...")

# --- 2. SAVE TO MYSQL ---
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Yonexa@2005",  # <-- CHANGE THIS
        database="Bengaluru_Environment"
    )
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE Historical_Environment_Data")

    insert_query = """
        INSERT INTO Historical_Environment_Data (record_date, max_temp_c, min_temp_c, max_aqi, min_aqi)
        VALUES (%s, %s, %s, %s, %s)
    """

    for i in range(len(dates)):
        record = (
            dates[i], 
            max_temps[i], 
            min_temps[i], 
            aqi_max[i], 
            aqi_min[i]
        )
        cursor.execute(insert_query, record)

    conn.commit()
    print(f"✅ Success! {len(dates)} days of historical data saved to MySQL.")

except mysql.connector.Error as err:
    print(f"❌ MySQL Error: {err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed.")