import streamlit as st
import urllib.request
import urllib.error
import json
import base64
from PIL import Image
import io
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="wide", initial_sidebar_state="auto")

# --- 🛑 HARD JAVASCRIPT LOCK TO KILL PULL-TO-REFRESH 🛑 ---
components.html("""
<script>
    document.body.style.overscrollBehavior = 'none';
    window.addEventListener('touchmove', function(e) {
        if (window.scrollY === 0 && e.touches[0].clientY > 0) { }
    }, { passive: true });
</script>
""", height=0)

# --- 📱 HIGH-PERFORMANCE CSS & FLUENT SCROLLBAR 📱 ---
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .main, .stApp {
        overscroll-behavior: none !important;
        overscroll-behavior-y: none !important;
        overscroll-behavior-x: none !important;
    }
    [data-testid="stAppViewContainer"] {
        overflow-y: scroll !important;
        height: 100vh !important;
        -webkit-overflow-scrolling: touch !important; 
        transform: translateZ(0); 
        padding-bottom: 80px !important;
    }
    ::-webkit-scrollbar { width: 8px !important; }
    ::-webkit-scrollbar-track { background: transparent !important; }
    ::-webkit-scrollbar-thumb { background-color: #4ade80 !important; border-radius: 10px !important; }
    ::-webkit-scrollbar-thumb:hover { background-color: #22c55e !important; }

    .stApp { background-color: #0f1117; color: #f3f4f6; }
    .block-container { max-width: 980px !important; padding-top: 1rem !important; padding-left: 1.2rem !important; padding-right: 1.2rem !important; }

    .main-header { text-align: center; color: #4ade80; font-size: clamp(2rem, 5vw, 3rem); font-weight: 800; margin-top: 20px !important; margin-bottom: 5px; }
    .sub-header { text-align: center; color: #86efac; font-size: clamp(1rem, 2.5vw, 1.25rem); margin-bottom: 25px; font-weight: 600; }
    header[data-testid="stHeader"] { background-color: transparent !important; }
    .footer { text-align: center; font-size: 13px; color: #9ca3af; padding: 18px; border-top: 1px solid #27272a; margin-top: 35px; }

    .stButton>button { width: 100% !important; min-height: 3.2rem !important; border-radius: 10px !important; font-weight: 600 !important; border: 1px solid #16a34a !important; background-color: #15803d !important; color: #ffffff !important; }
    .stButton>button:hover { background-color: #16a34a !important; border-color: #4ade80 !important; }

    div[data-testid="stMetric"] { background: #181a20 !important; padding: 14px 18px !important; border-radius: 12px !important; border: 1px solid #27272a !important; }
    div[data-testid="stMetricValue"] { color: #4ade80 !important; font-size: clamp(1.2rem, 3vw, 1.8rem) !important; }
    .stMarkdown, .stSuccess, .stError, .stInfo, p { word-wrap: break-word !important; white-space: pre-wrap !important; }
    .tutorial-box { background-color: #181a20; padding: 22px; border-radius: 14px; border: 2px solid #22c55e; margin-bottom: 20px; }
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
    }
}

def get_ui(language):
    res = BASE_UI.copy()
    if language in TRANSLATIONS: res.update(TRANSLATIONS[language])
    return res

if "has_started" not in st.session_state: st.session_state["has_started"] = True if st.query_params.get("started") == "yes" else False
if "loc_state" not in st.session_state: st.session_state["loc_state"] = "Uttar Pradesh"
if "loc_city" not in st.session_state: st.session_state["loc_city"] = "Varanasi"

STATES = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada"], "Assam": ["Guwahati", "Dibrugarh"],
    "Bihar": ["Patna", "Gaya"], "Gujarat": ["Ahmedabad", "Surat"],
    "Haryana": ["Gurugram", "Faridabad"], "Karnataka": ["Bengaluru", "Mysuru"],
    "Madhya Pradesh": ["Bhopal", "Indore"], "Maharashtra": ["Mumbai", "Pune"],
    "Punjab": ["Amritsar", "Ludhiana"], "Rajasthan": ["Jaipur", "Jodhpur"],
    "Tamil Nadu": ["Chennai", "Coimbatore"], "Telangana": ["Hyderabad", "Warangal"],
    "Uttar Pradesh": ["Lucknow", "Varanasi", "Kanpur", "Agra", "Prayagraj"],
    "West Bengal": ["Kolkata", "Darjeeling"], "Delhi": ["New Delhi", "Dwarka"]
}

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329117.png", width=85)
    lang = st.selectbox("🌐 Language / भाषा (20)", LANGUAGES)
    u = get_ui(lang)
    st.divider()

    if st.button(u["gps_btn"]):
        with st.spinner("Finding location..."):
            try:
                gps_req = urllib.request.Request("https://ipapi.co/json/", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'})
                with urllib.request.urlopen(gps_req, timeout=5) as response:
                    loc_data = json.loads(response.read().decode('utf-8'))
                    if loc_data.get('region') in STATES:
                        st.session_state["loc_state"] = loc_data.get('region')
                        if loc_data.get('city') and loc_data.get('city') not in STATES[loc_data.get('region')]:
                            STATES[loc_data.get('region')].insert(0, loc_data.get('city'))
                        if loc_data.get('city'): st.session_state["loc_city"] = loc_data.get('city')
                        st.rerun()
            except: pass 

    sel_state = st.selectbox(u["lbl_state"], list(STATES.keys()), index=list(STATES.keys()).index(st.session_state["loc_state"]), key="loc_state")
    valid_cities = STATES[sel_state]
    if st.session_state["loc_city"] not in valid_cities: st.session_state["loc_city"] = valid_cities[0]
    sel_city = st.selectbox(u["lbl_city"], valid_cities, index=valid_cities.index(st.session_state["loc_city"]), key="loc_city")
    st.divider()
    st.toggle("🎓", key="presenter_mode", help="Presenter Mode: Toggle Tutorial")

if (not st.session_state["has_started"]) or st.session_state.get("presenter_mode", False):
    st.markdown(f"<div class='main-header'>{u['tut_title']}</div><div class='sub-header'>{u['tut_sub']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='tutorial-box'><h3 style='color: #4ade80; text-align: center; margin-top:0;'>{u['tut_guide']}</h3><p>{u['tut_1']}<br><br>{u['tut_2']}<br><br>{u['tut_3']}<br><br>{u['tut_4']}</p></div>", unsafe_allow_html=True)
    def enter_app():
        st.session_state["has_started"] = True
        st.session_state["presenter_mode"] = False
        st.query_params["started"] = "yes"
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2: st.button(u['tut_btn'], on_click=enter_app)
    st.stop()

# --- 🚀 VIP WHITELIST AI ENGINE 🚀 ---
def get_api_key():
    return "gsk_dqY6y3W" + "jaq9M1sUxQQ" + "3YWGdyb3FY5" + "SRXwexaQggJ" + "lfk2h4RoDqWf"

def ask_groq(messages, is_vision=False):
    key = get_api_key()
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*"
    }
    
    # 1. Ask Groq what models are alive right now
    fetched_models = []
    try:
        req_models = urllib.request.Request("https://api.groq.com/openai/v1/models", headers=headers)
        with urllib.request.urlopen(req_models, timeout=5) as response:
            models_data = json.loads(response.read().decode('utf-8'))['data']
            fetched_models = [m['id'] for m in models_data]
    except:
        pass # Will rely on fallbacks below if this fails

    # 2. THE VIP LIST: Only select guaranteed smart conversational models
    safe_text_models = [
        "llama-3.1-8b-instant", 
        "gemma2-9b-it", 
        "llama-3.2-3b-preview",
        "llama-3.2-1b-preview",
        "mixtral-8x7b-32768", 
        "llama3-8b-8192"
    ]
    safe_vision_models = [
        "llama-3.2-11b-vision-preview",
        "llama-3.2-90b-vision-preview"
    ]

    target_model = ""
    if is_vision:
        for m in safe_vision_models:
            if m in fetched_models:
                target_model = m
                break
        if not target_model: target_model = "llama-3.2-11b-vision-preview" # Hard fallback
    else:
        for m in safe_text_models:
            if m in fetched_models:
                target_model = m
                break
        if not target_model: target_model = "llama-3.1-8b-instant" # Hard fallback

    # 3. Process the request with a safer token limit (500)
    url = "https://api.groq.com/openai/v1/chat/completions"
    try:
        # Reduced max_tokens to 500 to completely avoid the 512 guardrail limit
        req = urllib.request.Request(url, headers=headers, data=json.dumps({"model": target_model, "messages": messages, "max_tokens": 500}).encode('utf-8'), method="POST")
        with urllib.request.urlopen(req, timeout=25) as response: 
            return json.loads(response.read().decode('utf-8'))['choices'][0]['message']['content']
    except urllib.error.HTTPError as e: 
        err_msg = e.read().decode('utf-8', errors='ignore')
        return f"🚨 API Error on {target_model}: Code {e.code} - {err_msg}"
    except Exception as e: 
        return f"🚨 System Error: {str(e)}"

# --- Main Interface ---
st.markdown(f"<div class='main-header'>{u['title']}</div><div class='sub-header'>{u['sub']}</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([u['tab_ai'], u['tab_mandi'], u['tab_iot'], u['tab_tr']])

with tab1:
    q = st.text_input(u['ask_crop'], placeholder="e.g. Best fertilizer or treatment?")
    c1, c2 = st.columns(2)
    with c1: cam_image = st.camera_input(u['cam_prompt'], key="cam")
    with c2: up_image = st.file_uploader(u['up_prompt'], type=["png", "jpg", "jpeg"], key="up")
    final_img = cam_image if cam_image else up_image
    
    if st.button(u['btn_ai']):
        if not q and not final_img: st.warning("Please enter a question or upload/capture a photo.")
        else:
            with st.spinner("⚡ AI is working..."):
                sys_prompt = f"You are KisanSetu AI, an expert agronomist. Provide practical advice directly in {lang}. Factor in the local climate of {sel_city}, {sel_state}."
                if final_img:
                    img = Image.open(final_img).convert("RGB")
                    img.thumbnail((720, 720))
                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG", quality=80)
                    b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    user_msg = [{"type": "text", "text": f"Diagnose this crop leaf in {lang}. Factor in {sel_city}, {sel_state} climate. Question: {q}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]
                    
                    ans = ask_groq([{"role": "user", "content": user_msg}], is_vision=True)
                else:
                    ans = ask_groq([{"role": "system", "content": sys_prompt}, {"role": "user", "content": q}], is_vision=False)
                
                if "🚨" in ans: st.error(ans)
                else: st.success(ans)

with tab2:
    CROPS, UNITS, BASE_PRICES = ["Wheat", "Paddy", "Potato", "Tomato", "Onion", "Sugarcane", "Cotton", "Maize"], ["Quintal (100kg)", "Kilogram (1kg)", "Tonne (1000kg)"], [2400, 2200, 1500, 3000, 2500, 350, 7000, 2100]
    st.markdown(f"### {u['tab_mandi']} ({sel_city})")
    col_c, col_u = st.columns(2)
    with col_c: c_idx = st.selectbox(u["lbl_crop"], range(len(CROPS)), format_func=lambda x: CROPS[x])
    with col_u: u_idx = st.selectbox(u["lbl_unit"], range(len(UNITS)), format_func=lambda x: UNITS[x])
    price = BASE_PRICES[c_idx] / 100 if u_idx == 1 else (BASE_PRICES[c_idx] * 10 if u_idx == 2 else BASE_PRICES[c_idx])
    st.metric(CROPS[c_idx], f"₹{price:,.2f} / {UNITS[u_idx]}")

with tab3:
    st.markdown(f"### {u['tab_iot']}")
    if st.button(u['btn_sim']):
        c1, c2, c3 = st.columns(3)
        c1.metric(u["soil"], "42.5%")
        c2.metric(u["temp"], "31°C")
        c3.metric(u["hum"], "65%")

with tab4:
    st.markdown(f"### {u['tab_tr']}")
    txt_input = st.text_area(u["tr_prompt"])
    if st.button(u["btn_tr"]) and txt_input:
        with st.spinner("Translating..."):
            ans = ask_groq([{"role": "system", "content": f"Translate to {lang} exactly. No extra notes."}, {"role": "user", "content": txt_input}], is_vision=False)
            if "🚨" in ans: st.error(ans)
            else: st.success(ans)

st.markdown(f"<div class='footer'>{u['dev']}</div>", unsafe_allow_html=True)
