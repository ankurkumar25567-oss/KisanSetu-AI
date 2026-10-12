import streamlit as st
import urllib.request
import urllib.error
import json
import base64
from PIL import Image
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="KisanSetu - Smart Ag",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- 📱 DEVICE-ADAPTIVE CSS, ANTI-REFRESH & VECTOR SCROLLBAR 📱 ---
st.markdown("""
<style>
    /* 1. Stop Pull-to-Refresh FOREVER without breaking the layout */
    html, body, [data-testid="stAppViewContainer"], .main, .stApp {
        overscroll-behavior: none !important;
        overscroll-behavior-y: none !important;
        overscroll-behavior-x: none !important;
    }

    /* 2. CUSTOM VERTICAL SCROLLBAR (Vector Style) */
    ::-webkit-scrollbar {
        width: 20px !important;
    }
    ::-webkit-scrollbar-track {
        background: #1a1c23 !important;
        border-left: 1px solid #0f1117;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #3f3f46 !important;
        border-radius: 12px !important;
        border: 3px solid #1a1c23 !important;
        
        background-image: 
            linear-gradient(#ffffff, #ffffff),
            linear-gradient(#ffffff, #ffffff),
            linear-gradient(#ffffff, #ffffff) !important;
        background-size: 10px 2px, 10px 2px, 10px 2px !important;
        background-position: center calc(50% - 6px), center, center calc(50% + 6px) !important;
        background-repeat: no-repeat !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background-color: #52525b !important;
    }

    /* Global Dark Theme */
    .stApp { 
        background-color: #0f1117; 
        color: #f3f4f6; 
    }
    
    /* Device-Adaptive Responsive Container */
    .block-container {
        max-width: 980px !important;
        padding-top: 1rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    /* 3. FIX FOR THE CUT-OFF TEXT */
    .main-header { 
        text-align: center; 
        color: #4ade80; 
        font-size: clamp(2rem, 5vw, 3rem); 
        font-weight: 800; 
        margin-top: 50px !important;
        margin-bottom: 5px;
    }
    .sub-header { 
        text-align: center; 
        color: #86efac; 
        font-size: clamp(1rem, 2.5vw, 1.25rem); 
        margin-bottom: 25px; 
        font-weight: 600; 
    }
    
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .footer { 
        text-align: center; 
        font-size: 13px; 
        color: #9ca3af; 
        padding: 18px; 
        border-top: 1px solid #27272a; 
        margin-top: 35px; 
    }

    /* Touch & Click Friendly Buttons */
    .stButton>button {
        width: 100% !important;
        min-height: 3rem !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        border: 1px solid #16a34a !important;
        background-color: #15803d !important;
        color: #ffffff !important;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #16a34a !important;
        border-color: #4ade80 !important;
        color: #ffffff !important;
    }

    /* Device Card Metric Styling */
    div[data-testid="stMetric"] {
        background: #181a20 !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        border: 1px solid #27272a !important;
    }
    div[data-testid="stMetricValue"] { 
        color: #4ade80 !important; 
        font-size: clamp(1.2rem, 3vw, 1.8rem) !important;
    }

    /* Text Wrapping Fix */
    .stMarkdown, .stSuccess, .stError, .stInfo, p { 
        word-wrap: break-word !important; 
        overflow-wrap: break-word !important; 
        white-space: pre-wrap !important; 
    }

    /* Tutorial Box */
    .tutorial-box {
        background-color: #181a20;
        padding: 22px;
        border-radius: 14px;
        border: 2px solid #22c55e;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 🌐 20 LANGUAGES DICTIONARY & LOCALIZATION 🌐 ---
LANGUAGES = [
    "English", "Hindi (हिंदी)", "Punjabi (ਪੰਜਾਬੀ)", "Telugu (తెలుగు)",
    "Bengali (বাংলা)", "Marathi (मराठी)", "Tamil (தமிழ்)", "Gujarati (ગુજરાતી)",
    "Kannada (ಕನ್ನಡ)", "Malayalam (മലയാളം)", "Odia (ଓଡ଼ିଆ)", "Assamese (অসমীয়া)",
    "Urdu (اردو)", "Bhojpuri (भोजपुरी)", "Maithili (मैथिली)", "Nepali (नेपाली)",
    "Sanskrit (संस्कृतम्)", "Sindhi (सिंधी)", "Konkani (कोंकणी)", "Dogri (डोगरी)"
]

BASE_UI = {
    "title": "🌾 KisanSetu", "sub": "Smart AI Agriculture",
    "tab_ai": "🤖 AI Advisor", "tab_mandi": "📊 Market Rates", "tab_iot": "📡 Field Sensors", "tab_tr": "🔄 Translator",
    "tut_title": "Welcome to KisanSetu 🌾", "tut_sub": "Your Smart AI Agriculture Assistant",
    "tut_guide": "🚀 Quick Start Guide",
    "tut_1": "<b>1. 🤖 AI Advisor & Camera:</b> Ask farming queries or snap a leaf photo to diagnose diseases.",
    "tut_2": "<b>2. 📊 Market Rates:</b> Real-time Mandi price calculations tailored to your quantity and crop.",
    "tut_3": "<b>3. 📡 Field Sensors:</b> Live simulated IoT metrics for soil moisture and temperature.",
    "tut_4": "<b>4. 🛰️ Auto-Locate:</b> Click the GPS button in the sidebar to sync to your current region!",
    "tut_btn": "✅ Start Using KisanSetu",
    "ask_crop": "Ask your question here:", "cam_prompt": "📷 Take a live photo", "up_prompt": "📁 Or upload an image",
    "btn_ai": "Ask AI / Analyze Crop", "lbl_crop": "Select Crop:", "lbl_unit": "Select Unit:",
    "btn_sim": "Refresh Sensors", "lbl_state": "Select State:", "lbl_city": "Select City:",
    "gps_btn": "🛰️ Auto-Locate (GPS)", "soil": "💧 Soil Moisture", "temp": "🌡️ Temperature", "hum": "💨 Humidity",
    "tr_prompt": "Paste text to translate:", "btn_tr": "Translate",
    "dev": "<b>Developed by Ankur Kumar & Vikalp Chaubey</b><br>The Aryan International School, Varanasi"
}

TRANSLATIONS = {
    "Hindi (हिंदी)": {
        "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई कृषि",
        "tab_ai": "🤖 एआई सलाहकार", "tab_mandi": "📊 बाजार भाव", "tab_iot": "📡 खेत सेंसर", "tab_tr": "🔄 अनुवादक",
        "tut_title": "किसान सेतु में आपका स्वागत है 🌾", "tut_sub": "आपका स्मार्ट एआई कृषि सहायक",
        "tut_guide": "🚀 त्वरित आरंभ गाइड",
        "tut_1": "<b>1. 🤖 एआई सलाहकार:</b> खेती के प्रश्न पूछें या बीमारी का पता लगाने के लिए पत्ती की फोटो लें।",
        "tut_2": "<b>2. 📊 बाजार भाव:</b> आपकी फसल और मात्रा के अनुसार वास्तविक समय मंडी मूल्य।",
        "tut_3": "<b>3. 📡 खेत सेंसर:</b> मिट्टी की नमी और तापमान के लिए लाइव IoT मेट्रिक्स।",
        "tut_4": "<b>4. 🛰️ ऑटो-लोकेट:</b> अपने क्षेत्र से सिंक करने के लिए साइडबार में GPS बटन दबाएं!",
        "tut_btn": "✅ किसान सेतु शुरू करें",
        "ask_crop": "अपना प्रश्न यहाँ पूछें:", "cam_prompt": "📷 लाइव फोटो लें", "up_prompt": "📁 या छवि अपलोड करें",
        "btn_ai": "एआई से पूछें / फसल का विश्लेषण करें", "lbl_crop": "फसल चुनें:", "lbl_unit": "इकाई चुनें:",
        "btn_sim": "सेंसर रीफ्रेश करें", "lbl_state": "राज्य चुनें:", "lbl_city": "शहर चुनें:",
        "gps_btn": "🛰️ ऑटो-लोकेट (GPS)", "soil": "💧 मिट्टी की नमी", "temp": "🌡️ तापमान", "hum": "💨 आर्द्रता",
        "tr_prompt": "अनुवाद करने के लिए टेक्स्ट पेस्ट करें:", "btn_tr": "अनुवाद करें",
        "dev": "<b>अंकुर कुमार और विकल्प चौबे द्वारा विकसित</b><br>द आर्यन इंटरनेशनल स्कूल, वाराणसी"
    },
    "Punjabi (ਪੰਜਾਬੀ)": {
        "title": "🌾 ਕਿਸਾਨ ਸੇਤੂ", "sub": "ਸਮਾਰਟ ਏਆਈ ਖੇਤੀ",
        "tab_ai": "🤖 ਏਆਈ ਸਲਾਹਕਾਰ", "tab_mandi": "📊 ਬਾਜ਼ਾਰ ਦੇ ਭਾਅ", "tab_iot": "📡 ਖੇਤ ਸੈਂਸਰ", "tab_tr": "🔄 ਅਨੁਵਾਦਕ",
        "tut_title": "ਕਿਸਾਨ ਸੇਤੂ ਵਿੱਚ ਸਵਾਗਤ ਹੈ 🌾", "tut_sub": "ਤੁਹਾਡਾ ਸਮਾਰਟ ਏਆਈ ਖੇਤੀ ਸਹਾਇਕ",
        "tut_guide": "🚀 ਤੁਰੰਤ ਸ਼ੁਰੂਆਤ",
        "tut_btn": "✅ ਕਿਸਾਨ ਸੇਤੂ ਸ਼ੁਰੂ ਕਰੋ", "ask_crop": "ਆਪਣਾ ਸਵਾਲ ਇੱਥੇ ਪੁੱਛੋ:", "btn_ai": "ਏਆਈ ਨੂੰ ਪੁੱਛੋ / ਫਸਲ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ",
        "cam_prompt": "📷 ਲਾਈਵ ਫੋਟੋ ਲਓ", "up_prompt": "📁 ਜਾਂ ਚਿੱਤਰ ਅਪਲੋਡ ਕਰੋ", "lbl_crop": "ਫਸਲ ਚੁਣੋ:", "lbl_unit": "ਯੂਨਿਟ ਚੁਣੋ:",
        "btn_sim": "ਸੈਂਸਰ ਰਿਫ੍ਰੈਸ਼ ਕਰੋ", "lbl_state": "ਸੂਬਾ ਚੁਣੋ:", "lbl_city": "ਸ਼ਹਿਰ ਚੁਣੋ:",
        "gps_btn": "🛰️ ਆਟੋ-ਲੋਕੇਟ (GPS)", "soil": "💧 ਮਿੱਟੀ ਦੀ ਨਮੀ", "temp": "🌡️ ਤਾਪਮਾਨ", "hum": "💨 ਨਮੀ",
        "tr_prompt": "ਅਨੁਵਾਦ ਕਰਨ ਲਈ ਟੈਕਸਟ ਪੇਸਟ ਕਰੋ:", "btn_tr": "ਅਨੁਵਾਦ ਕਰੋ"
    },
    "Telugu (తెలుగు)": {
        "title": "🌾 కిసాన్ సేతు", "sub": "స్మార్ట్ AI వ్యవసాయం",
        "tab_ai": "🤖 AI సలహాదారు", "tab_mandi": "📊 మార్కెట్ ధరలు", "tab_iot": "📡 సెన్సార్లు", "tab_tr": "🔄 అనువాదకుడు",
        "tut_title": "కిసాన్ సేతుకు స్వాగతం 🌾", "tut_sub": "మీ స్మార్ట్ AI వ్యవసాయ సహాయకుడు",
        "tut_guide": "🚀 శీఘ్ర ప్రారంభం",
        "tut_btn": "✅ కిసాన్ సేతు ప్రారంభించండి", "ask_crop": "మీ ప్రశ్నను ఇక్కడ అడగండి:", "btn_ai": "AI ని అడగండి / పంటను విశ్లేషించండి",
        "cam_prompt": "📷 లైవ్ ఫోటో తీయండి", "up_prompt": "📁 లేదా చిత్రాన్ని అప్‌లోడ్ చేయండి", "lbl_crop": "పంటను ఎంచుకోండి:", "lbl_unit": "యూనిట్ ఎంచుకోండి:",
        "btn_sim": "సెన్సార్లను రిఫ్రెష్ చేయండి", "lbl_state": "రాష్ట్రం ఎంచుకోండి:", "lbl_city": "నగరాన్ని ఎంచుకోండి:",
        "gps_btn": "🛰️ ఆటో-లొకేట్ (GPS)", "soil": "💧 నేల
