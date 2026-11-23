import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

print("Connecting to MySQL to fetch historical data...")

# 1. Fetch data from MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Yonexa@2005",  # <-- CHANGE THIS
    database="Bengaluru_Environment"
)

query = "SELECT record_date, max_temp_c FROM Historical_Environment_Data ORDER BY record_date"
df = pd.read_sql(query, conn)
conn.close()

# 2. Prepare the data for AI
df['record_date'] = pd.to_datetime(df['record_date'])
df.set_index('record_date', inplace=True)

print(f"Loaded {len(df)} days of data. Training the AI model...")

# 3. Train the ARIMA Model (Time-Series Forecasting)
# ARIMA(5,1,0) means it looks at the last 5 days to predict the next day, with 1 degree of differencing (for trends)
model = ARIMA(df['max_temp_c'], order=(5,1,0))
model_fit = model.fit()

# 4. Forecast the next 30 days
forecast_steps = 30
forecast = model_fit.forecast(steps=forecast_steps)

print(f"\n✅ AI Model Trained! Here are the predicted Max Temperatures for the next 5 days in Bengaluru:")
for i, temp in enumerate(forecast.head(5)):
    print(f"Day {i+1}: {temp:.2f}°C")

# 5. Plot the results so you can see the AI working visually
plt.figure(figsize=(12,6))
plt.plot(df.index[-100:], df['max_temp_c'][-100:], label='Past 100 Days (Actual)', color='blue')
plt.plot(forecast.index, forecast, label='Next 30 Days (AI Prediction)', color='red', linestyle='--')
plt.title('Bengaluru Max Temperature: Actual vs AI Forecast')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)
plt.show()