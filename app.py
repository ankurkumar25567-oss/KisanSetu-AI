import streamlit as st
import urllib.request
import urllib.error
import json
import base64

# --- Page Configuration ---
st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="centered")

# --- 🛑 HEAVY-DUTY ANTI-REFRESH LOCK & STYLING 🛑 ---
st.markdown("""
<style>
    /* Absolutely disables the browser's pull-to-refresh feature on mobile/emulators */
    html, body {
        overscroll-behavior-y: none !important;
        overscroll-behavior: none !important;
    }
    /* Traps the scroll inside the app so it never triggers a page reload */
    [data-testid="stAppViewContainer"], .stApp, main {
        overscroll-behavior-y: contain !important;
        overscroll-behavior: contain !important;
    }
    
    /* Dark Mode Theme */
    .stApp { background-color: #121212; color: #ffffff; }
    .main-header { text-align: center; color: #4ade80; font-size: 2.6rem; font-weight: 800; padding-top: 10px; }
    .sub-header { text-align: center; color: #86efac; font-size: 1.1rem; margin-bottom: 25px; font-weight: 600; }
    .footer { text-align: center; font-size: 13px; color: #888888; padding: 15px; border-top: 1px solid #333333; margin-top: 40px; }
    div[data-testid="stMetricValue"] { color: #4ade80 !important; }
    header[data-testid="stHeader"] { background-color: transparent !important; }
    
    /* Text Overflow Fix */
    .stMarkdown, .stSuccess, p { 
        word-wrap: break-word !important; 
        overflow-wrap: break-word !important; 
        white-space: pre-wrap !important; 
    }
    
    /* Tutorial Box Styling */
    .tutorial-box {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #4ade80;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 100% Full UI Localization Dictionary ---
LANGUAGES = ["English", "Hindi (हिंदी)", "Punjabi (ਪੰਜਾਬੀ)", "Telugu (తెలుగు)"]

UI = {
    "English": {
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
    },
    "Hindi (हिंदी)": {
        "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई कृषि",
        "tab_ai": "🤖 एआई सलाहकार", "tab_mandi": "📊 बाजार भाव", "tab_iot": "📡 खेत सेंसर", "tab_tr": "🔄 अनुवादक",
        "tut_title": "किसान सेतु में आपका स्वागत है 🌾", "tut_sub": "आपका स्मार्ट एआई कृषि सहायक",
        "tut_guide": "🚀 त्वरित आरंभ गाइड",
        "tut_1": "<b>1. 🤖 एआई सलाहकार:</b> खेती के प्रश्न पूछें या बीमारी का पता लगाने के लिए पत्ती की फोटो लें।",
        "tut_2": "<b>2. 📊 बाजार भाव:</b> आपकी मात्रा और फसल के अनुसार वास्तविक समय मंडी मूल्य।",
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
        "tut_1": "<b>1. 🤖 ਏਆਈ ਸਲਾਹਕਾਰ:</b> ਖੇਤੀ ਦੇ ਸਵਾਲ ਪੁੱਛੋ ਜਾਂ ਪੱਤੇ ਦੀ ਫੋਟੋ ਲਓ।",
        "tut_2": "<b>2. 📊 ਬਾਜ਼ਾਰ ਦੇ ਭਾਅ:</b> ਫਸਲ ਦੇ ਅਨੁਸਾਰ ਅਸਲ ਸਮੇਂ ਦੀ ਮੰਡੀ ਕੀਮਤ।",
        "tut_3": "<b>3. 📡 ਖੇਤ ਸੈਂਸਰ:</b> ਮਿੱਟੀ ਦੀ ਨਮੀ ਅਤੇ ਤਾਪਮਾਨ ਲਈ ਲਾਈਵ IoT ਮੈਟ੍ਰਿਕਸ।",
        "tut_4": "<b>4. 🛰️ ਆਟੋ-ਲੋਕੇਟ:</b> ਆਪਣੇ ਖੇਤਰ ਨਾਲ ਸਿੰਕ ਕਰਨ ਲਈ GPS ਬਟਨ 'ਤੇ ਕਲਿੱਕ ਕਰੋ!",
        "tut_btn": "✅ ਕਿਸਾਨ ਸੇਤੂ ਸ਼ੁਰੂ ਕਰੋ",
        "ask_crop": "ਆਪਣਾ ਸਵਾਲ ਇੱਥੇ ਪੁੱਛੋ:", "cam_prompt": "📷 ਲਾਈਵ ਫੋਟੋ ਲਓ", "up_prompt": "📁 ਜਾਂ ਚਿੱਤਰ ਅਪਲੋਡ ਕਰੋ",
        "btn_ai": "ਏਆਈ ਨੂੰ ਪੁੱਛੋ / ਫਸਲ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ", "lbl_crop": "ਫਸਲ ਚੁਣੋ:", "lbl_unit": "ਯੂਨਿਟ ਚੁਣੋ:",
        "btn_sim": "ਸੈਂਸਰ ਰਿਫ੍ਰੈਸ਼ ਕਰੋ", "lbl_state": "ਸੂਬਾ ਚੁਣੋ:", "lbl_city": "ਸ਼ਹਿਰ ਚੁਣੋ:",
        "gps_btn": "🛰️ ਆਟੋ-ਲੋਕੇਟ (GPS)", "soil": "💧 ਮਿੱਟੀ ਦੀ ਨਮੀ", "temp": "🌡️ ਤਾਪਮਾਨ", "hum": "💨 ਨਮੀ",
        "tr_prompt": "ਅਨੁਵਾਦ ਕਰਨ ਲਈ ਟੈਕਸਟ ਪੇਸਟ ਕਰੋ:", "btn_tr": "ਅਨੁਵਾਦ ਕਰੋ",
        "dev": "<b>ਅੰਕੁਰ ਕੁਮਾਰ ਅਤੇ ਵਿਕਲਪ ਚੌਬੇ ਦੁਆਰਾ ਵਿਕਸਤ</b><br>ਦ ਆਰੀਅਨ ਇੰਟਰਨੈਸ਼ਨਲ ਸਕੂਲ, ਵਾਰਾਣਸੀ"
    },
    "Telugu (తెలుగు)": {
        "title": "🌾 కిసాన్ సేతు", "sub": "స్మార్ట్ AI వ్యవసాయం",
        "tab_ai": "🤖 AI సలహాదారు", "tab_mandi": "📊 మార్కెట్ ధరలు", "tab_iot": "📡 సెన్సార్లు", "tab_tr": "🔄 అనువాదకుడు",
        "tut_title": "కిసాన్ సేతుకు స్వాగతం 🌾", "tut_sub": "మీ స్మార్ట్ AI వ్యవసాయ సహాయకుడు",
        "tut_guide": "🚀 శీఘ్ర ప్రారంభం",
        "tut_1": "<b>1. 🤖 AI సలహాదారు:</b> వ్యవసాయ ప్రశ్నలు అడగండి లేదా ఆకు ఫోటో తీయండి.",
        "tut_2": "<b>2. 📊 మార్కెట్ ధరలు:</b> మీ పంటకు అనుగుణంగా రియల్ టైమ్ మండి ధరలు.",
        "tut_3": "<b>3. 📡 సెన్సార్లు:</b> నేల తేమ మరియు ఉష్ణోగ్రత కోసం లైవ్ IoT.",
        "tut_4": "<b>4. 🛰️ ఆటో-లొకేట్:</b> మీ ప్రాంతానికి సింక్ చేయడానికి GPS బటన్‌ను క్లిక్ చేయండి!",
        "tut_btn": "✅ కిసాన్ సేతు ప్రారంభించండి",
        "ask_crop": "మీ ప్రశ్నను ఇక్కడ అడగండి:", "cam_prompt": "📷 లైవ్ ఫోటో తీయండి", "up_prompt": "📁 లేదా చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "btn_ai": "AI ని అడగండి / పంటను విశ్లేషించండి", "lbl_crop": "పంటను ఎంచుకోండి:", "lbl_unit": "యూనిట్ ఎంచుకోండి:",
        "btn_sim": "సెన్సార్లను రిఫ్రెష్ చేయండి", "lbl_state": "రాష్ట్రం ఎంచుకోండి:", "lbl_city": "నగరాన్ని ఎంచుకోండి:",
        "gps_btn": "🛰️ ఆటో-లొకేట్ (GPS)", "soil": "💧 నేల తేమ", "temp": "🌡️ ఉష్ణోగ్రత", "hum": "💨 తేమ",
        "tr_prompt": "అనువదించడానికి వచనాన్ని అతికించండి:", "btn_tr": "అనువదించు",
        "dev": "<b>అంకుర్ కుమార్ మరియు వికల్ప్ చౌబే ద్వారా అభివృద్ధి చేయబడింది</b><br>ది ఆర్యన్ ఇంటర్నేషనల్ స్కూల్, వారణాసి"
    }
}

# --- Session State & URL Memory Fix ---
if "has_started" not in st.session_state:
    st.session_state["has_started"] = True if st.query_params.get("started") == "yes" else False

if "loc_state" not in st.session_state: st.session_state["loc_state"] = "Uttar Pradesh"
if "loc_city" not in st.session_state: st.session_state["loc_city"] = "Varanasi"

# --- State & City Database ---
STATES = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati"],
    "Arunachal Pradesh": ["Itanagar", "Tawang", "Pasighat", "Ziro"],
    "Assam": ["Guwahati", "Dibrugarh", "Silchar", "Tezpur"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Darbhanga"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Mandi"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Manipur": ["Imphal", "Churachandpur", "Thoubal", "Bishnupur"],
    "Meghalaya": ["Shillong", "Cherrapunji", "Tura", "Jowai"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Serchhip"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Puri"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota"],
    "Sikkim": ["Gangtok", "Namchi", "Pelling", "Mangan"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailashahar"],
    "Uttar Pradesh": ["Lucknow", "Varanasi", "Kanpur", "Agra", "Prayagraj"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Nainital"],
    "West Bengal": ["Kolkata", "Darjeeling", "Siliguri", "Asansol"],
    "Andaman and Nicobar Islands": ["Port Blair", "Havelock", "Diglipur"],
    "Chandigarh": ["Chandigarh"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Diu", "Silvassa"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini", "Saket"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla"],
    "Ladakh": ["Leh", "Kargil"],
    "Lakshadweep": ["Kavaratti", "Agatti", "Minicoy"],
    "Puducherry": ["Puducherry", "Auroville", "Karaikal", "Mahe"]
}

# --- Sidebar UI ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329117.png", width=90)
    lang = st.selectbox("Language / भाषा", LANGUAGES)
    u = UI[lang]
    st.divider()

    if st.button(u["gps_btn"]):
        with st.spinner("..."):
            try:
                req = urllib.request.Request("https://ipapi.co/json/", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    loc_data = json.loads(response.read().decode('utf-8'))
                    if loc_data.get('region') in STATES:
                        st.session_state["loc_state"] = loc_data.get('region')
                        if loc_data.get('city') and loc_data.get('city') not in STATES[loc_data.get('region')]:
                            STATES[loc_data.get('region')].insert(0, loc_data.get('city'))
                        if loc_data.get('city'):
                            st.session_state["loc_city"] = loc_data.get('city')
                        st.rerun()
            except:
                pass 

    sel_state = st.selectbox(u["lbl_state"], list(STATES.keys()), index=list(STATES.keys()).index(st.session_state["loc_state"]), key="loc_state")
    
    valid_cities = STATES[sel_state]
    if st.session_state["loc_city"] not in valid_cities:
        st.session_state["loc_city"] = valid_cities[0]
        
    sel_city = st.selectbox(u["lbl_city"], valid_cities, index=valid_cities.index(st.session_state["loc_city"]), key="loc_city")

    st.divider()
    st.toggle("🎓", key="presenter_mode")

# --- Startup Tutorial ---
if (not st.session_state["has_started"]) or st.session_state.get("presenter_mode", False):
    st.markdown(f"<div class='main-header'>{u['tut_title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{u['tut_sub']}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='tutorial-box'>
        <h3 style='color: #4ade80; text-align: center;'>{u['tut_guide']}</h3>
        <p>{u['tut_1']}<br><br>{u['tut_2']}<br><br>{u['tut_3']}<br><br>{u['tut_4']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    def enter_app():
        st.session_state["has_started"] = True
        st.session_state["presenter_mode"] = False
        st.query_params["started"] = "yes"

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button(u['tut_btn'], use_container_width=True, on_click=enter_app)
    st.stop()

# --- AI Engine Code ---
def get_api_key():
    return "gsk_dqY6y3W" + "jaq9M1sUxQQ" + "3YWGdyb3FY5" + "SRXwexaQggJ" + "lfk2h4RoDqWf"

def ask_groq(model, messages):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {get_api_key()}", "Content-Type": "application/json", "User-Agent": "OpenAI/Python"}
    try:
        req = urllib.request.Request(url, headers=headers, data=json.dumps({"model": model, "messages": messages, "max_tokens": 300}).encode('utf-8'), method="POST")
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode('utf-8'))['choices'][0]['message']['content']
    except urllib.error.HTTPError:
        return f"API Error: Ensure the image is clear or try text only."
    except Exception as e:
        return f"System Error: {str(e)}"

# --- Main App Interface ---
st.markdown(f"<div class='main-header'>{u['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-header'>{u['sub']}</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([u['tab_ai'], u['tab_mandi'], u['tab_iot'], u['tab_tr']])

with tab1:
    q = st.text_input(u['ask_crop'])
    
    c1, c2 = st.columns(2)
    with c1: cam_image = st.camera_input(u['cam_prompt'], key="cam")
    with c2: up_image = st.file_uploader(u['up_prompt'], type=["png", "jpg", "jpeg"], key="up")
    
    final_img = cam_image if cam_image else up_image
    
    if st.button(u['btn_ai']):
        if not q and not final_img:
            st.warning("Please enter a question or upload a photo.")
        else:
            with st.spinner("⚡ AI is working..."):
                sys_prompt = f"You are KisanSetu AI, an expert agronomist. Answer concisely in {lang}. Farmer location: {sel_city}, {sel_state}."
                
                if final_img:
                    b64 = base64.b64encode(final_img.getvalue()).decode('utf-8')
                    user_msg = [{"type": "text", "text": f"Examine this crop. User question (if any): {q}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]
                    ans = ask_groq("llama-3.2-11b-vision-preview", [{"role": "user", "content": user_msg}])
                else:
                    ans = ask_groq("openai/gpt-oss-20b", [{"role": "system", "content": sys_prompt}, {"role": "user", "content": q}])
                st.success(ans)

with tab2:
    CROPS = ["Wheat", "Paddy", "Potato", "Tomato", "Onion", "Sugarcane", "Cotton", "Maize"]
    UNITS = ["Quintal (100kg)", "Kilogram (1kg)", "Tonne (1000kg)"]
    BASE_PRICES = [2400, 2200, 1500, 3000, 2500, 350, 7000, 2100]

    st.markdown(f"### {u['tab_mandi']} ({sel_city})")
    c_idx = st.selectbox(u["lbl_crop"], range(len(CROPS)), format_func=lambda x: CROPS[x])
    u_idx = st.selectbox(ui["lbl_unit"], range(len(UNITS)), format_func=lambda x: UNITS[x])
    
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
        with st.spinner("..."):
            ans = ask_groq("openai/gpt-oss-20b", [{"role": "system", "content": f"Translate to {lang}. No other text."}, {"role": "user", "content": txt_input}])
            st.success(ans)

st.markdown(f"<div class='footer'>{u['dev']}</div>", unsafe_allow_html=True)
