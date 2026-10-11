import streamlit as st
import os
import json
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Import our custom modules
from models.translator import translate
from models.ocr import read_text
from models.speech import speech_to_text, speak
from models.leaf_disease import predict
from services.weather import get_weather
from services.mandi import get_mandi_prices
from services.sms import send_alert
from services.location import get_current_location, INDIAN_LOCATIONS

# Load Environment Variables
load_dotenv()

# Page Config
st.set_page_config(page_title="KisanSetu - Empowering Farmers", page_icon="🌾", layout="wide")

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
 },
 "Punjabi (ਪੰਜਾਬੀ)": {
 "title": "🌾 ਕਿਸਾਨ ਸੇਤੂ",
 "advisor": "🤖 ਏਆਈ ਸਲਾਹਕਾਰ",
 "market": "📊 ਬਾਜ਼ਾਰ ਅਤੇ ਮੌਸਮ",
 "diagnostics": "🔍 ਫਸਲ ਨਿਦਾਨ",
 "tools": "🛠️ ਸੰਦ",
 "iot": "📡 IoT ਸੈਂਸਰ",
 "ask_label": "ਆਪਣੀ ਫਸਲ, ਖਾਦ ਜਾਂ ਮਿੱਟੀ ਬਾਰੇ ਪੁੱਛੋ:",
 "get_advice": "ਮਾਹਰ ਸਲਾਹ ਲਓ",
 "weather": "☁️ ਮੌਸਮ ਦੀ ਭਵਿੱਖਬਾਣੀ",
 "mandi": "📈 ਮੰਡੀ ਦੇ ਭਾਅ",
 "leaf": "🍃 ਪੱਤੇ ਦੇ ਰੋਗ",
 "ocr": "📄 ਬੈਗ ਓਸੀਆਰ",
 "state_label": "ਸੂਬਾ ਚੁਣੋ:",
 "city_label": "ਸ਼ਹਿਰ ਚੁਣੋ:",
 "crop_label": "ਫਸਲ ਚੁਣੋ",
 "extract_btn": "ਜਾਣਕਾਰੀ ਕੱਢੋ",
 "translate_btn": "ਅਨੁਵਾਦ ਕਰੋ",
 "temp": "ਤਾਪਮਾਨ",
 "condition": "ਹਾਲਤ",
 "rain_warn": "⚠️ ਮੀਂਹ ਦੀ ਉਮੀਦ! ਫਸਲਾਂ ਦੀ ਰਾਖੀ ਕਰੋ।",
 "status": "ਬਾਜ਼ਾਰ ਦੀ ਸਥਿਤੀ",
 "id_btn": "ਬਿਮਾਰੀ ਦੀ ਪਛਾਣ ਕਰੋ",
 "file_label": "📄 ਫਸਲ ਦਸਤਾਵੇਜ਼ ਜਾਂ ਚਿੱਤਰ ਅਪਲੋਡ ਕਰੋ:",
 "analyze_btn": "ਫਾਈਲ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ",
 "unit_label": "ਯੂਨਿਟ ਚੁਣੋ:",
 "soil_moisture": "ਮਿੱਟੀ ਦੀ ਨਮੀ",
 "simulate_btn": "ESP ਡੇਟਾ ਸਿमुलेट ਕਰੋ"
 },
 "Telugu (తెలుగు)": {
 "title": "🌾 కిసాన్ సేతు",
 "advisor": "🤖 AI సలహాదారు",
 "market": "📊 మార్కెట్ & వాతావరణం",
 "diagnostics": "🔍 పంట నిర్ధారణ",
 "tools": "🛠️ ఉపకరణాలు",
 "iot": "📡 IoT సెన్సార్",
 "ask_label": "మీ పంట, ఎరువులు లేదా నేల గురించి అడగండి:",
 "get_advice": "నిపుణుల సలహా తీసుకోండి",
 "weather": "☁️ వాతావరణ సూచన",
 "mandi": "📈 మండి ధరలు",
 "leaf": "🍃 ఆకు వ్యాధి",
 "ocr": "📄 బ్యాగ్ OCR",
 "state_label": "రాష్ట్రం ఎంచుకోండి:",
 "city_label": "నగరాన్ని ఎంచుకోండి:",
 "crop_label": "పంటను ఎంచుకోండి",
 "extract_btn": "సమాచారాన్ని సేకరించండి",
 "translate_btn": "అనువదించండి",
 "temp": "ఉష్ణోగ్రత",
 "condition": "పరిస్థితి",
 "rain_warn": "⚠️ వర్షం పడే అవకాశం ఉంది! పంటలను రక్షించండి.",
 "status": "మార్కెట్ స్థితి",
 "id_btn": "వ్యాధిని గుర్తించండి",
 "file_label": "📄 పంట పత్రం లేదా చిత్రాన్ని అప్‌లోడ్ చేయండి:",
 "analyze_btn": "ఫైల్‌ను విశ్లేషించండి",
 "unit_label": "యూనిట్ ఎంచుకోండి:",
 "soil_moisture": "నేల తేమ",
 "simulate_btn": "ESP డేటాను అనుకరించండి"
 }
}

# --- AI Configuration & Discovery ---
api_key = os.getenv("GEMINI_API_KEY")
model_to_use = "gemini-1.5-flash"

if api_key:
 genai.configure(api_key=api_key)
 try:
  all_models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
  available_models = [m for m in all_models if "2.5" not in m and "vision" not in m]
  if 'gemini-1.5-flash' in available_models: model_to_use = 'gemini-1.5-flash'
  elif 'gemini-1.5-pro' in available_models: model_to_use = 'gemini-1.5-pro'
  elif available_models: model_to_use = available_models[0]
 except Exception as e:
  st.sidebar.error(f"AI Discovery Error: {e}")

# --- Sidebar ---
with st.sidebar:
 st.image("https://cdn-icons-png.flaticon.com/512/2329/2329117.png", width=100)
 st.title("KisanSetu")
 language = st.selectbox("Select Language / भाषा", list(UI_TEXT.keys()))
 t = UI_TEXT[language]
 st.divider()

 if 'user_city' not in st.session_state:
  loc = get_current_location()
  st.session_state['user_city'] = loc['city']
  st.session_state['user_region'] = loc['region']

 st.subheader("📍 " + ("Location" if language == "English" else "स्थान"))
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

 if st.button("🛰️ " + ("Auto-Detect (GPS)" if language == "English" else "स्वचालित पहचान")):
  loc = get_current_location()
  st.session_state['user_city'] = loc['city']
  st.session_state['user_region'] = loc['region']
  st.rerun()

 st.divider()
 if 'available_models' in locals() and available_models:
  selected_model = st.selectbox("🤖 Choose AI Model:", available_models, index=available_models.index(model_to_use) if model_to_use in available_models else 0)
  model_to_use = selected_model

 st.success(f"Active AI: {model_to_use}")
 st.divider()
 st.warning("⚠️ **Disclaimer:** I am an AI acting as a plant pathologist. For large-scale commercial agricultural decisions, I recommend sending a soil and root sample to a certified laboratory.")

# --- Main UI ---
st.title(t["title"])

tabs = st.tabs([t["advisor"], t["market"], t["diagnostics"], t["tools"], t["iot"]])

# --- Tab 1: AI Advisor ---
with tabs[0]:
 st.header(t["advisor"])
 uploaded_file = st.file_uploader(t["file_label"], type=["jpg", "png", "jpeg", "pdf", "txt"])
 user_query = st.text_input(t["ask_label"], placeholder="e.g. What is written in this report?")

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
  if "error" in weather_data: st.warning(weather_data["error"])
  else:
   st.metric(t["temp"], f"{weather_data['main']['temp']}°C")
   st.write(f"{t['condition']}: {weather_data['weather'][0]['main']}")
   if "Rain" in weather_data['weather'][0]['main']: st.error(t["rain_warn"])

 with col_m:
  st.subheader(t["mandi"])
  commodity = st.selectbox(t["crop_label"], ["Wheat", "Paddy", "Potato", "Tomato"])
  target_unit = st.selectbox(t["unit_label"], ["Quintal", "kg", "Tonne"])
  mandi_data = get_mandi_prices(commodity)
  if mandi_data:
   base_price = int(mandi_data['price'].replace('₹', ''))
   display_price = base_price / 100 if target_unit == "kg" else (base_price * 10 if target_unit == "Tonne" else base_price)
   st.metric(f"{commodity}", f"₹{display_price:.2f} / {target_unit}", delta=mandi_data['trend'])
   st.info(f"{t['status']}: {mandi_data['status']}")

# --- Tab 3: Crop Diagnostics ---
with tabs[2]:
 st.subheader(t["diagnostics"])
 diag_tab1, diag_tab2 = st.tabs([t["leaf"], t["ocr"]])
 with diag_tab1:
  leaf_img = st.file_uploader("Upload leaf image...", type=["jpg", "png"])
  if leaf_img and st.button(t["id_btn"]):
   with open("temp_leaf.jpg", "wb") as f: f.write(leaf_img.getbuffer())
   st.info(predict("temp_leaf.jpg", model_name=model_to_use))
 with diag_tab2:
  bag_img = st.file_uploader("Upload bag image...", type=["jpg", "png"])
  if bag_img and st.button(t["extract_btn"]):
   with open("temp_bag.jpg", "wb") as f: f.write(bag_img.getbuffer())
   st.success(read_text("temp_bag.jpg", model_name=model_to_use))

# --- Tab 4: Tools ---
with tabs[3]:
 st.subheader(t["tools"])
 eng_text = st.text_area("English Text to Translate:")
 if st.button(t["translate_btn"]):
  st.success(translate(eng_text, model_name=model_to_use))

# --- Tab 5: IoT Sensor Hub ---
with tabs[4]:
 st.subheader(t["iot"])
 DATA_FILE = "sensor_data.json"

 if st.button("🧪 " + t["simulate_btn"]):
  mock_data = {"soil_moisture": 42.5, "temperature": 31.0, "humidity": 65.0, "status": "Optimal"}
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
  st.info("No sensor data received yet. Click simulate or connect your ESP.")

 st.markdown("---")
 st.markdown("### 🔌 Future ESP32 Code Snippet")
 st.code("""
# Use this on your ESP32 later to post data:
# HTTPClient http;
# http.begin("YOUR_APP_URL/update");
# http.addHeader("Content-Type", "application/json");
# http.POST("{\\"soil_moisture\\": 45, \\"temperature\\": 29}");
 """, language="cpp")
