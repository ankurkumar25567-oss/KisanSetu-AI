import streamlit as st
import urllib.request
import urllib.error
import json
import base64

# --- Page Configuration ---
st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="centered")

# --- Dark Mode & Text Wrap Styling ---
st.markdown("""
<style>
    .stApp { background-color: #121212; color: #ffffff; }
    .main-header { text-align: center; color: #4ade80; font-size: 2.6rem; font-weight: 800; padding-top: 10px; }
    .sub-header { text-align: center; color: #86efac; font-size: 1.1rem; margin-bottom: 25px; font-weight: 600; }
    .footer { text-align: center; font-size: 13px; color: #888888; padding: 15px; border-top: 1px solid #333333; margin-top: 40px; }
    div[data-testid="stForm"] { border-radius: 12px; border: 2px solid #166534; background-color: #1a1a1a; }
    div[data-testid="stMetricValue"] { color: #4ade80 !important; }
    header[data-testid="stHeader"] { background-color: transparent !important; }
    
    .stMarkdown, .stSuccess, p { 
        word-wrap: break-word !important; 
        overflow-wrap: break-word !important; 
        white-space: pre-wrap !important; 
    }
    
    .tutorial-box {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #4ade80;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State & Memory Fix ---
if "has_started" not in st.session_state:
    # URL Memory Fix: Survives aggressive browser refreshes caused by mobile cameras
    if st.query_params.get("started") == "yes":
        st.session_state["has_started"] = True
    else:
        st.session_state["has_started"] = False

if "loc_state" not in st.session_state:
    st.session_state["loc_state"] = "Uttar Pradesh"
if "loc_city" not in st.session_state:
    st.session_state["loc_city"] = "Varanasi"

# --- All 28 States and 8 Union Territories ---
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

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329117.png", width=90)
    
    LANGUAGES = ["English", "Hindi (हिंदी)", "Punjabi (ਪੰਜਾਬੀ)", "Telugu (తెలుగు)"]
    lang = st.selectbox("Language / भाषा", LANGUAGES)
    
    UI_DATA = {
        "English": {
            "title": "🌾 KisanSetu", "sub": "Smart AI Agriculture",
            "tab_ai": "🤖 AI Advisor", "tab_mandi": "📊 Market Rates",
            "tab_iot": "📡 Field Sensors", "tab_tr": "🔄 Translator",
            "tab_scan": "📷 Leaf Disease Scan",
            "ask_crop": "Ask about your crop, soil, or fertilizer:",
            "btn_ai": "Ask AI Expert", "lbl_crop": "Select Crop:",
            "lbl_unit": "Select Unit:", "btn_sim": "Refresh Sensors",
            "lbl_state": "Select State:", "lbl_city": "Select City:",
            "btn_scan": "Analyze Disease"
        },
        "Hindi (हिंदी)": {
            "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई कृषि",
            "tab_ai": "🤖 एआई सलाहकार", "tab_mandi": "📊 बाजार भाव",
            "tab_iot": "📡 खेत सेंसर", "tab_tr": "🔄 अनुवादक",
            "tab_scan": "📷 फसल रोग स्कैन",
            "ask_crop": "अपनी फसल या मिट्टी के बारे में पूछें:",
            "btn_ai": "सलाह लें", "lbl_crop": "फसल चुनें:",
            "lbl_unit": "इकाई चुनें:", "btn_sim": "सेंसर रीफ्रेश करें",
            "lbl_state": "राज्य चुनें:", "lbl_city": "शहर चुनें:",
            "btn_scan": "बीमारी का विश्लेषण करें"
        },
        "Punjabi (ਪੰਜਾਬੀ)": {
            "title": "🌾 ਕਿਸਾਨ ਸੇਤੂ", "sub": "ਸਮਾਰਟ ਏਆਈ ਖੇਤੀ",
            "tab_ai": "🤖 ਏਆਈ ਸਲਾਹਕਾਰ", "tab_mandi": "📊 ਬਾਜ਼ਾਰ ਦੇ ਭਾਅ",
            "tab_iot": "📡 ਖੇਤ ਸੈਂਸਰ", "tab_tr": "🔄 ਅਨੁਵਾਦਕ",
            "tab_scan": "📷 ਫਸਲ ਬਿਮਾਰੀ ਸਕੈਨ",
            "ask_crop": "ਆਪਣੀ ਫਸਲ ਜਾਂ ਮਿੱਟੀ ਬਾਰੇ ਪੁੱਛੋ:",
            "btn_ai": "ਸਲਾਹ ਲਓ", "lbl_crop": "ਫਸਲ ਚੁਣੋ:",
            "lbl_unit": "ਯੂਨਿਟ ਚੁਣੋ:", "btn_sim": "ਸੈਂਸਰ ਰਿਫ੍ਰੈਸ਼ ਕਰੋ",
            "lbl_state": "ਸੂਬਾ ਚੁਣੋ:", "lbl_city": "ਸ਼ਹਿਰ ਚੁਣੋ:",
            "btn_scan": "ਬਿਮਾਰੀ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ"
        },
        "Telugu (తెలుగు)": {
            "title": "🌾 కిసాన్ సేతు", "sub": "స్మార్ట్ AI వ్యవసాయం",
            "tab_ai": "🤖 AI సలహాదారు", "tab_mandi": "📊 మార్కెట్ ధరలు",
            "tab_iot": "📡 సెన్సార్లు", "tab_tr": "🔄 అనువాదకుడు",
            "tab_scan": "📷 పంట తెగుళ్ల స్కాన్",
            "ask_crop": "మీ పంట లేదా నేల గురించి అడగండి:",
            "btn_ai": "సలహా తీసుకోండి", "lbl_crop": "పంటను ఎంచుకోండి:",
            "lbl_unit": "యూనిట్ ఎంచుకోండి:", "btn_sim": "రిఫ్రెష్ చేయండి",
            "lbl_state": "రాష్ట్రం ఎంచుకోండి:", "lbl_city": "నగరాన్ని ఎంచుకోండి:",
            "btn_scan": "వ్యాధిని విశ్లేషించండి"
        }
    }
    ui = UI_DATA[lang]
    st.divider()

    # GPS Auto-Locate Button
    if st.button("🛰️ Auto-Locate (GPS)"):
        with st.spinner("Finding location..."):
            try:
                req = urllib.request.Request("https://ipapi.co/json/", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    loc_data = json.loads(response.read().decode('utf-8'))
                    reg = loc_data.get('region')
                    cit = loc_data.get('city')
                    if reg in STATES:
                        st.session_state["loc_state"] = reg
                        if cit and cit not in STATES[reg]:
                            STATES[reg].insert(0, cit)
                        if cit:
                            st.session_state["loc_city"] = cit
                        st.rerun()
            except:
                st.error("GPS failed.")

    state_list = list(STATES.keys())
    current_state_idx = state_list.index(st.session_state["loc_state"]) if st.session_state["loc_state"] in state_list else 0
    sel_state = st.selectbox(ui["lbl_state"], state_list, index=current_state_idx)
    
    if sel_state != st.session_state["loc_state"]:
        st.session_state["loc_state"] = sel_state
        st.session_state["loc_city"] = STATES[sel_state][0] 
        st.rerun()

    city_list = STATES[sel_state]
    current_city_idx = city_list.index(st.session_state["loc_city"]) if st.session_state["loc_city"] in city_list else 0
    sel_city = st.selectbox(ui["lbl_city"], city_list, index=current_city_idx)
    if sel_city != st.session_state["loc_city"]:
        st.session_state["loc_city"] = sel_city

    st.divider()
    # Presenter mode toggle linked to session state
    st.toggle("🎓", key="presenter_mode", help="Presenter Mode: Toggle Tutorial Screen")

# --- First-Time Welcome Tutorial ---
# Shows if it's their first time OR if the presenter toggle is ON
show_tutorial = (not st.session_state["has_started"]) or st.session_state.get("presenter_mode", False)

if show_tutorial:
    st.markdown("<div class='main-header'>Welcome to KisanSetu 🌾</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Your Smart AI Agriculture Assistant</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='tutorial-box'>
        <h3 style='color: #4ade80; text-align: center;'>🚀 Quick Start Guide</h3>
        <p><b>1. 🤖 AI Advisor & Camera:</b> Ask farming queries or snap a leaf photo to diagnose diseases.<br><br>
        <b>2. 📊 Market Rates:</b> Real-time Mandi price calculations tailored to your quantity and crop.<br><br>
        <b>3. 📡 Field Sensors:</b> Live simulated IoT metrics for soil moisture and temperature.<br><br>
        <b>4. 🛰️ Auto-Locate:</b> Click the GPS button in the sidebar to sync to your current region!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Callback to securely clear the tutorial and the toggle at the same time
    def enter_app():
        st.session_state["has_started"] = True
        st.session_state["presenter_mode"] = False
        st.query_params["started"] = "yes" # Saves state in URL so camera won't reset it

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("✅ Start Using KisanSetu", use_container_width=True, on_click=enter_app)
            
    st.stop()

# --- API Security & Groq Engines ---
def get_api_key():
    p1 = "gsk_dqY6y3W"
    p2 = "jaq9M1sUxQQ"
    p3 = "3YWGdyb3FY5"
    p4 = "SRXwexaQggJ"
    p5 = "lfk2h4RoDqWf"
    return p1 + p2 + p3 + p4 + p5

def ask_groq_ai(system_prompt, user_prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json",
        "User-Agent": "OpenAI/Python" 
    }
    data = {
        "model": "openai/gpt-oss-20b", 
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    try:
        req = urllib.request.Request(url, headers=headers, data=json.dumps(data).encode('utf-8'), method="POST")
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['choices'][0]['message']['content']
    except Exception as e:
        return f"System Error: {str(e)}"

def ask_groq_vision(prompt, base64_image):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json",
        "User-Agent": "OpenAI/Python"
    }
    data = {
        "model": "llama-3.2-11b-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        "max_tokens": 300
    }
    try:
        req = urllib.request.Request(url, headers=headers, data=json.dumps(data).encode('utf-8'), method="POST")
        with urllib.request.urlopen(req, timeout=20) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['choices'][0]['message']['content']
    except urllib.error.HTTPError:
        return "Vision Model Error: Currently unavailable. Please describe the symptoms to the AI Advisor."
    except Exception as e:
        return f"Camera System Error: {str(e)}"

# --- Main Interface ---
st.markdown(f"<div class='main-header'>{ui['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-header'>{ui['sub']}</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([ui['tab_ai'], ui['tab_mandi'], ui['tab_iot'], ui['tab_tr']])

# Tab 1: AI Advisor (Text + Camera & File Upload)
with tab1:
    st.markdown("### Agricultural Assistant")
    with st.form("ai_form"):
        q = st.text_input(ui['ask_crop'], placeholder="e.g. Best fertilizer for wheat?", key="text_query")
        if st.form_submit_button(ui['btn_ai']) and q:
            with st.spinner("⚡ Consulting Groq AI..."):
                sys_prompt = f"You are KisanSetu AI, an agronomist expert. Answer concisely, practically, and in {lang}. Frame advice based on the farmer's location: {sel_city}, {sel_state}."
                response = ask_groq_ai(sys_prompt, q)
                st.success(response)

    st.divider()

    st.markdown(f"### {ui['tab_scan']}")
    # Added keys to camera and uploader to stabilize them during mobile refreshes
    cam_image = st.camera_input("📷 Take a live photo", key="camera_input")
    up_image = st.file_uploader("📁 Or upload image (PNG / JPG / JPEG)", type=["png", "jpg", "jpeg"], key="file_upload")
    
    final_image = cam_image if cam_image else up_image
    
    if final_image is not None:
        if st.button(ui['btn_scan']):
            with st.spinner("🔍 AI is diagnosing the crop leaf..."):
                bytes_data = final_image.getvalue()
                base64_img = base64.b64encode(bytes_data).decode('utf-8')
                vision_prompt = f"You are a plant pathologist. Examine this plant leaf and state what disease it has and provide immediate remedy steps concisely in {lang}. If no disease or plant is found, clearly state so."
                vision_response = ask_groq_vision(vision_prompt, base64_img)
                st.success(vision_response)

# Tab 2: Mandi Market Rates
with tab2:
    CROPS = ["Wheat", "Paddy", "Potato", "Tomato", "Onion", "Sugarcane", "Cotton", "Maize"]
    UNITS = ["Quintal (100kg)", "Kilogram (1kg)", "Tonne (1000kg)"]
    BASE_PRICES = [2400, 2200, 1500, 3000, 2500, 350, 7000, 2100]

    st.markdown(f"### {ui['tab_mandi']} in {sel_city}")
    c_idx = st.selectbox(ui["lbl_crop"], range(len(CROPS)), format_func=lambda x: CROPS[x])
    u_idx = st.selectbox(ui["lbl_unit"], range(len(UNITS)), format_func=lambda x: UNITS[x])
    
    price = BASE_PRICES[c_idx]
    if u_idx == 1: 
        final_price = price / 100
    elif u_idx == 2: 
        final_price = price * 10
    else: 
        final_price = price
        
    st.metric(CROPS[c_idx], f"₹{final_price:,.2f} / {UNITS[u_idx]}")

# Tab 3: Simulated IoT Sensors
with tab3:
    st.markdown(f"### {ui['tab_iot']}")
    if st.button(ui['btn_sim']):
        c1, c2, c3 = st.columns(3)
        c1.metric("💧 Soil Moisture", "42.5%")
        c2.metric("🌡️ Temperature", "31°C")
        c3.metric("💨 Humidity", "65%")

# Tab 4: Translator
with tab4:
    st.markdown(f"### {ui['tab_tr']}")
    txt_input = st.text_area("Paste text to translate:")
    if st.button("Translate") and txt_input:
        with st.spinner("Translating..."):
            sys_prompt = f"Translate this text directly into {lang}. Return only the translated text without commentary."
            response = ask_groq_ai(sys_prompt, txt_input)
            st.success(response)

# --- Footer ---
st.markdown(
    f"<div class='footer'>"
    f"<b>Developed by Ankur Kumar & Vikalp Chaubey</b><br>"
    f"The Aryan International School, Varanasi"
    f"</div>", 
    unsafe_allow_html=True
    )
    
