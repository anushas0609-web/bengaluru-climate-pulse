import streamlit as st
import requests
import mysql.connector
import pandas as pd
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# 1. THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Bengaluru Climate Pulse", page_icon="🌍", layout="wide")

# 2. THE LOGIN FUNCTION
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["general"]["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Please enter the access code to view the dashboard", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Please enter the access code", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

# 3. THIS STOPS THE APP UNTIL THE PASSWORD IS ENTERED
if not check_password():
    st.stop() 

# --- IF WE REACH HERE, THE PASSWORD WAS CORRECT ---

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; color: #333333; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #FFFFFF; padding: 10px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab"] { height: 50px; border-radius: 8px; padding: 10px 20px; font-weight: bold; color: #555; }
    .stTabs [aria-selected="true"] { background-color: #E3F2FD; color: #007BFF; }
    .alert-high { background-color: #FFEBEE; border-left: 5px solid #D32F2F; padding: 15px; border-radius: 8px; margin-bottom: 15px; color: #B71C1C; }
    .alert-mod { background-color: #FFF8E1; border-left: 5px solid #FFA000; padding: 15px; border-radius: 8px; margin-bottom: 15px; color: #E65100; }
    .driver-alert { background: #E3F2FD; border-left: 6px solid #007BFF; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- FETCH LIVE DATA ---
@st.cache_data(ttl=600)
def get_live_data():
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=12.97&longitude=77.59&current=temperature_2m,relative_humidity_2m&daily=temperature_2m_max&timezone=Asia%2FKolkata"
    aqi_url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=12.97&longitude=77.59&current=us_aqi"
    
    weather_data = requests.get(weather_url).json()
    aqi_data = requests.get(aqi_url).json()
    
    return {
        "temp": weather_data['current']['temperature_2m'],
        "max_temp": weather_data['daily']['temperature_2m_max'][0],
        "humidity": weather_data['current']['relative_humidity_2m'],
        "aqi": aqi_data['current']['us_aqi'],
        "time": datetime.now().strftime('%I:%M %p')
    }

try:
    live_data = get_live_data()
except:
    st.error("Could not fetch live data. Please check your internet connection.")
    st.stop()

# --- APP HEADER ---
st.markdown("<h1 style='text-align: center; color: #007BFF;'>🌍 Bengaluru Climate Pulse</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #28A745; font-weight: bold;'>🟢 Live Data • {live_data['time']}</p>", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🚕 Driver Mode", "🏭 AI Impact"])

# --- PAGE 1: DASHBOARD ---
with tab1:
    st.markdown("### Current Conditions")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="🌡️ Temp", value=f"{live_data['temp']} °C")
    col2.metric(label="💧 Humidity", value=f"{live_data['humidity']} %")
    col3.metric(label="🍃 AQI", value=f"{live_data['aqi']}")
    
    st.markdown("---")
    st.markdown("### 🚨 Reservoir Supply Risk")
    
    try:
        db_password = st.secrets["general"]["mysql_password"]
        conn = mysql.connector.connect(host="localhost", user="root", password=db_password, database="Bengaluru_Environment")
        df_res = pd.read_sql("SELECT reservoir_name, current_level_tmc, full_capacity_tmc FROM Reservoir_Levels", conn)
        
        for index, row in df_res.iterrows():
            percent_full = (row['current_level_tmc'] / row['full_capacity_tmc']) * 100
            if percent_full < 60:
                st.markdown(f"<div class='alert-high'><b>{row['reservoir_name']}</b>: {percent_full:.1f}% full. Status: <b>High Risk</b></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='alert-mod'><b>{row['reservoir_name']}</b>: {percent_full:.1f}% full. Status: <b>Moderate Risk</b></div>", unsafe_allow_html=True)
        conn.close()
    except Exception as e:
        st.error(f"Database disconnected. Error: {e}")

    st.markdown("---")
    st.markdown("### 🗺️ Bengaluru Tech Hub Watch")
    st.markdown("Major IT hubs in Bengaluru driving data center growth.")
    
    # We create a dataframe with the specific locations
    map_data = pd.DataFrame({
        'lat': [13.0480, 12.9784, 12.8452],
        'lon': [77.6210, 77.7279, 77.6602],
        'name': ['Manyata Tech Park', 'Whitefield', 'Electronic City']
    })
    
    # Plot the map with a nice green color
    st.map(map_data, size=150, color="#28A745")

# --- PAGE 2: DRIVER MODE ---
with tab2:
    st.markdown("### 🚕 Daily Shift Planner")
    st.markdown("A quick action plan for your daily driving shift.")
    
    if live_data['max_temp'] > 30:
        st.error(f"🔥 **HEAT WARNING:** Max temp is {live_data['max_temp']}°C. Stay hydrated and use AC carefully.")
    else:
        st.success(f"🌤️ **Pleasant Weather:** Max temp is {live_data['max_temp']}°C. Good conditions for driving.")

    if live_data['aqi'] > 100:
        st.warning(f"😷 **AIR QUALITY ALERT:** AQI is {live_data['aqi']}. Keep windows up in heavy traffic.")
    else:
        st.info(f"🍃 **AQI is {live_data['aqi']} (Moderate).** Safe for your shift today.")

    st.markdown("---")
    st.markdown("### 🤖 AI Shift Prediction")
    st.markdown(f"""
    <div class="driver-alert">
        <h3>⏰ Plan Your Breaks</h3>
        <p>Based on AI forecasts, temperatures will peak between <b>1:00 PM and 4:00 PM</b> today. If you are on the road, expect high AC fuel usage and heat stress. Plan your water breaks accordingly.</p>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE 3: AI IMPACT ---
with tab3:
    st.markdown("### 🏭 The Hidden Cost of AI")
    st.markdown("Data centers run 24/7 to power AI. They use massive amounts of water for cooling.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Water per AI Chat", value="1.8 Litres", delta="Water bottle", delta_color="inverse")
    with col_b:
        st.metric(label="Water per Data Center", value="2B+ Litres/Yr", delta="Evaporated", delta_color="inverse")
        
    st.markdown("---")
    st.markdown("### 🚰 Calculate Your Impact")
    num_queries = st.slider("How many AI queries do you make in a day?", 1, 100, 10)
    litres_used = num_queries * 1.8
    buckets_used = litres_used / 18
    
    st.markdown(f"""
    <div style="background-color: #E3F2FD; border-left: 5px solid #007BFF; padding: 15px; border-radius: 5px; color: #0D47A1;">
        If you make <b>{num_queries}</b> queries a day, you are indirectly consuming <b>{litres_used:.1f} litres</b> of water daily.<br><br>
        That is equivalent to <b>{buckets_used:.1f} standard water buckets</b> evaporating into the sky just for AI.
    </div>
    """, unsafe_allow_html=True)