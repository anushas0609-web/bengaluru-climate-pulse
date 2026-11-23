import requests
import mysql.connector
from datetime import datetime

# --- 1. FETCH LIVE WEATHER & AQI ---
print("Fetching live Bengaluru data...")

# Weather API
weather_url = "https://api.open-meteo.com/v1/forecast?latitude=12.97&longitude=77.59&current=temperature_2m,relative_humidity_2m&timezone=Asia%2FKolkata"
weather_data = requests.get(weather_url).json()

# Air Quality API (Open-Meteo)
aqi_url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=12.97&longitude=77.59&current=us_aqi"
aqi_data = requests.get(aqi_url).json()

# Extract values
temp = weather_data['current']['temperature_2m']
humidity = weather_data['current']['relative_humidity_2m']
aqi = aqi_data['current']['us_aqi']
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print(f"Temperature: {temp}°C | Humidity: {humidity}% | AQI: {aqi}")

# --- 2. SAVE TO MYSQL ---
try:
    # Connect to MySQL (Replace 'root' and 'your_password' with your actual MySQL Workbench password)
    print("Connecting to MySQL...")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Yonexa@2005",  # <-- CHANGE THIS
        database="Bengaluru_Environment"
    )
    cursor = conn.cursor()

    # Create table if it doesn't exist (We are using the one we made earlier, but adding AQI)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Live_Environment_Data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME,
            temperature_c FLOAT,
            humidity_percent INT,
            aqi INT
        )
    """)

    # Insert the live data
    insert_query = """
        INSERT INTO Live_Environment_Data (timestamp, temperature_c, humidity_percent, aqi)
        VALUES (%s, %s, %s, %s)
    """
    record = (timestamp, temp, humidity, aqi)
    cursor.execute(insert_query, record)
    conn.commit()

    print("✅ Success! Live data saved to MySQL database.")

except mysql.connector.Error as err:
    print(f"❌ MySQL Error: {err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed.")