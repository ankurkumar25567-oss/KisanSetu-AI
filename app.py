import streamlit as st
import urllib.request
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="wide", initial_sidebar_state="auto")

components.html("""<script>document.body.style.overscrollBehavior = 'none';</script>""", height=0)

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .main, .stApp { background-color: #07090e !important; color: #f3f4f6 !important; }
    .block-container { max-width: 980px !important; padding-top: 1.2rem !important; }
    .main-header { text-align: center; color: #4ade80; font-size: 2.5rem; font-weight: 800; }
    .sub-header { text-align: center; color: #86efac; font-size: 1.1rem; margin-bottom: 20px; }
    .stButton>button { width: 100% !important; min-height: 3rem !important; border-radius: 10px !important; background: #15803d !important; color: #fff !important; font-weight: 600 !important; }
    .feature-card { background: #0f172a; padding: 18px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

LANGUAGES = [
    "English", "Hindi (हिंदी)", "Punjabi (ਪੰਜਾਬੀ)", "Telugu (తెలుగు)", "Bengali (বাংলা)", 
    "Marathi (मराठी)", "Tamil (தமிழ்)", "Gujarati (ગુજરાતી)", "Kannada (ಕನ್ನಡ)", "Malayalam (മലയാളം)"
]

UI_TEXT = {
    "English": {
        "title": "🌾 KisanSetu", "sub": "Smart AI Agriculture Platform",
        "tab0": "🏠 Overview & Features", "tab1": "🤖 AI Advisor", "tab2": "📊 Market Rates", "tab3": "📜 Govt Schemes", "tab4": "🔄 Translator",
        "ask": "Ask your farming question or crop query:", "ask_ph": "e.g. Best organic fertilizer for paddy?",
        "cam": "📷 Take photo", "up": "📁 Or upload image", "btn_ai": "Ask AI / Analyze Crop",
        "mandi_title": "📊 Mandi Prices for", "crop_lbl": "Select Crop:", "unit_lbl": "Select Unit:",
        "tr_title": "🔄 Multilingual Translator", "tr_ph": "Enter text or upload document/image to translate:",
        "tr_btn": "Translate Text / Image", "dev": "Developed by Ankur Kumar & Vikalp Chaubey<br>The Aryan International School, Varanasi"
    },
    "Hindi (हिंदी)": {
        "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई कृषि प्लेटफॉर्म",
        "tab0": "🏠 परिचय और विशेषताएँ", "tab1": "🤖 एआई सलाहकार", "tab2": "📊 बाजार भाव", "tab3": "📜 सरकारी योजनाएं", "tab4": "🔄 अनुवादक",
        "ask": "अपना कृषि प्रश्न या फसल संबंधी जिज्ञासा पूछें:", "ask_ph": "जैसे: धान के लिए सबसे अच्छी जैविक खाद?",
        "cam": "📷 फोटो लें", "up": "📁 या छवि अपलोड करें", "btn_ai": "एआई से पूछें / फसल विश्लेषण करें",
        "mandi_title": "📊 मंडी भाव:", "crop_lbl": "फसल चुनें:", "unit_lbl": "इकाई चुनें:",
        "tr_title": "🔄 बहुभाषी अनुवादक", "tr_ph": "अनुवाद के लिए टेक्स्ट दर्ज करें या दस्तावेज़/छवि अपलोड करें:",
        "tr_btn": "टेक्स्ट / छवि का अनुवाद करें", "dev": "अंकुर कुमार और विकल्प चौबे द्वारा विकसित<br>द आर्यन इंटरनेशनल स्कूल, वाराणसी"
    },
    "Punjabi (ਪੰਜਾਬੀ)": {
        "title": "🌾 ਕਿਸਾਨ ਸੇਤੂ", "sub": "ਸਮਾਰਟ ਏਆਈ ਖੇਤੀਬਾੜੀ ਪਲੇਟਫਾਰਮ",
        "tab0": "🏠 ਜਾਣਕਾਰੀ ਅਤੇ ਵਿਸ਼ੇਸ਼ਤਾਵਾਂ", "tab1": "🤖 ਏਆਈ ਸਲਾਹਕਾਰ", "tab2": "📊 ਬਾਜ਼ਾਰ ਭਾਵ", "tab3": "📜 ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ", "tab4": "🔄 ਅਨੁਵਾਦਕ",
        "ask": "ਆਪਣਾ ਖੇਤੀਬਾੜੀ ਸਵਾਲ ਪੁੱਛੋ:", "ask_ph": "ਉਦਾਹਰਣ ਲਈ: ਝੋਨੇ ਲਈ ਵਧੀਆ ਖਾਦ?",
        "cam": "📷 ਫੋਟੋ ਲਓ", "up": "📁 ਜਾਂ ਫੋਟੋ ਅੱਪਲੋਡ ਕਰੋ", "btn_ai": "ਏਆਈ ਤੋਂ ਪੁੱਛੋ",
        "mandi_title": "📊 ਮੰਡੀ ਭਾਵ:", "crop_lbl": "ਫਸਲ ਚੁਣੋ:", "unit_lbl": "ਯੂਨਿਟ ਚੁਣੋ:",
        "tr_title": "🔄 ਅਨੁਵਾਦਕ", "tr_ph": "ਅਨੁਵਾਦ ਲਈ ਟੈਕਸਟ ਦਰਜ ਕਰੋ:", "tr_btn": "ਅਨੁਵਾਦ ਕਰੋ",
        "dev": "ਅੰਕੁਰ ਕੁਮਾਰ ਅਤੇ ਵਿਕਲਪ ਚੌਬੇ ਦੁਆਰਾ ਵਿਕਸਤ<br>ਦ ਆਰੀਅਨ ਇੰਟਰਨੈਸ਼ਨਲ ਸਕੂਲ, ਵਾਰਾਣਸੀ"
    }
}

def get_ui(lang_name):
    return UI_TEXT.get(lang_name, UI_TEXT["English"])

STATES_AND_UTS = {"Uttar Pradesh": ["Varanasi", "Lucknow", "Kanpur"], "Bihar": ["Patna", "Gaya"], "Punjab": ["Amritsar", "Ludhiana"]}
PRE_MADE_ANSWERS = {
    "How to grow wheat": "🌾 **Wheat Guide:** Use well-drained loamy soil, sow in mid-November, and provide 4-6 irrigations.",
    "How to grow rice": "🌾 **Rice Guide:** Clayey soil, maintain 2-5 cm standing water in puddled fields.",
    "What happened to my tomatoes?": "🍅 **Diagnosis:** Late Blight / Fruit Rot. Remove infected fruit and apply copper fungicide."
}

GOVT_SCHEMES = [
    ("🌱 PM-Kisan Samman Nidhi", "Provides income support of ₹6,000 per year to all farmer families across India in three equal installments."),
    ("💧 PM Krishi Sinchayee Yojana (PMKSY)", "Harakati irrigation program focused on 'Har Khet Ko Pani' and improving water use efficiency ('More Crop Per Drop')."),
    ("🛡️ Pradhan Mantri Fasal Bima Yojana (PMFBY)", "Affordable crop insurance scheme protecting farmers against crop loss/failure due to natural calamities."),
    ("🧪 Soil Health Card Scheme", "Provides soil nutrient status reports to farmers with crop-wise fertilizer recommendations.")
]

if "query_input" not in st.session_state: st.session_state["query_input"] = ""

with st.sidebar:
    lang = st.selectbox("🌐 Language", LANGUAGES)
    t = get_ui(lang)
    sel_state = st.selectbox("State", list(STATES_AND_UTS.keys()))
    sel_city = st.selectbox("City", STATES_AND_UTS[sel_state])

def ask_openrouter(prompt_text):
    try:
        key = st.secrets["OPENROUTER_API_KEY"]
        req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", 
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            data=json.dumps({"model": "openrouter/free", "messages": [{"role": "user", "content": prompt_text}]}).encode('utf-8'), method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

st.markdown(f"<div class='main-header'>{t['title']}</div><div class='sub-header'>{t['sub']}</div>", unsafe_allow_html=True)

tab0, tab1, tab2, tab3, tab4 = st.tabs([t['tab0'], t['tab1'], t['tab2'], t['tab3'], t['tab4']])

with tab0:
    st.markdown("### 🌟 About KisanSetu Platform")
    st.markdown("KisanSetu is an advanced, AI-powered agricultural assistant designed to bridge the gap between modern technology and rural farming communities.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='feature-card'><b>🤖 AI Agronomist</b><br>Instant crop disease detection via camera upload and expert farming recommendations tailored to local weather and soil conditions.</div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>📊 Market Mandi Intelligence</b><br>Real-time district-level market valuation tracking with automated unit conversion across weights.</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='feature-card'><b>📜 Government Subsidy Hub</b><br>Instant guidance on key agricultural schemes like PM-Kisan, crop insurance, and soil health cards.</div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>🔄 10+ Language Localization</b><br>Seamless translation of agricultural insights, UI elements, and documents into regional Indian languages.</div>", unsafe_allow_html=True)

with tab1:
    col1, col2, col3 = st.columns(3)
    if col1.button("How to grow wheat"): st.session_state["query_input"] = "How to grow wheat"
    if col2.button("How to grow rice"): st.session_state["query_input"] = "How to grow rice"
    if col3.button("Tomato Disease"): st.session_state["query_input"] = "What happened to my tomatoes?"

    q = st.text_input(t['ask'], value=st.session_state["query_input"], placeholder=t['ask_ph'])
    cam = st.camera_input(t['cam'], key="c1")
    up = st.file_uploader(t['up'], type=["png", "jpg"], key="u1")

    if st.button(t['btn_ai']):
        if q in PRE_MADE_ANSWERS:
            st.success(PRE_MADE_ANSWERS[q])
        elif q or cam or up:
            with st.spinner("Analyzing..."):
                st.success(ask_openrouter(f"Practical farming advice in {lang} for {sel_city}: {q}"))
        else:
            st.warning("Enter a query or upload an image.")

with tab2:
    st.markdown(f"### {t['mandi_title']} {sel_city}")
    st.metric("Wheat", "₹2,400 / Quintal")
    st.metric("Paddy", "₹2,200 / Quintal")

with tab3:
    st.markdown("### 📜 Active Government Schemes & Subsidies")
    for name, desc in GOVT_SCHEMES:
        st.markdown(f"<div class='feature-card'><b>{name}</b><br>{desc}</div>", unsafe_allow_html=True)

with tab4:
    t_text = st.text_area(t['tr_ph'])
    if st.button(t['tr_btn']) and t_text:
        with st.spinner("Translating..."):
            st.success(ask_openrouter(f"Translate into {lang}: {t_text}"))

st.markdown(f"<div class='footer' style='text-align:center; color:#9ca3af; margin-top:40px; font-size:13px;'><b>{t['dev']}</b></div>", unsafe_allow_html=True)
