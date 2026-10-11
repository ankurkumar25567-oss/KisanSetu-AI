import streamlit as st
import os
import json
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

st.set_page_config(page_title="KisanSetu - Empowering Farmers", page_icon="🌾", layout="wide")

# --- Expanded Indian Locations ---
INDIAN_LOCATIONS = {
    "Uttar Pradesh": ["Varanasi", "Lucknow", "Kanpur", "Prayagraj", "Agra", "Meerut", "Etah", "Gorakhpur", "Bareilly", "Noida"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Purnia", "Darbhanga", "Ara", "Begusarai"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur", "Amravati", "Kolhapur"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Kharagpur", "Bardhaman"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain", "Sagar", "Dewas", "Satna"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Erode"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru", "Belagavi", "Davangere", "Ballari"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Junagadh", "Gandhinagar"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner", "Alwar", "Bhilwara"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala", "Bathinda", "Hoshiarpur", "Mohali"],
    "Haryana": ["Chandigarh", "Gurugram", "Faridabad", "Panipat", "Ambala", "Yamunanagar", "Rohtak"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Palakkad", "Alappuzha"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur", "Puri", "Balasore"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Tinsukia", "Nagaon", "Tezpur"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam", "Ramagundam"],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Tirupati", "Kakinada"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar", "Hazaribagh", "Giridih"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Durg", "Rajnandgaon", "Jagdalpur"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Nainital", "Rudrapur", "Rishikesh"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Solan", "Mandi", "Bilaspur", "Kullu"],
    "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi", "Central Delhi"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Udhampur", "Kathua"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda"]
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
        "title": "🌾 KisanSetu", "advisor": "🤖 AI Advisor", "market": "📊 Market & Weather", 
        "diagnostics": "🔍 Crop Diagnostics", "tools": "🛠️ Tools", "iot": "📡 IoT Sensor Hub", 
        "ask_label": "Ask about your crop, fertilizers, or soil:", "get_advice": "Get Expert Advice", 
        "weather": "☁️ Weather Forecast", "mandi": "📈 Mandi Prices", "leaf": "🍃 Leaf Disease", 
        "ocr": "📄 Bag OCR", "state_label": "Select State:", "city_label": "Select City:", 
        "crop_label": "Select Crop", "extract_btn": "Extract Info", "translate_btn": "Translate", 
        "temp": "Temperature", "condition": "Condition", "rain_warn": "⚠️ Rain Expected! Protect crops.", 
        "status": "Market Status", "id_btn": "Identify Disease", "file_label": "📄 Upload Crop Doc or Image:", 
        "unit_label": "Select Unit:", "soil_moisture": "Soil Moisture", "simulate_btn": "Simulate ESP Data"
    },
    "Hindi (हिंदी)": {
        "title": "🌾 किसान सेतु", "advisor": "🤖 एआई सलाहकार", "market": "📊 बाजार और मौसम", 
        "diagnostics": "🔍 फसल निदान", "tools": "🛠️ उपकरण", "iot": "📡 आईओटी सेंसर हब", 
        "ask_label": "अपनी फसल, उर्वरक या मिट्टी के बारे में पूछें:", "get_advice": "विशेषज्ञ सलाह लें", 
        "weather": "☁️ मौसम का पूर्वानुमान", "mandi": "📈 मंडी भाव", "leaf": "🍃 पत्ती रोग", 
        "ocr": "📄 बैग ओसीआर", "state_label": "राज्य चुनें:", "city_label": "शहर चुनें:", 
        "crop_label": "फसल चुनें", "extract_btn": "जानकारी निकालें", "translate_btn": "अनुवाद करें", 
        "temp": "तापमान", "condition": "स्थिति", "rain_warn": "⚠️ बारिश की संभावना! फसलों की रक्षा करें।", 
        "status": "बाजार की स्थिति", "id_btn": "रोग पहचानें", "file_label": "📄 फसल दस्तावेज़ या छवि अपलोड करें:", 
        "unit_label": "इकाई चुनें:", "soil_moisture": "मिट्टी की नमी", "simulate_btn": "ESP डेटा सिमुलेट करें"
    },
    "Bengali (বাংলা)": {
        "title": "🌾 কিষাণ সেতু", "advisor": "🤖 এআই উপদেষ্টা", "market": "📊 বাজার ও আবহাওয়া", 
        "diagnostics": "🔍 ফসল নির্ণয়", "tools": "🛠️ সরঞ্জাম", "iot": "📡 আইওটি সেন্সর", 
        "ask_label": "আপনার ফসল, সার বা মাটি সম্পর্কে জিজ্ঞাসা করুন:", "get_advice": "বিশেষজ্ঞের পরামর্শ নিন", 
        "weather": "☁️ আবহাওয়া পূর্বাভাস", "mandi": "📈 মণ্ডির দর", "leaf": "🍃 পাতার রোগ", 
        "ocr": "📄 ব্যাগ ওসিআর", "state_label": "রাজ্য নির্বাচন করুন:", "city_label": "শহর নির্বাচন করুন:", 
        "crop_label": "ফসল নির্বাচন করুন", "extract_btn": "তথ্য বের করুন", "translate_btn": "অনুবাদ করুন", 
        "temp": "তাপমাত্রা", "condition": "অবস্থা", "rain_warn": "⚠️ বৃষ্টি হতে পারে! ফসল রক্ষা করুন।", 
        "status": "বাজারের অবস্থা", "id_btn": "রোগ চিহ্নিত করুন", "file_label": "📄 ফসলের নথি বা ছবি আপলোড করুন:", 
        "unit_label": "একক নির্বাচন করুন:", "soil_moisture": "মাটির আর্দ্রতা", "simulate_btn": "ইএসপি ডেটা সিমুলেট করুন"
    },
    "Marathi (मराठी)": {
        "title": "🌾 किसान सेतू", "advisor": "🤖 एआय सल्लागार", "market": "📊 बाजार आणि हवामान", 
        "diagnostics": "🔍 पीक निदान", "tools": "🛠️ साधने", "iot": "📡 आयओटी सेन्सर", 
        "ask_label": "तुमच्या पिकाबद्दल विचार करा:", "get_advice": "तज्ञांचा सल्ला घ्या", 
        "weather": "☁️ हवामान अंदाज", "mandi": "📈 बाजारभाव", "leaf": "🍃 पानावरील रोग", 
        "ocr": "📄 बॅग ओसीआर", "state_label": "राज्य निवडा:", "city_label": "शहर निवडा:", 
        "crop_label": "पीक निवडा", "extract_btn": "माहिती काढा", "translate_btn": "भाषांतर करा", 
        "temp": "तापमान", "condition": "स्थिती", "rain_warn": "⚠️ पाऊस पडण्याची शक्यता!", 
        "status": "बाजार स्थिती", "id_btn": "रोग ओळखा", "file_label": "📄 कागदपत्र किंवा प्रतिमा अपलोड करा:", 
        "unit_label": "युनिट निवडा:", "soil_moisture": "मातीतील ओलावा", "simulate_btn": "डेटा सिम्युलेट करा"
    },
    "Telugu (తెలుగు)": {
        "title": "🌾 కిసాన్ సేతు", "advisor": "🤖 AI సలహాదారు", "market": "📊 మార్కెట్ & వాతావరణం", 
        "diagnostics": "🔍 పంట నిర్ధారణ", "tools": "🛠️ ఉపకరణాలు", "iot": "📡 IoT సెన్సార్", 
        "ask_label": "మీ పంట గురించి అడగండి:", "get_advice": "నిపుణుల సలహా తీసుకోండి", 
        "weather": "☁️ వాతావరణ సూచన", "mandi": "📈 మండి ధరలు", "leaf": "🍃 ఆకు వ్యాధి", 
        "ocr": "📄 బ్యాగ్ OCR", "state_label": "రాష్ట్రం ఎంచుకోండి:", "city_label": "నగరాన్ని ఎంచుకోండి:", 
        "crop_label": "పంటను ఎంచుకోండి", "extract_btn": "సమాచారాన్ని సేకరించండి", "translate_btn": "అనువదించండి", 
        "temp": "ఉష్ణోగ్రత", "condition": "పరిస్థితి", "rain_warn": "⚠️ వర్షం పడే అవకాశం ఉంది!", 
        "status": "మార్కెట్ స్థితి", "id_btn": "వ్యాధిని గుర్తించండి", "file_label": "📄 చిత్రాన్ని అప్‌లోడ్ చేయండి:", 
        "unit_label": "యూనిట్ ఎంచుకోండి:", "soil_moisture": "నేల తేమ", "simulate_btn": "డేటాను అనుకరించండి"
    },
    "Tamil (தமிழ்)": {
        "title": "🌾 கிசான் சேது", "advisor": "🤖 AI ஆலோசகர்", "market": "📊 சந்தை & வானிலை", 
        "diagnostics": "🔍 பயிர் கண்டறிதல்", "tools": "🛠️ கருவிகள்", "iot": "📡 IoT சென்சார்", 
        "ask_label": "உங்கள் பயிர் பற்றி கேளுங்கள்:", "get_advice": "நிபுணர் ஆலோசனை பெறவும்", 
        "weather": "☁️ வானிலை முன்னறிவிப்பு", "mandi": "📈 சந்தை விலைகள்", "leaf": "🍃 இலை நோய்", 
        "ocr": "📄 பையை ஸ்கேன் செய்", "state_label": "மாநிலம்:", "city_label": "நகரம்:", 
        "crop_label": "பயிர்", "extract_btn": "தகவலை எடு", "translate_btn": "மொழிபெயர்", 
        "temp": "வெப்பநிலை", "condition": "நிலை", "rain_warn": "⚠️ மழை எதிர்பார்க்கப்படுகிறது!", 
        "status": "சந்தை நிலை", "id_btn": "நோயை அடையாளம் காணவும்", "file_label": "📄 பதிவேற்றவும்:", 
        "unit_label": "அலகு:", "soil_moisture": "மண் ஈரப்பதம்", "simulate_btn": "உருவகப்படுத்து"
    },
    "Gujarati (ગુજરાતી)": {
        "title": "🌾 કિસાન સેતુ", "advisor": "🤖 AI સલાહકાર", "market": "📊 બજાર અને હવામાન", 
        "diagnostics": "🔍 પાક નિદાન", "tools": "🛠️ સાધનો", "iot": "📡 IoT સેન્સર", 
        "ask_label": "તમારા પાક વિશે પૂછો:", "get_advice": "નિષ્ણાતની સલાહ લો", 
        "weather": "☁️ હવામાનની આગાહી", "mandi": "📈 બજાર ભાવ", "leaf": "🍃 પાંદડાનો રોગ", 
        "ocr": "📄 બેગ OCR", "state_label": "રાજ્ય પસંદ કરો:", "city_label": "શહેર પસંદ કરો:", 
        "crop_label": "પાક પસંદ કરો", "extract_btn": "માહિતી મેળવો", "translate_btn": "અનુવાદ કરો", 
        "temp": "તાપમાન", "condition": "સ્થિતિ", "rain_warn": "⚠️ વરસાદની શક્યતા!", 
        "status": "બજાર સ્થિતિ", "id_btn": "રોગ ઓળખો", "file_label": "📄 દસ્તાવેજ અપલોડ કરો:", 
        "unit_label": "એકમ પસંદ કરો:", "soil_moisture": "માટીની ભેજ", "simulate_btn": "સિમ્યુલેટ કરો"
    },
    "Punjabi (ਪੰਜਾਬੀ)": {
        "title": "🌾 ਕਿਸਾਨ ਸੇਤੂ", "advisor": "🤖 ਏਆਈ ਸਲਾਹਕਾਰ", "market": "📊 ਬਾਜ਼ਾਰ ਅਤੇ ਮੌਸਮ", 
        "diagnostics": "🔍 ਫਸਲ ਨਿਦਾਨ", "tools": "🛠️ ਸੰਦ", "iot": "📡 IoT ਸੈਂਸਰ", 
        "ask_label": "ਆਪਣੀ ਫਸਲ ਬਾਰੇ ਪੁੱਛੋ:", "get_advice": "ਮਾਹਰ ਸਲਾਹ ਲਓ", 
        "weather": "☁️ ਮੌਸਮ ਦੀ ਭਵਿੱਖਬਾਣੀ", "mandi": "📈 ਮੰਡੀ ਦੇ ਭਾਅ", "leaf": "🍃 ਪੱਤੇ ਦੇ ਰੋਗ", 
        "ocr": "📄 ਬੈਗ ਓਸੀਆਰ", "state_label": "ਸੂਬਾ ਚੁਣੋ:", "city_label": "ਸ਼ਹਿਰ ਚੁਣੋ:", 
        "crop_label": "ਫਸਲ ਚੁਣੋ", "extract_btn": "ਜਾਣਕਾਰੀ ਕੱਢੋ", "translate_btn": "ਅਨੁਵਾਦ ਕਰੋ", 
        "temp": "ਤਾਪਮਾਨ", "condition": "ਹਾਲਤ", "rain_warn": "⚠️ ਮੀਂਹ ਦੀ ਉਮੀਦ!", 
        "status": "ਬਾਜ਼ਾਰ ਦੀ ਸਥਿਤੀ", "id_btn": "ਬਿਮਾਰੀ ਦੀ ਪਛਾਣ ਕਰੋ", "file_label": "📄 ਅਪਲੋਡ ਕਰੋ:", 
        "unit_label": "ਯੂਨਿਟ ਚੁਣੋ:", "soil_moisture": "ਮਿੱਟੀ ਦੀ ਨमी", "simulate_btn": "ਸਿਮੂਲੇਟ ਕਰੋ"
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
 user_query = st.text_input(t["ask_label"], placeholder="e.g. Best fertilizer for wheat")

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
  st.info(f"Status: {mandi_data['status']}")

# --- Tab 3: Crop Diagnostics ---
with tabs[2]:
 st.subheader(t["diagnostics"])
 diag_tab1, diag_tab2 = st.tabs([t["leaf"], t["ocr"]])
 with diag_tab1:
  leaf_img = st.file_uploader("Upload leaf image...", type=["jpg", "png"], key="leaf")
  if leaf_img and st.button(t["id_btn"]):
   with st.spinner("Analyzing leaf..."):
    model = genai.GenerativeModel(model_to_use)
    response = model.generate_content([f"Identify any plant disease in this leaf and recommend treatment in {language}.", Image.open(leaf_img)])
    st.info(response.text)
 with diag_tab2:
  bag_img = st.file_uploader("Upload bag image...", type=["jpg", "png"], key="bag")
  if bag_img and st.button(t["extract_btn"]):
   with st.spinner("Reading text..."):
    model = genai.GenerativeModel(model_to_use)
    response = model.generate_content([f"Extract and summarize all fertilizer/product details from this image in {language}.", Image.open(bag_img)])
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
