import streamlit as st
import google.generativeai as genai
import json

# --- Page Config ---
st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="centered")

# --- Custom Dark Mode CSS Theme ---
st.markdown("""
<style>
    .stApp { background-color: #121212; color: #ffffff; }
    .main-header { text-align: center; color: #4ade80; font-size: 2.8rem; font-weight: 800; padding-top: 10px; }
    .sub-header { text-align: center; color: #86efac; font-size: 1.2rem; margin-bottom: 25px; font-weight: 600; }
    .footer { text-align: center; font-size: 13px; color: #888888; padding: 15px; border-top: 1px solid #333333; margin-top: 40px; }
    div[data-testid="stForm"] { border-radius: 15px; border: 2px solid #166534; background-color: #1a1a1a; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    div[data-testid="stMetricValue"] { color: #4ade80 !important; }
    header[data-testid="stHeader"] { background-color: transparent !important; }
</style>
""", unsafe_allow_html=True)

# --- API Configuration ---
genai.configure(api_key="AQ.Ab8RN6KFRLjANXg_wcXie-WdxgBIWRXXp_FT7bGXyPJQuYoIcQ")

@st.cache_resource
def get_model():
    return genai.GenerativeModel("gemini-1.5-flash")

model = get_model()

# --- Dynamic AI Location Translator ---
@st.cache_data(show_spinner=False)
def get_localized_locations(lang):
    # Base English Locations (Includes your key cities)
    ENG_LOC = {
        "Andhra Pradesh": ["Visakhapatnam", "Vijayawada"],
        "Assam": ["Guwahati", "Silchar"],
        "Bihar": ["Patna", "Gaya"],
        "Delhi": ["New Delhi"],
        "Gujarat": ["Ahmedabad", "Surat"],
        "Karnataka": ["Bengaluru", "Mysuru"],
        "Kerala": ["Thiruvananthapuram", "Kochi"],
        "Madhya Pradesh": ["Bhopal", "Indore"],
        "Maharashtra": ["Mumbai", "Pune"],
        "Punjab": ["Amritsar", "Ludhiana"],
        "Rajasthan": ["Jaipur", "Jodhpur"],
        "Tamil Nadu": ["Chennai", "Coimbatore"],
        "Telangana": ["Hyderabad", "Warangal"],
        "Uttar Pradesh": ["Varanasi", "Lucknow", "Kanpur", "Prayagraj", "Etah"],
        "West Bengal": ["Kolkata", "Howrah"]
    }
    
    if lang == "English":
        return ENG_LOC
        
    try:
        # Instantly translates the dictionary into the selected language
        prompt = f"Translate the keys and values of this JSON dictionary into {lang}. Return strictly ONLY valid JSON. No markdown, no backticks:\n{json.dumps(ENG_LOC)}"
        res = model.generate_content(prompt, generation_config={"temperature": 0.1, "max_output_tokens": 1000})
        clean_json = res.text.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_json)
    except Exception:
        return ENG_LOC # Safe fallback to English if translation hiccups

# --- 23 Languages UI Dictionary (Safe Line-by-Line Format) ---
UI = {}
UI["English"] = {"title": "🌾 KisanSetu", "sub": "Smart Agriculture", "ask": "Ask about crop:", "btn": "Ask AI", "mandi": "Market", "iot": "IoT", "sim": "Simulate", "state": "State", "city": "City", "crop": "Crop"}
UI["Hindi"] = {"title": "🌾 किसान सेतु", "sub": "स्मार्ट कृषि", "ask": "फसल के बारे में पूछें:", "btn": "सलाह लें", "mandi": "बाजार", "iot": "आईओटी", "sim": "सिमुलेट", "state": "राज्य", "city": "शहर", "crop": "फसल"}
UI["Bengali"] = {"title": "🌾 কিষাণ সেতু", "sub": "স্মার্ট কৃষি", "ask": "ফসল সম্পর্কে জিজ্ঞাসা করুন:", "btn": "পরামর্শ নিন", "mandi": "বাজার", "iot": "IoT", "sim": "সিমুলেট", "state": "রাজ্য", "city": "শহর", "crop": "ফসল"}
UI["Marathi"] = {"title": "🌾 किसान सेतू", "sub": "स्मार्ट शेती", "ask": "पिकाबद्दल विचारा:", "btn": "सल्ला घ्या", "mandi": "बाजार", "iot": "IoT", "sim": "सिम्युलेट", "state": "राज्य", "city": "शहर", "crop": "पीक"}
UI["Telugu"] = {"title": "🌾 కిసాన్ సేతు", "sub": "స్మార్ట్ వ్యవసాయం", "ask": "పంట గురించి అడగండి:", "btn": "సలహా తీసుకోండి", "mandi": "మార్కెట్", "iot": "IoT", "sim": "అనుకరించండి", "state": "రాష్ట్రం", "city": "నగరం", "crop": "పంట"}
UI["Tamil"] = {"title": "🌾 கிசான் சேது", "sub": "ஸ்மார்ட் விவசாயம்", "ask": "பயிர் பற்றி கேளுங்கள்:", "btn": "ஆலோசனை பெறவும்", "mandi": "சந்தை", "iot": "IoT", "sim": "உருவகப்படுத்து", "state": "மாநிலம்", "city": "நகரம்", "crop": "பயிர்"}
UI["Gujarati"] = {"title": "🌾 કિસાન સેતુ", "sub": "સ્માર્ટ કૃષિ", "ask": "પાક વિશે પૂછો:", "btn": "સલાહ લો", "mandi": "બજાર", "iot": "IoT", "sim": "સિમ્યુલેટ કરો", "state": "રાજ્ય", "city": "શહેર", "crop": "પાક"}
UI["Urdu"] = {"title": "🌾 کسان سیتی", "sub": "سمارٹ زراعت", "ask": "فصل کے بارے میں پوچھیں:", "btn": "مشورہ لیں", "mandi": "مارکیٹ", "iot": "IoT", "sim": "تخروپن", "state": "ریاست", "city": "شہر", "crop": "فصل"}
UI["Kannada"] = {"title": "🌾 ಕಿಸಾನ್ ಸೇತು", "sub": "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ", "ask": "ಬೆಳೆ ಬಗ್ಗೆ ಕೇಳಿ:", "btn": "ಸಲಹೆ ಪಡೆಯಿರಿ", "mandi": "ಮಾರುಕಟ್ಟೆ", "iot": "IoT", "sim": "ಸಿಮ್ಯುಲೇಟ್", "state": "ರಾಜ್ಯ", "city": "ನಗರ", "crop": "ಬೆಳೆ"}
UI["Odia"] = {"title": "🌾 କିସାନ ସେତୁ", "sub": "ସ୍ମାର୍ଟ କୃଷି", "ask": "ଫସଲ ବିଷୟରେ ପଚାରନ୍ତୁ:", "btn": "ପରାମର୍ଶ ନିଅନ୍ତୁ", "mandi": "ବଜାର", "iot": "IoT", "sim": "ସିମୁଲେଟ୍", "state": "ରାଜ୍ୟ", "city": "ସହର", "crop": "ଫସଲ"}
UI["Malayalam"] = {"title": "🌾 കിസാൻ സേതു", "sub": "സ്മാർട്ട് കൃഷി", "ask": "വിളയെക്കുറിച്ച് ചോദിക്കുക:", "btn": "ഉപദേശം നേടുക", "mandi": "മാർക്കറ്റ്", "iot": "IoT", "sim": "സിമുലേറ്റ്", "state": "സംസ്ഥാനം", "city": "നഗരം", "crop": "വിള"}
UI["Punjabi"] = {"title": "🌾 ਕਿਸਾਨ ਸੇਤੂ", "sub": "ਸਮਾਰਟ ਖੇਤੀ", "ask": "ਫਸਲ ਬਾਰੇ ਪੁੱਛੋ:", "btn": "ਸਲਾਹ ਲਓ", "mandi": "ਬਾਜ਼ਾਰ", "iot": "IoT", "sim": "ਸਿਮੂਲੇਟ ਕਰੋ", "state": "ਸੂਬਾ", "city": "ਸ਼ਹਿਰ", "crop": "ਫਸਲ"}
UI["Assamese"] = {"title": "🌾 কিষাণ সেতু", "sub": "স্মাৰ্ট কৃষি", "ask": "শস্যৰ বিষয়ে সুধক:", "btn": "পৰামৰ্শ লওক", "mandi": "বজাৰ", "iot": "IoT", "sim": "চিমুলেট", "state": "ৰাজ্য", "city": "চহৰ", "crop": "শস্য"}
UI["Nepali"] = {"title": "🌾 किसान सेतू", "sub": "स्मार्ट कृषि", "ask": "बाली बारे सोध्नुहोस्:", "btn": "सल्लाह लिनुहोस्", "mandi": "बजार", "iot": "IoT", "sim": "सिमुलेट", "state": "राज्य", "city": "शहर", "crop": "बाली"}
UI["Maithili"] = {"title": "🌾 किसान सेतु", "sub": "स्मार्ट कृषि", "ask": "फसलक विषयमे पूछू:", "btn": "सलाह लिअ", "mandi": "बाजार", "iot": "IoT", "sim": "सिमुलेट", "state": "राज्य", "city": "शहर", "crop": "फसल"}
UI["Santali"] = {"title": "🌾 ᱠᱤᱥᱟᱱ ᱥᱮᱛᱩ", "sub": "Smart Agriculture", "ask": "Ask about crop:", "btn": "Ask AI", "mandi": "Market", "iot": "IoT", "sim": "Simulate", "state": "State", "city": "City", "crop": "Crop"}
UI["Kashmiri"] = {"title": "🌾 किसान सेतु", "sub": "स्मार्ट कृषि", "ask": "फसल के बारे में पूछें:", "btn": "सलाह लें", "mandi": "बाजार", "iot": "IoT", "sim": "सिमुलेट", "state": "राज्य", "city": "शहर", "crop": "फसल"}
UI["Sindhi"] = {"title": "🌾 ڪسان سيتو", "sub": "سمارٽ زراعت", "ask": "فصل بابت پڇو:", "btn": "صلاح وٺو", "mandi": "مارڪيٽ", "iot": "IoT", "sim": "Simulate", "state": "صوبو", "city": "شهر", "crop": "فصل"}
UI["Konkani"] = {"title": "🌾 किसान सेतू", "sub": "स्मार्ट शेती", "ask": "पिकाबद्दल विचारा:", "btn": "सल्लो घेयात", "mandi": "बाजार", "iot": "IoT", "sim": "सिम्युलेट", "state": "राज्य", "city": "शहर", "crop": "पीक"}
UI["Manipuri"] = {"title": "🌾 কিষাণ সেতু", "sub": "Smart Agriculture", "ask": "Ask about crop:", "btn": "Ask AI", "mandi": "Market", "iot": "IoT", "sim": "Simulate", "state": "State", "city": "City", "crop": "Crop"}
UI["Dogri"] = {"title": "🌾 किसान सेतू", "sub": "स्मार्ट खेती", "ask": "फसल बारे पुच्छो:", "btn": "सलाह लो", "mandi": "बाजार", "iot": "IoT", "sim": "सिमुलेट", "state": "राज्य", "city": "शहर", "crop": "फसल"}
UI["Sanskrit"] = {"title": "🌾 किसानसेतु", "sub": "स्मार्ट कृषि", "ask": "सस्यस्य विषये पृच्छतु:", "btn": "सल्लाहं प्राप्नुवन्तु", "mandi": "आपण", "iot": "IoT", "sim": "Simulate", "state": "राज्य", "city": "नगर", "crop": "सस्य"}
UI["Bodo"] = {"title": "🌾 किसान सेतू", "sub": "स्मार्ट कृषि", "ask": "फसलनि सोमोन्दै सों:", "btn": "सल्लाह ला", "mandi": "बाजार", "iot": "IoT", "sim": "Simulate", "state": "राज्य", "city": "शहर", "crop": "फसल"}

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329117.png", width=90)
    lang = st.selectbox("Language / भाषा", list(UI.keys()))
    t = UI[lang]
    st.divider()
    
    # Load dynamically translated locations
    with st.spinner("Translating locations..."):
        LOCATIONS = get_localized_locations(lang)
        
    states_list = list(LOCATIONS.keys())
    # Default to UP if it exists in the translated list
    default_state_index = 0
    for i, state_name in enumerate(states_list):
        if "Uttar Pradesh" in state_name or "उत्तर प्रदेश" in state_name:
            default_state_index = i
            break
            
    sel_state = st.selectbox(t["state"], states_list, index=default_state_index)
    sel_city = st.selectbox(t["city"], LOCATIONS[sel_state])

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
    crop = st.selectbox(t["crop"], ["Wheat", "Paddy", "Potato", "Tomato"])
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
    "<b>Developed by Ankur Kumar & Vikalp Chaubey</b>"
    "</div>", 
    unsafe_allow_html=True
)
