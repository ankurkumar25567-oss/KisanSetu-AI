import streamlit as st
import os
import json
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

st.set_page_config(page_title="KisanSetu - Empowering Farmers", page_icon="🌾", layout="wide")

# --- Fallback Data & Functions ---
INDIAN_LOCATIONS = {
    "Uttar Pradesh": ["Varanasi", "Lucknow", "Kanpur", "Prayagraj", "Etah"],
    "Delhi": ["New Delhi"],
    "Maharashtra": ["Mumbai", "Pune"],
    "Punjab": ["Amritsar", "Ludhiana"]
}

def get_current_location():
    return {"city": "Varanasi", "region": "Uttar Pradesh"}

def get_weather(city):
    return {"main": {"temp": 32}, "weather": [{"main": "Clear"}]}

def get_mandi_prices(commodity):
    prices = {
        "Wheat": {"price": "₹2400", "trend": "+₹50", "status": "Stable"},
        "Paddy": {"price": "₹2200", "trend": "+₹30", "status": "High Demand"},
        "Potato": {"price": "₹1500", "trend": "-₹20", "status": "Normal"},
        "Tomato": {"price": "₹3000", "trend": "+₹200", "status": "Rising"}
    }
    return prices.get(commodity, {"price": "₹2000", "trend": "0", "status": "Stable"})

# --- UI Translation Mapping ---
UI_TEXT = {
 "English": {
  "title": "🌾 KisanSetu (किसान सेतु)",
  "advisor": "🤖 AI Advisor",
  "market": "📊 Market & Weather",
  "diagnostics": "🔍 Crop Diagnostics",
  "tools": "🛠️ Tools",
  "iot": "📡 IoT Sensor Hub",
  "ask_label": "Ask about your crop, fertilizers, or soil:",
  "get_advice": "Get Expert Advice",
  "weather": "☁️ Weather Forecast",
  "mandi": "📈 Mandi Prices",
  "leaf": "🍃 Leaf Disease",
  "ocr": "📄 Bag OCR",
  "state_label": "Select State:",
  "city_label": "Select City:",
  "crop_label": "Select Crop",
  "extract_btn": "Extract Info",
  "translate_btn": "Translate",
  "temp": "Temperature",
  "condition": "Condition",
  "rain_warn": "⚠️ Rain Expected! Protect crops.",
  "status": "Market Status",
  "id_btn": "Identify Disease",
  "file_label": "📄 Upload Crop Doc or Image:",
  "analyze_btn": "Analyze File",
  "unit_label": "Select Unit:",
  "soil_moisture": "Soil Moisture",
  "simulate_btn": "Simulate ESP Data"
 },
 "Hindi (हिंदी)": {
  "title": "🌾 किसान सेतु",
  "advisor": "🤖 एआई सलाहकार",
  "market": "📊 बाजार और मौसम",
  "diagnostics": "🔍 फसल निदान",
  "tools": "🛠️ उपकरण",
  "iot": "📡 आईओटी सेंसर हब",
  "ask_label": "अपनी फसल, उर्वरक या मिट्टी के बारे में पूछें:",
  "get_advice": "विशेषज्ञ सलाह लें",
  "weather": "☁️ मौसम का पूर्वानुमान",
  "mandi": "📈 मंडी भाव",
  "leaf": "🍃 पत्ती रोग",
  "ocr": "📄 बैग ओसीआर (OCR)",
  "state_label": "राज्य चुनें:",
  "city_label": "शहर चुनें:",
  "crop_label": "फसल चुनें",
  "extract_btn": "जानकारी निकालें",
  "translate_btn": "अनुवाद करें",
  "temp": "तापमान",
  "condition": "स्थिति",
  "rain_warn": "⚠️ बारिश की संभावना! फसलों की रक्षा करें।",
  "status": "बाजार की स्थिति",
  "id_btn": "रोग पहचानें",
  "file_label": "📄 फसल दस्तावेज़ या छवि अपलोड करें:",
  "analyze_btn": "फ़ाइल का विश्लेषण करें",
  "unit_label": "इकाई चुनें:",
  "soil_moisture": "मिट्टी की नमी",
  "simulate_btn": "ESP डेटा सिमुलेट करें"
 }
}

# --- AI Configuration ---
api_key = os.getenv("GEMINI_API_KEY")
model_to_use = "gemini-1.5-flash"

if api_key:
 genai.configure(api_key=api_key)

# --- Sidebar ---
with st.sidebar:
 st.title("KisanSetu")
 language = st.selectbox("Select Language / भाषा", list(UI_TEXT.keys()))
 t = UI_TEXT[language]
 st.divider()

 if 'user_city' not in st.session_state:
  loc = get_current_location()
  st.session_state['user_city'] = loc['city']
  st.session_state['user_region'] = loc['region']

 state_list = list(INDIAN_LOCATIONS.keys())
 default_state_idx = 0
 if st.session_state['user_region'] in state_list:
  default_state_idx = state_list.index(st.session_state['user_region'])

 selected_state = st.selectbox(t["state_label"], state_list, index=default_state_idx)
 city_list = INDIAN_LOCATIONS[selected_state]
 default_city_idx = 0
 if st.session_state['user_city'] in city_list:
  default_city_idx = city_list.index(st.session_state['user_city'])

 city = st.selectbox(t["city_label"], city_list, index=default_city_idx)
 st.divider()

# --- Main UI ---
st.title(t["title"])
tabs = st.tabs([t["advisor"], t["market"], t["diagnostics"], t["tools"], t["iot"]])

# --- Tab 1: AI Advisor ---
with tabs[0]:
 st.header(t["advisor"])
 uploaded_file = st.file_uploader(t["file_label"], type=["jpg", "png", "jpeg", "pdf", "txt"])
 user_query = st.text_input(t["ask_label"], placeholder="e.g. What is the best fertilizer for wheat?")

 if st.button(t["get_advice"]):
  if not user_query and not uploaded_file:
   st.warning("Please enter a question or upload a file.")
  else:
   with st.spinner("Consulting AI..."):
    try:
     model = genai.GenerativeModel(model_to_use)
     content = [f"You are KisanSetu AI, an expert agronomist. Answer in {language}. Provide practical solutions."]
     if user_query: content.append(f"User Question: {user_query}")
     if uploaded_file:
      if uploaded_file.type.startswith("image"):
       content.append(Image.open(uploaded_file))
       content.append("Analyze this image provided by the farmer.")
      else:
       content.append(f"Document Content: {uploaded_file.getvalue().decode('utf-8', errors='ignore')[:2000]}")
     response = model.generate_content(content)
     st.success(response.text)
    except Exception as e:
     st.error(f"AI Error: {e}")

# --- Tab 2: Market & Weather ---
with tabs[1]:
 col_w, col_m = st.columns(2)
 with col_w:
  st.subheader(t["weather"])
  weather_data = get_weather(city)
  st.metric(t["temp"], f"{weather_data['main']['temp']}°C")
  st.write(f"{t['condition']}: {weather_data['weather'][0]['main']}")
 with col_m:
  st.subheader(t["mandi"])
  commodity = st.selectbox(t["crop_label"], ["Wheat", "Paddy", "Potato", "Tomato"])
  target_unit = st.selectbox(t["unit_label"], ["Quintal", "kg", "Tonne"])
  mandi_data = get_mandi_prices(commodity)
  base_price = int(mandi_data['price'].replace('₹', ''))
  display_price = base_price / 100 if target_unit == "kg" else (base_price * 10 if target_unit == "Tonne" else base_price)
  st.metric(f"{commodity}", f"₹{display_price:.2f} / {target_unit}", delta=mandi_data['trend'])
  st.info(f"{t['status']}: {mandi_data['status']}")

# --- Tab 3: Crop Diagnostics ---
with tabs[2]:
 st.subheader(t["diagnostics"])
 diag_tab1, diag_tab2 = st.tabs([t["leaf"], t["ocr"]])
 with diag_tab1:
  leaf_img = st.file_uploader("Upload leaf image...", type=["jpg", "png"], key="leaf")
  if leaf_img and st.button(t["id_btn"]):
   with st.spinner("Analyzing leaf..."):
    model = genai.GenerativeModel(model_to_use)
    response = model.generate_content(["Identify any plant disease in this leaf and recommend treatment in Hindi/English.", Image.open(leaf_img)])
    st.info(response.text)
 with diag_tab2:
  bag_img = st.file_uploader("Upload bag image...", type=["jpg", "png"], key="bag")
  if bag_img and st.button(t["extract_btn"]):
   with st.spinner("Reading text..."):
    model = genai.GenerativeModel(model_to_use)
    response = model.generate_content(["Extract and summarize all fertilizer/product details from this image.", Image.open(bag_img)])
    st.success(response.text)

# --- Tab 4: Tools ---
with tabs[3]:
 st.subheader(t["tools"])
 eng_text = st.text_area("Text to Translate:")
 if st.button(t["translate_btn"]):
  model = genai.GenerativeModel(model_to_use)
  response = model.generate_content(f"Translate the following agricultural text to {language}: {eng_text}")
  st.success(response.text)

# --- Tab 5: IoT Sensor Hub ---
with tabs[4]:
 st.subheader(t["iot"])
 DATA_FILE = "sensor_data.json"
 if st.button("🧪 " + t["simulate_btn"]):
  mock_data = {"soil_moisture": 42.5, "temperature": 31.0, "humidity": 65.0}
  with open(DATA_FILE, "w") as f:
   json.dump(mock_data, f)
  st.success("Simulated sensor data received!")

 if os.path.exists(DATA_FILE):
  with open(DATA_FILE, "r") as f:
   sensor = json.load(f)
  col1, col2, col3 = st.columns(3)
  col1.metric(f"💧 {t['soil_moisture']}", f"{sensor.get('soil_moisture')}%")
  col2.metric("🌡️ Temperature", f"{sensor.get('temperature')}°C")
  col3.metric("💨 Humidity", f"{sensor.get('humidity')}%")
 else:
  st.info("No sensor data received yet. Click simulate.")
 
