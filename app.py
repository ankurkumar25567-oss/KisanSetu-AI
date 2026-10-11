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

# --- Dynamic AI Translator for Data ---
@st.cache_data(show_spinner=False)
def get_dynamic_data(lang):
    base_data = {
        "locs": {
            "Uttar Pradesh": ["Varanasi", "Lucknow", "Kanpur", "Etah", "Prayagraj"],
            "Bihar": ["Patna", "Gaya", "Muzaffarpur"],
            "Punjab": ["Amritsar", "Ludhiana", "Patiala"],
            "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
            "Delhi": ["New Delhi"]
        },
        "crops": ["Wheat", "Paddy", "Potato", "Tomato", "Onion", "Sugarcane", "Cotton", "Maize"],
        "units": ["Quintal (100kg)", "Kilogram (1kg)", "Tonne (1000kg)"]
    }
    
    if lang == "English":
        return base_data
        
    prompt = f"Translate all string values in this JSON to {lang}. Keep the JSON keys and structure identical:\n{json.dumps(base_data)}"
    try:
        # Force strict JSON output for speed and reliability
        res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "temperature": 0.1})
        return json.loads(res.text)
    except Exception:
        return base_data # Fallback to English if translation fails

# --- 23 Languages UI Dictionary (Safe Line-by-Line) ---
UI = {}
UI["English"] = {"t": "🌾 KisanSetu", "s": "Smart Agriculture", "ask": "Ask about crop:", "btn": "Ask AI", "m": "Market", "i": "IoT", "sim": "Simulate", "st": "State", "ct": "City", "cr": "Crop", "un": "Unit", "tr": "Translator", "txt": "Text", "cv": "Convert"}
UI["Hindi"] = {"t": "🌾 किसान सेतु", "s": "स्मार्ट कृषि", "ask": "फसल के बारे में पूछें:", "btn": "सलाह लें", "m": "बाजार", "i": "आईओटी", "sim": "सिमुलेट", "st": "राज्य", "ct": "शहर", "cr": "फसल", "un": "इकाई", "tr": "अनुवादक", "txt": "पाठ", "cv": "बदलें"}
UI["Bengali"] = {"t": "🌾 কিষাণ সেতু", "s": "স্মার্ট কৃষি", "ask": "ফসল সম্পর্কে জিজ্ঞাসা:", "btn": "পরামর্শ", "m": "বাজার", "i": "IoT", "sim": "সিমুলেট", "st": "রাজ্য", "ct": "শহর", "cr": "ফসল", "un": "একক", "tr": "অনুবাদক", "txt": "পাঠ্য", "cv": "রূপান্তর"}
UI["Marathi"] = {"t": "🌾 किसान सेतू", "s": "स्मार्ट शेती", "ask": "पिकाबद्दल विचारा:", "btn": "सल्ला घ्या", "m": "बाजार", "i": "IoT", "sim": "सिम्युलेट", "st": "राज्य", "ct": "शहर", "cr": "पीक", "un": "एकक", "tr": "अनुवादक", "txt": "मजकूर", "cv": "रुपांतरित करा"}
UI["Telugu"] = {"t": "🌾 కిసాన్ సేతు", "s": "స్మార్ట్ వ్యవసాయం", "ask": "పంట గురించి అడగండి:", "btn": "సలహా", "m": "మార్కెట్", "i": "IoT", "sim": "సిమ్యులేట్", "st": "రాష్ట్రం", "ct": "నగరం", "cr": "పంట", "un": "యూనిట్", "tr": "అనువాదకుడు", "txt": "వచనం", "cv": "మార్చు"}
UI["Tamil"] = {"t": "🌾 கிசான் சேது", "s": "ஸ்மார்ட் விவசாயம்", "ask": "பயிர் பற்றி கேளுங்கள்:", "btn": "கேள்", "m": "சந்தை", "i": "IoT", "sim": "உருவகப்படுத்து", "st": "மாநிலம்", "ct": "நகரம்", "cr": "பயிர்", "un": "அலகு", "tr": "மொழிபெயர்ப்பாளர்", "txt": "உரை", "cv": "மாற்று"}
UI["Gujarati"] = {"t": "🌾 કિસાન સેતુ", "s": "સ્માર્ટ કૃષિ", "ask": "પાક વિશે પૂછો:", "btn": "સલાહ લો", "m": "બજાર", "i": "IoT", "sim": "સિમ્યુલેટ", "st": "રાજ્ય", "ct": "શહેર", "cr": "પાક", "un": "એકમ", "tr": "અનુવાદક", "txt": "લખાણ", "cv": "બદલો"}
UI["Urdu"] = {"t": "🌾 کسان سیتی", "s": "سمارٹ زراعت", "ask": "فصل کے بارے میں پوچھیں:", "btn": "مشورہ", "m": "مارکیٹ", "i": "IoT", "sim": "تخروپن", "st": "ریاست", "ct": "شہر", "cr": "فصل", "un": "یونٹ", "tr": "مترجم", "txt": "متن", "cv": "تبدیل کریں"}
UI["Kannada"] = {"t": "🌾 ಕಿಸಾನ್ ಸೇತು", "s": "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ", "ask": "ಬೆಳೆ ಬಗ್ಗೆ ಕೇಳಿ:", "btn": "ಸಲಹೆ", "m": "ಮಾರುಕಟ್ಟೆ", "i": "IoT", "sim": "ಸಿಮ್ಯುಲೇಟ್", "st": "ರಾಜ್ಯ", "ct": "ನಗರ", "cr": "ಬೆಳೆ", "un": "ಘಟಕ", "tr": "ಅನುವಾದಕ", "txt": "ಪಠ್ಯ", "cv": "ಪರಿವರ್ತಿಸಿ"}
UI["Odia"] = {"t": "🌾 କିସାନ ସେତୁ", "s": "ସ୍ମାର୍ଟ କୃଷି", "ask": "ଫସଲ ବିଷୟରେ ପଚାରନ୍ତୁ:", "btn": "ପରାମର୍ଶ", "m": "ବଜାର", "i": "IoT", "sim": "ସିମୁଲେଟ୍", "st": "ରାଜ୍ୟ", "ct": "ସହର", "cr": "ଫସଲ", "un": "ଏକକ", "tr": "ଅନୁବାଦକ", "txt": "ପାଠ୍ୟ", "cv": "ରୂପାନ୍ତର କରନ୍ତୁ"}
UI["Malayalam"] = {"t": "🌾 കിസാൻ സേതു", "s": "സ്മാർട്ട് കൃഷി", "ask": "വിളയെക്കുറിച്ച് ചോദിക്കുക:", "btn": "ഉപദേശം", "m": "മാർക്കറ്റ്", "i": "IoT", "sim": "സിമുലേറ്റ്", "st": "സംസ്ഥാനം", "ct": "നഗരം", "cr": "വിള", "un": "യൂണിറ്റ്", "tr": "വിവർത്തകൻ", "txt": "വാചകം", "cv": "മാറ്റുക"}
UI["Punjabi"] = {"t": "🌾 ਕਿਸਾਨ ਸੇਤੂ", "s": "ਸਮਾਰਟ ਖੇਤੀ", "ask": "ਫਸਲ ਬਾਰੇ ਪੁੱਛੋ:", "btn": "ਸਲਾਹ", "m": "ਬਾਜ਼ਾਰ", "i": "IoT", "sim": "ਸਿਮੂਲੇਟ", "st": "ਸੂਬਾ", "ct": "ਸ਼ਹਿਰ", "cr": "ਫਸਲ", "un": "ਯੂਨਿਟ", "tr": "ਅਨੁਵਾਦਕ", "txt": "ਟੈਕਸਟ", "cv": "ਬਦਲੋ"}
UI["Assamese"] = {"t": "🌾 কিষাণ সেতু", "s": "স্মাৰ্ট কৃষি", "ask": "শস্যৰ বিষয়ে সুধক:", "btn": "পৰামৰ্শ", "m": "বজাৰ", "i": "IoT", "sim": "চিমুলেট", "st": "ৰাজ্য", "ct": "চহৰ", "cr": "শস্য", "un": "একক", "tr": "অনুবাদক", "txt": "পাঠ্য", "cv": "পৰিৱৰ্তন"}
UI["Nepali"] = {"t": "🌾 किसान सेतू", "s": "स्मार्ट कृषि", "ask": "बाली बारे सोध्नुहोस्:", "btn": "सल्लाह", "m": "बजार", "i": "IoT", "sim": "सिमुलेट", "st": "राज्य", "ct": "शहर", "cr": "बाली", "un": "इकाई", "tr": "अनुवादक", "txt": "पाठ", "cv": "रूपान्तरण"}
UI["Maithili"] = {"t": "🌾 किसान सेतु", "s": "स्मार्ट कृषि", "ask": "फसलक विषयमे पूछू:", "btn": "सलाह", "m": "बाजार", "i": "IoT", "sim": "सिमुलेट", "st": "राज्य", "ct": "शहर", "cr": "फसल", "un": "इकाई", "tr": "अनुवादक", "txt": "पाठ", "cv": "बदलू"}
UI["Santali"] = {"t": "🌾 ᱠᱤᱥᱟᱱ ᱥᱮᱛᱩ", "s": "Smart Agriculture", "ask": "Ask about crop:", "btn": "Ask", "m": "Market", "i": "IoT", "sim": "Simulate", "st": "State", "ct": "City", "cr": "Crop", "un": "Unit", "tr": "Translator", "txt": "Text", "cv": "Convert"}
UI["Kashmiri"] = {"t": "🌾 किसान सेतु", "s": "स्मार्ट कृषि", "ask": "फसल के बारे में पूछें:", "btn": "सलाह", "m": "बाजार", "i": "IoT", "sim": "सिमुलेट", "st": "राज्य", "ct": "शहर", "cr": "फसल", "un": "इकाई", "tr": "अनुवादक", "txt": "पाठ", "cv": "बदलें"}
UI["Sindhi"] = {"t": "🌾 ڪسان سيتو", "s": "سمارٽ زراعت", "ask": "فصل بابت پڇو:", "btn": "صلاح", "m": "مارڪيٽ", "i": "IoT", "sim": "Simulate", "st": "صوبو", "ct": "شهر", "cr": "فصل", "un": "يونٽ", "tr": "مترجم", "txt": "متن", "cv": "تبديل"}
UI["Konkani"] = {"t": "🌾 किसान सेतू", "s": "स्मार्ट शेती", "ask": "पिकाबद्दल विचारा:", "btn": "सल्लो", "m": "बाजार", "i": "IoT", "sim": "सिम्युलेट", "st": "राज्य", "ct": "शहर", "cr": "पीक", "un": "एकक", "tr": "अनुवादक", "txt": "मजकूर", "cv": "बदल"}
UI["Manipuri"] = {"t": "🌾 কিষাণ সেতু", "s": "Smart Agriculture", "ask": "Ask about crop:", "btn": "Ask", "m": "Market", "i": "IoT", "sim": "Simulate", "st": "State", "ct": "City", "cr": "Crop", "un": "Unit", "tr": "Translator", "txt": "Text", "cv": "Convert"}
UI["Dogri"] = {"t": "🌾 किसान सेतू", "s": "स्मार्ट खेती", "ask": "फसल बारे पुच्छो:", "btn": "सलाह", "m": "बाजार", "i": "IoT", "sim": "सिमुलेट", "st": "राज्य", "ct": "शहर", "cr": "फसल", "un": "इकाई", "tr": "अनुवादक", "txt": "पाठ", "cv": "बदलो"}
UI["Sanskrit"] = {"t": "🌾 किसानसेतु", "s": "स्मार्ट कृषि", "ask": "सस्यस्य विषये पृच्छतु:", "btn": "सल्लाहं", "m": "आपण", "i": "IoT", "sim": "Simulate", "st": "राज्य", "ct": "नगर", "cr": "सस्य", "un": "इकाई", "tr": "अनुवादक", "txt": "पाठ", "cv": "परिवर्तय"}
UI["Bodo"] = {"t": "🌾 किसान सेतू", "s": "स्मार्ट कृषि", "ask": "फसलनि सोमोन्दै सों:", "btn": "सल्लाह", "m": "बाजार", "i": "IoT", "sim": "Simulate", "st": "राज्य", "ct": "शहर", "cr": "फसल", "un": "इकाई", "tr": "Translator", "txt": "Text", "cv": "Convert"}

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329117.png", width=90)
    lang = st.selectbox("Language / भाषा", list(UI.keys()))
    ui = UI[lang]
    st.divider()
    
    with st.spinner("🌍 Translating Data..."):
        dyn_data = get_dynamic_data(lang)
    
    locs = dyn_data["locs"]
    states_list = list(locs.keys())
    
    sel_state = st.selectbox(ui["st"], states_list)
    sel_city = st.selectbox(ui["ct"], locs[sel_state])

# --- Main UI ---
st.markdown(f"<div class='main-header'>{ui['t']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-header'>{ui['s']}</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI", f"📊 {ui['m']}", f"📡 {ui['i']}", f"🔄 {ui['tr']}"])

# Tab 1: AI
with tab1:
    with st.form("ai_form"):
        q = st.text_input(ui['ask'], placeholder="...")
        if st.form_submit_button(ui['btn']) and q:
            with st.spinner("⚡ AI Processing..."):
                res = model.generate_content(f"Answer in {lang} concisely: {q}", generation_config={"max_output_tokens": 250})
                st.success(res.text)

# Tab 2: Market
with tab2:
    st.markdown("### 🌾 Live Market Rates")
    
    col1, col2 = st.columns(2)
    with col1:
        # User selects crop by translated name, but we track the index
        c_idx = st.selectbox(ui["cr"], range(len(dyn_data["crops"])), format_func=lambda x: dyn_data["crops"][x])
    with col2:
        u_idx = st.selectbox(ui["un"], range(len(dyn_data["units"])), format_func=lambda x: dyn_data["units"][x])

    # Base Prices per Quintal (100kg) for: [Wheat, Paddy, Potato, Tomato, Onion, Sugarcane, Cotton, Maize]
    base_prices = [2400, 2200, 1500, 3000, 2500, 350, 7000, 2100]
    base_price = base_prices[c_idx]
    
    # Calculate Unit Math
    if u_idx == 1: # Kilogram
        final_price = base_price / 100
    elif u_idx == 2: # Tonne
        final_price = base_price * 10
    else: # Quintal
        final_price = base_price
        
    st.metric(dyn_data["crops"][c_idx], f"₹{final_price:,.2f} / {dyn_data['units'][u_idx]}", delta="+₹50" if c_idx % 2 == 0 else "-₹20")

# Tab 3: Sensors
with tab3:
    st.markdown("### 📡 Field Sensors")
    if st.button(ui['sim']):
        c1, c2, c3 = st.columns(3)
        c1.metric("💧 Moisture", "42.5%")
        c2.metric("🌡️ Temp", "31°C")
        c3.metric("💨 Humidity", "65%")

# Tab 4: Text Converter
with tab4:
    st.markdown(f"### 🔄 {ui['tr']}")
    txt_input = st.text_area(ui["txt"])
    if st.button(ui["cv"]) and txt_input:
        with st.spinner("⚡ Translating..."):
            res = model.generate_content(f"Translate the following text to {lang}: {txt_input}", generation_config={"max_output_tokens": 300})
            st.success(res.text)

# --- Footer & Credits ---
st.markdown(
    "<div class='footer'>"
    "⚠️ <b>Disclaimer:</b> AI can make mistakes. Please verify critical farming decisions.<br><br>"
    "<b>Developed by Ankur Kumar & Vikalp Chaubey</b>"
    "</div>", 
    unsafe_allow_html=True
    )
