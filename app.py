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
</style>
""", unsafe_allow_html=True)

LANGUAGES = [
    "English", "Hindi (हिंदी)", "Punjabi (ਪੰਜਾਬੀ)", "Telugu (తెలుగు)", "Bengali (বাংলা)", 
    "Marathi (मराठी)", "Tamil (தமிழ்)", "Gujarati (ગુજરાતી)", "Kannada (ಕನ್ನಡ)", "Malayalam (മലയാളം)"
]

# UI Localization Dictionary for all supported languages
UI_TEXT = {
    "English": {
        "title": "🌾 KisanSetu", "sub": "Smart AI Agriculture Platform",
        "tab1": "🤖 AI Advisor", "tab2": "📊 Market Rates", "tab3": "🔄 Translator",
        "ask": "Ask your farming question or crop query:", "ask_ph": "e.g. Best organic fertilizer for paddy?",
        "cam": "📷 Take photo", "up": "📁 Or upload image", "btn_ai": "Ask AI / Analyze Crop",
        "mandi_title": "📊 Mandi Prices for", "crop_lbl": "Select Crop:", "unit_lbl": "Select Unit:",
        "tr_title": "🔄 Multilingual Translator", "tr_ph": "Enter text or upload document/image to translate:",
        "tr_btn": "Translate Text / Image", "dev": "Developed by Ankur Kumar & Vikalp Chaubey<br>The Aryan International School, Varanasi"
    },
    "Hindi (हिंदी)": {
        "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई कृषि प्लेटफॉर्म",
        "tab1": "🤖 एआई सलाहकार", "tab2": "📊 बाजार भाव", "tab3": "🔄 अनुवादक",
        "ask": "अपना कृषि प्रश्न या फसल संबंधी जिज्ञासा पूछें:", "ask_ph": "जैसे: धान के लिए सबसे अच्छी जैविक खाद?",
        "cam": "📷 फोटो लें", "up": "📁 या छवि अपलोड करें", "btn_ai": "एआई से पूछें / फसल विश्लेषण करें",
        "mandi_title": "📊 मंडी भाव:", "crop_lbl": "फसल चुनें:", "unit_lbl": "इकाई चुनें:",
        "tr_title": "🔄 बहुभाषी अनुवादक", "tr_ph": "अनुवाद के लिए टेक्स्ट दर्ज करें या दस्तावेज़/छवि अपलोड करें:",
        "tr_btn": "टेक्स्ट / छवि का अनुवाद करें", "dev": "अंकुर कुमार और विकल्प चौबे द्वारा विकसित<br>द आर्यन इंटरनेशनल स्कूल, वाराणसी"
    },
    "Punjabi (ਪੰਜਾਬੀ)": {
        "title": "🌾 ਕਿਸਾਨ ਸੇਤੂ", "sub": "ਸਮਾਰਟ ਏਆਈ ਖੇਤੀਬਾੜੀ ਪਲੇਟਫਾਰਮ",
        "tab1": "🤖 ਏਆਈ ਸਲਾਹਕਾਰ", "tab2": "📊 ਬਾਜ਼ਾਰ ਭਾਵ", "tab3": "🔄 ਅਨੁਵਾਦਕ",
        "ask": "ਆਪਣਾ ਖੇਤੀਬਾੜੀ ਸਵਾਲ ਪੁੱਛੋ:", "ask_ph": "ਉਦਾਹਰਣ ਲਈ: ਝੋਨੇ ਲਈ ਵਧੀਆ ਖਾਦ?",
        "cam": "📷 ਫੋਟੋ ਲਓ", "up": "📁 ਜਾਂ ਫੋਟੋ ਅੱਪਲੋਡ ਕਰੋ", "btn_ai": "ਏਆਈ ਤੋਂ ਪੁੱਛੋ",
        "mandi_title": "📊 ਮੰਡੀ ਭਾਵ:", "crop_lbl": "ਫਸਲ ਚੁਣੋ:", "unit_lbl": "ਯੂਨਿਟ ਚੁਣੋ:",
        "tr_title": "🔄 ਅਨੁਵਾਦਕ", "tr_ph": "ਅਨੁਵਾਦ ਲਈ ਟੈਕਸਟ ਦਰਜ ਕਰੋ:", "tr_btn": "ਅਨੁਵਾਦ ਕਰੋ",
        "dev": "ਅੰਕੁਰ ਕੁਮਾਰ ਅਤੇ ਵਿਕਲਪ ਚੌਬੇ ਦੁਆਰਾ ਵਿਕਸਤ<br>ਦ ਆਰੀਅਨ ਇੰਟਰਨੈਸ਼ਨਲ ਸਕੂਲ, ਵਾਰਾਣਸੀ"
    },
    "Telugu (తెలుగు)": {
        "title": "🌾 కిసాన్ సేతు", "sub": "స్మార్ట్ AI వ్యవసాయ వేదిక",
        "tab1": "🤖 AI సలహాదారు", "tab2": "📊 మార్కెట్ ధరలు", "tab3": "🔄 అనువాదకుడు",
        "ask": "మీ వ్యవసాయ ప్రశ్నను అడగండి:", "ask_ph": "ఉదా: వరికి ఉత్తమమైన ఎరువు?",
        "cam": "📷 ఫోటో తీయండి", "up": "📁 చిత్రం అప్‌లోడ్ చేయండి", "btn_ai": "AIని అడగండి",
        "mandi_title": "📊 మార్కెట్ ధరలు:", "crop_lbl": "పంటను ఎంచుకోండి:", "unit_lbl": "యూనిట్ ఎంచుకోండి:",
        "tr_title": "🔄 అనువాదకుడు", "tr_ph": "అనువదించడానికి టెక్స్ట్ నమోదు చేయండి:", "tr_btn": "అనువదించు",
        "dev": "అంకుర్ కుమార్ & వికల్ప్ చౌబే ద్వారా అభివృద్ధి చేయబడింది"
    },
    "Bengali (বাংলা)": {
        "title": "🌾 কিষাণ সেতু", "sub": "স্মার্ট এআই কৃষি প্ল্যাটফর্ম",
        "tab1": "🤖 এআই উপদেষ্টা", "tab2": "📊 বাজার দর", "tab3": "🔄 অনুবাদক",
        "ask": "আপনার কৃষির প্রশ্ন জিজ্ঞাসা করুন:", "ask_ph": "যেমন: ধানের জন্য সেরা সার?",
        "cam": "📷 ছবি তুলুন", "up": "📁 ছবি আপলোড করুন", "btn_ai": "এআই কে জিজ্ঞাসা করুন",
        "mandi_title": "📊 বাজার দর:", "crop_lbl": "ফসল বাছুন:", "unit_lbl": "একক বাছুন:",
        "tr_title": "🔄 অনুবাদক", "tr_ph": "অনুবাদ করতে টেক্সট লিখুন:", "tr_btn": "অনুবাদ করুন",
        "dev": "অঙ্কুর কুমার এবং বিকল্প চৌবে দ্বারা বিকশিত"
    },
    "Marathi (मराठी)": {
        "title": "🌾 किसान सेतू", "sub": "स्मार्ट एआय कृषी प्लॅटफॉर्म",
        "tab1": "🤖 एआय सल्लागार", "tab2": "📊 बाजार भाव", "tab3": "🔄 अनुवादक",
        "ask": "तुमचा शेतीचा प्रश्न विचार ः", "ask_ph": "उदा. धान्यासाठी उत्तम खत?",
        "cam": "📷 फोटो काढ ः", "up": "📁 फोटो अपलोड करा", "btn_ai": "एआय ला विचारा",
        "mandi_title": "📊 बाजार भाव:", "crop_lbl": "पीक निवडा:", "unit_lbl": "युनिट निवडा:",
        "tr_title": "🔄 अनुवादक", "tr_ph": "मजकूर प्रविष्ट करा:", "tr_btn": "भाषांतर करा",
        "dev": "अंकुर कुमार आणि विकल्प चौबे द्वारे विकसित"
    },
    "Tamil (தமிழ்)": {
        "title": "🌾 கிசான் சேது", "sub": "ஸ்மார்ட் AI விவசாய தளம்",
        "tab1": "🤖 AI ஆலோசகர்", "tab2": "📊 சந்தை விலைகள்", "tab3": "🔄 மொழிபெயர்ப்பாளர்",
        "ask": "உங்கள் விவசாய கேள்வியைக் கேளுங்கள்:", "ask_ph": "எ.கா. நெல்லுக்கு சிறந்த உரம்?",
        "cam": "📷 படம் எடுக்கவும்", "up": "📁 படத்தை பதிவேற்றவும்", "btn_ai": "AI ஐக் கேளுங்கள்",
        "mandi_title": "📊 சந்தை விலைகள்:", "crop_lbl": "பயிரைத் தேர்ந்தெடுக்கவும்:", "unit_lbl": "அலகைத் தேர்ந்தெடுக்கவும்:",
        "tr_title": "🔄 மொழிபெயர்ப்பாளர்", "tr_ph": "உரையை உள்ளிடவும்:", "tr_btn": "மொழிபெயர்க்கவும்",
        "dev": "அம்கூர் குமார் & விகல்ப் சௌபே"
    },
    "Gujarati (ગુજરાતી)": {
        "title": "🌾 કિસાન સેતુ", "sub": "સ્માર્ટ AI કૃષિ પ્લેટફોર્મ",
        "tab1": "🤖 AI સલાહકાર", "tab2": "📊 બજાર ભાવ", "tab3": "🔄 અનુવાદક",
        "ask": "તમારો કૃષિ પ્રશ્ન પૂછો:", "ask_ph": "દા.ત. ડાંગર માટે શ્રેષ્ઠ ખાતર?",
        "cam": "📷 ફોટો લો", "up": "📁 છબી અપલોડ કરો", "btn_ai": "AI ને પૂછો",
        "mandi_title": "📊 બજાર ભાવ:", "crop_lbl": "પાક પસંદ કરો:", "unit_lbl": "એકમ પસંદ કરો:",
        "tr_title": "🔄 અનુવાદક", "tr_ph": "ટેક્સ્ટ દાખલ કરો:", "tr_btn": "અનુવાદ કરો",
        "dev": "અંકુર કુમાર અને વિકલ્પ चौबे દ્વારા વિકસિત"
    },
    "Kannada (ಕನ್ನಡ)": {
        "title": "🌾 ಕಿಸಾನ್ ಸೇತು", "sub": "ಸ್ಮಾರ್ಟ್ AI ಕೃಷಿ ವೇದಿಕೆ",
        "tab1": "🤖 AI ಸಲಹೆಗಾರ", "tab2": "📊 ಮಾರುಕಟ್ಟೆ ದರಗಳು", "tab3": "🔄 ಅನುವಾದಕ",
        "ask": "ನಿಮ್ಮ ಕೃಷಿ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ:", "ask_ph": "ಉದಾ: ಭತ್ತಕ್ಕೆ ಉತ್ತಮ ಗೊಬ್ಬರ?",
        "cam": "📷 ಫೋಟೋ ತೆಗೆಯಿರಿ", "up": "📁 ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ", "btn_ai": "AI ಅನ್ನು ಕೇಳಿ",
        "mandi_title": "📊 ಮಾರುಕಟ್ಟೆ ದರಗಳು:", "crop_lbl": "ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ:", "unit_lbl": "ಘಟಕ ಆಯ್ಕೆಮಾಡಿ:",
        "tr_title": "🔄 ಅನುವಾದಕ", "tr_ph": "ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ:", "tr_btn": "ಅನುವಾದಿಸು",
        "dev": "ಅಂಕುರ್ ಕುಮಾರ್ ಮತ್ತು ವಿಕಲ್ಪ್ ಚೌಬೆ"
    },
    "Malayalam (മലയാളം)": {
        "title": "🌾 കിസാൻ സേതു", "sub": "സ്മാർട്ട് AI കാർഷിക പ്ലാറ്റ്‌ഫോം",
        "tab1": "🤖 AI ഉപദേശകൻ", "tab2": "📊 വിപണി വില", "tab3": "🔄 പരിഭാഷകൻ",
        "ask": "നിങ്ങളുടെ കാർഷിക ചോദ്യം ചോദിക്കുക:", "ask_ph": "ഉദാഹരണം: നെല്ലിന് മികച്ച വളം?",
        "cam": "📷 ഫോട്ടോ എടുക്കുക", "up": "📁 ചിത്രം അപ്‌ലോഡ് ചെയ്യുക", "btn_ai": "AI-യോട് ചോദിക്കുക",
        "mandi_title": "📊 വിപണി വില:", "crop_lbl": "വിള തിരഞ്ഞെടുക്കുക:", "unit_lbl": "യൂണിറ്റ് തിരഞ്ഞെടുക്കുക:",
        "tr_title": "🔄 പരിഭാഷകൻ", "tr_ph": "ടെക്സ്റ്റ് നൽകുക:", "tr_btn": "പരിഭാഷപ്പെടുത്തുക",
        "dev": "അങ്കുർ കുമാറും വികൽപ് ചൗബെയും ചേർന്ന് വികസിപ്പിച്ചത്"
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

tab1, tab2, tab3 = st.tabs([t['tab1'], t['tab2'], t['tab3']])

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
    t_text = st.text_area(t['tr_ph'])
    if st.button(t['tr_btn']) and t_text:
        with st.spinner("Translating..."):
            st.success(ask_openrouter(f"Translate into {lang}: {t_text}"))

st.markdown(f"<div class='footer' style='text-align:center; color:#9ca3af; margin-top:40px; font-size:13px;'><b>{t['dev']}</b></div>", unsafe_allow_html=True)
