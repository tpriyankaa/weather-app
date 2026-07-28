import streamlit as st
import requests

# 1. Page Configuration (No HTML required!)
st.set_page_config(page_title="Weather Engine", page_icon="🌤️", layout="centered")

st.title("Python Weather Engine")
st.write("Enter a city name below to fetch real-time atmospheric data.")

# 2. Add your real OpenWeatherMap API Key here
API_KEY = "YOUR_API_KEY_HERE"

# 3. Form input and search button
city = st.text_input("Enter city name...", placeholder="e.g., London, Mumbai, New York")

if st.button("Search Weather", type="primary"):
    if city:
        url = f"http://openweathermap.org{city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(url).json()

            # 4. Check if the server answers cleanly
            if response.get("cod") == 200:
                name = response["name"]
                temp = round(response["main"]["temp"])
                desc = response["weather"][0]["description"].capitalize()
                humidity = response["main"]["humidity"]
                wind_speed = round(response["wind"]["speed"] * 3.6, 1) # Convert m/s to km/h

                # 5. Build a premium layout instantly using pure Python
                st.markdown("---")
                st.subheader(f"📍 {name}")
                st.metric(label="Current Temperature", value=f"{temp}°C")
                st.write(f"**Sky Condition:** {desc}")

                # Create two clean informational columns side-by-side
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"💧 **Humidity:** {humidity}%")
                with col2:
                    st.info(f"💨 **Wind Speed:** {wind_speed} km/h")
                    
            else:
                st.error("City not found! Please check your spelling and try again.")
        except Exception:
            st.error("Network connection failed. Could not reach weather servers.")
    else:
        st.warning("Please type a city name first.")
        
