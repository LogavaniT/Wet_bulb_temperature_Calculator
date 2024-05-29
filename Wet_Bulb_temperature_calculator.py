#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests
from PIL import Image
import numpy as np
import gdown
import os

# Function to calculate wet bulb temperature
def calculate_wet_bulb_temperature(temp, humidity):
    if temp < 0:
        return temp
    wet_bulb_temp = temp * np.arctan(0.151977 * (humidity + 8.313659)**0.5) + \
                    np.arctan(temp + humidity) - \
                    np.arctan(humidity - 1.676331) + \
                    0.00391838 * (humidity)**1.5 * np.arctan(0.023101 * humidity) - 4.686035
    return wet_bulb_temp

# Sidebar
st.sidebar.title("Weather Application")
page = st.sidebar.selectbox("Choose a page", ["Home", "Wet Bulb Calculator", "Historical Weather Data"])
st.sidebar.markdown("### Developed by Logavani T")
st.sidebar.markdown("#### References:")
st.sidebar.markdown("[Omni Calculator](https://www.omnicalculator.com/)")
st.sidebar.markdown("#### Data Sources:")
st.sidebar.markdown("[OpenWeatherMap](https://openweathermap.org/)")
st.sidebar.markdown("[Iowa Environmental Mesonet](https://mesonet.agron.iastate.edu/request/download.phtml)")

# Home Page
if page == "Home":
    st.title("🌡️ Wet Bulb Temperature")
    st.markdown("""
    India is currently experiencing severe heat waves, especially in the parts of coastal cities. So, have you ever walked outside on a summer day and immediately felt like you were being suffocated by the heat? Or perhaps you've heard the term "wet bulb temperature" being thrown around during a heatwave. In either case, understanding wet bulb temperature and its implications is crucial for staying safe and healthy in hot weather.

    Wet bulb temperature is a crucial factor in determining how hot it is outside and how our bodies respond to the heat. It is essential to pay attention to this measure and take necessary precautions during hot weather to avoid heat-related illnesses. 
    """)

    st.subheader("🤔 What is wet bulb temperature?")
    st.markdown("""
    Wet bulb temperature is a meteorological term used to describe the lowest temperature that can be reached by evaporating water into the air at constant pressure. It is measured by covering a thermometer bulb with a wet cloth and letting the water evaporate. As the water evaporates, it cools the thermometer, showing the wet bulb temperature. This temperature helps measure humidity and understand how much water can evaporate into the air, affecting things like comfort, farming, and weather patterns.
    """)

    st.subheader("🧮 How to calculate wet bulb temperature?")
    st.markdown("""
    Although many equations have been created over the years, our calculator uses the Stull formula, which is accurate for relative humidities between 5% and 99% and temperatures between -20°C and 50°C. The wet-bulb calculator is based on the following formula:

    𝑇𝑤 = 𝑇 arctan(0.151977 * (𝑅𝐻 + 8.313659)**0.5) + 0.00391838 * (𝑅𝐻)**1.5 arctan(0.023101 * 𝑅𝐻) − arctan(𝑅𝐻 − 1.676331) + arctan(𝑇 + 𝑅𝐻) − 4.686035**

    - **𝑇** — Temperature — air temperature or dry-bulb temperature is the temperature given by a thermometer not exposed to direct sunlight.
    - **𝑅𝐻[%]** — Relative humidity — a ratio of how much water vapor is in the air to how much it could contain at a given temperature.
    
    **Note:** Both temperature and wet bulb temperature in this formula are expressed in °C! If you would like to use other units, you need to convert them to the Celsius scale before you start calculations.
    """)

    st.subheader("🌟 What are the applications of wet bulb calculator?")
    st.markdown("""
    The wet-bulb temperature might not be a widely known measure, but it has some valuable functions:

    - **Construction:** Different materials react differently to different humidities, so this temperature is needed when designing a building in different climates.
    - **Snowmaking:** Snow production needs low temperatures, and when the humidity decreases, the temperature rises.
    - **Meteorology:** Forecasters use wet-bulb temperature to predict rain, snow, or freezing rain.
    """)

# Wet Bulb Calculator Page
elif page == "Wet Bulb Calculator":
    st.title("Wet Bulb Temperature Calculator")
    
    city = st.text_input("Enter city name")
    if city:
        api_key = "20fa20d7ac6bd2f12b306e91d5848608"
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(weather_url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wet_bulb_temp = calculate_wet_bulb_temperature(temp, humidity)
            
            st.write(f"Temperature: {temp}°C")
            st.write(f"Humidity: {humidity}%")
            st.write(f"Wet Bulb Temperature: {wet_bulb_temp:.2f}°C")
            
            if wet_bulb_temp > 35:
                st.markdown(f"<span style='color:red;'>Theoretically, humans cannot survive for very long when the wet-bulb temperature exceeds 35 °C (95 °F). If that's what you're experiencing, move to a place with air conditioning and drink lots of water as soon as possible. ☠️</span>", unsafe_allow_html=True)
            elif wet_bulb_temp > 30:
                st.markdown(f"<span style='color:blue;'>Wet-bulb temperatures exceeding 30°C (86°F) can be potentially fatal for humans outdoors and are extremely uncomfortable. In such conditions, it's crucial to avoid direct sunlight and stay well-hydrated.</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:green;'>The wet-bulb temperature is within a safe range. However, it's important to stay hydrated and seek shelter indoors if you start feeling the effects of the sun.</span>", unsafe_allow_html=True)
        else:
            st.write("City not found.")
    
    st.markdown("### Wet Bulb Calculator")
    temp_input = st.number_input("Enter temperature", value=0.0)
    temp_unit = st.selectbox("Temperature Unit", ["Celsius", "Fahrenheit"])
    if temp_unit == "Fahrenheit":
        temp_input = (temp_input - 32) * 5.0/9.0
    
    humidity_input = st.number_input("Enter relative humidity", value=0.0)
    
    if st.button("Calculate Wet Bulb Temperature"):
        wet_bulb_temp_input = calculate_wet_bulb_temperature(temp_input, humidity_input)
        if temp_unit == "Fahrenheit":
            wet_bulb_temp_input = wet_bulb_temp_input * 9.0/5.0 + 32
        st.write(f"Wet Bulb Temperature: {wet_bulb_temp_input:.2f} {temp_unit}")
        
        if wet_bulb_temp_input > 35:
            st.markdown(f"<span style='color:red;'>Theoretically, humans cannot survive for very long when the wet-bulb temperature exceeds 35 °C (95 °F). If that's what you're experiencing, move to a place with air conditioning and drink lots of water as soon as possible☠️.</span>", unsafe_allow_html=True)
        elif wet_bulb_temp_input > 30:
            st.markdown(f"<span style='color:blue;'>Wet-bulb temperatures exceeding 30°C (86°F) can be potentially fatal for humans outdoors and are extremely uncomfortable. In such conditions, it's crucial to avoid direct sunlight and stay well-hydrated.</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:green;'>The wet-bulb temperature is within a safe range. However, it's important to stay hydrated and seek shelter indoors if you start feeling the effects of the sun.</span>", unsafe_allow_html=True)

# Historical Weather Data Page
elif page == "Historical Weather Data":
    st.title("Historical Weather Data")
    
    cities = ["Chennai", "Kolkata", "Kochi", "Mumbai", "Delhi", "Bangalore", "Hyderabad","Calicut"]
    city_selection = st.selectbox("Select a city", cities)
    
    city_file_links = {
        "Chennai": "https://drive.google.com/uc?id=1vDCJ-UOPsTOWgQ4I1_MNp4W3HjJNDTbg",
        "Kolkata": "https://drive.google.com/uc?id=1swyyye0vxMkD_nRTVwtx40xHc56JQYtP",
        "Kochi": "https://drive.google.com/uc?id=1qKsdw-wDoNIbTL86kRMCrO-cCVZdhb-J",
        "Mumbai": "https://drive.google.com/uc?id=1MsKFKEY4SxSaNFmZEFCf2AnjClsOiv-I",
        "Delhi": "https://drive.google.com/uc?id=1tKc3Hy58I7vKRWVq25w_6q9Tda5FHs_Q",
        "Bangalore": "https://drive.google.com/uc?id=1s89mYBqAOnfbICqyVtULaWyUgNcfq4bp",
        "Hyderabad": "https://drive.google.com/uc?id=1pqX7QVz7y56Cxyz9uWgjjOYdgjl48WDB",
        "Calicut": "https://drive.google.com/uc?id=11nuUyqPMgXoL78-5rE-rKqZjI3MDh4s5"
    }
    
    if city_selection:
        file_link = city_file_links[city_selection]
        file_name = f"{city_selection}.jpg"
        gdown.download(file_link, file_name, quiet=False, use_cookies=False)
        
        if os.path.exists(file_name):
            image = Image.open(file_name)
            st.image(image, caption=f"{city_selection}'s historical wet bulb temperature trends")
        else:
            st.write("No historical data found for this city.")


# In[ ]:




