import streamlit as st
import json
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="KisanSetu - AI Agriculture", page_icon="🌾", layout="centered")

genai.configure(api_key="AQ.Ab8RN6KFRLjANXg_wcXie-WdxgBIWRXXp_FT7bGXyPJQuYoIcQ")

@st.cache_resource
def get_model():
    return genai.GenerativeModel("gemini-1.5-flash")

model = get_model()

# --- Localized States & Cities ---
LOCATIONS = {
    "English": {
        "Uttar Pradesh": ["Varanasi", "Lucknow", "Kanpur"],
        "Bihar": ["Patna", "Gaya"]
    },
    "Hindi (हिंदी)": {
        "उत्तर प्रदेश": ["वाराणसी", "लखनऊ", "कानपुर"],
        "बिहार": ["पटना", "गया"]
    }
}

UI = {
    "English": {"title": "🌾 KisanSetu (Smart Agriculture)", "ask": "Ask about your crop or soil:", "btn": "Get AI Advice", "mandi": "📊 Market Prices", "iot": "📡 IoT Hub", "sim": "Simulate Sensor Data"},
    "Hindi (हिंदी)": {"title": "🌾 किसान सेतु (स्मार्ट कृषि)", "ask": "अपनी फसल या मिट्टी के बारे में पूछें:", "btn": "एआई सलाह लें", "mandi": "📊 बाजार भाव", "iot": "📡 आईओटी हब", "sim": "सेंसर डेटा सिमुलेट करें"}
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329117.png", width=80)
    st.title("KisanSetu")
    lang = st.selectbox("Language / भाषा", list(UI.keys()))
    t = UI[lang]
    st.divider()
    
    states = list(LOCATIONS[lang].keys())
    sel_state = st.selectbox("State /
    
