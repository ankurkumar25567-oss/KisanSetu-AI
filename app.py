import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="centered")

# --- Custom Attractive CSS Theme ---
st.markdown("""
<style>
    .stApp { background-color: #f7fcf7; }
    .main-header { text-align: center; color: #1b5e20; font-size: 2.8rem; font-weight: 800; padding-top: 10px; }
    .sub-header { text-align: center; color: #4caf50; font-size: 1.2rem; margin-bottom: 25px; font-weight: 600; }
    .footer { text-align: center; font-size: 13px; color: #666; padding: 15px; border-top: 1px solid #ddd; margin-top: 40px; }
    div[data-testid="stForm"] { border-radius: 15px; border: 2px solid #e8f5e9; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

# API Configuration
genai.configure(api_key="AQ.Ab8RN6KFRLjANXg_wcXie-WdxgBIWRXXp_FT7bGXyPJQuYoIcQ")

@st.cache_resource
def get_model():
    return genai.GenerativeModel("gemini-1.5-flash")

model = get_model()

# --- Language Data (Safe from line breaks) ---
LOCATIONS = {
    "English": {"Uttar Pradesh": ["Varanasi", "Lucknow", "Kanpur"], "Bihar": ["Patna", "Gaya"]},
    "Hindi": {"उत्तर प्रदेश": ["वाराणसी", "लखनऊ", "कानपुर"], "बिहार": ["पटना", "गया"]}
}

UI = {
    "English": {"title": "🌾 KisanSetu", "sub": "Smart AI Agriculture", "ask": "Ask about your crop or soil:", "btn": "Get AI Advice", "mandi": "📊 Market", "iot": "📡 IoT Hub", "sim": "Simulate Sensor Data", "state": "Select State", "city": "Select City", "crop": "Select Crop"},
    "Hindi": {"title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई कृषि", "ask": "अपनी फसल या मिट्टी के बारे में पूछें:", "btn": "एआई सलाह लें", "mandi": "📊 बाजार", "iot": "📡 आईओटी", "sim": "सेंसर डेटा सिमुलेट करें", "state": "राज्य चुनें", "city": "शहर चुनें", "crop": "फसल चुनें"}
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329117.png", width=90)
    lang = st.selectbox("Language / भाषा", ["English", "Hindi"])
    t = UI[lang]
    st.divider()
    
    states = list(LOCATIONS[lang].keys())
    sel_state = st.selectbox(t["state"], states)
    sel_city = st.selectbox(t["city"], LOCATIONS[lang][sel_state])

# --- Main UI ---
st.markdown(f"<div class='main-header'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-header'>{t['sub']}</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🤖 AI Advisor", t['mandi'], t['iot']])

# Tab 1: AI
with tab1:
    with st.form("ai_form"):
        q = st.text_input(t['ask'], placeholder="e.g. Best fertilizer for wheat...")
        if st.form_submit_button(t['btn']) and q:
            with st.spinner("⚡ Processing..."):
                res = model.generate_content(f"Answer in {lang} concisely: {q}", generation_config={"max_output_tokens": 200})
                st.success(res.text)

# Tab 2: Market
with tab2:
    st.markdown("### 🌾 Live Rates")
    crop = st.selectbox(t["crop"], ["Wheat / गेहूं", "Paddy / धान", "Potato / आलू", "Tomato / टमाटर"])
    st.metric(crop, "₹2,400 / Quintal", delta="+₹50 (Stable)")

# Tab 3: Sensors
with tab3:
    st.markdown("### 📡 Field Sensors")
    if st.button(t['sim']):
        c1, c2, c3 = st.columns(3)
        c1.metric("💧 Moisture", "42.5%")
        c2.metric("🌡️ Temp", "31°C")
        c3.metric("💨 Humidity", "65%")

# --- Footer & Credits ---
st.markdown(
    "<div class='footer'>"
    "⚠️ <b>Disclaimer:</b> AI can make mistakes. Please verify critical farming decisions.<br><br>"
    "<b>Developed by Ankur Kumar & Vikalp Chaubay</b>"
    "</div>", 
    unsafe_allow_html=True
)
