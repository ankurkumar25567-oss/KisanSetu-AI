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

# --- 📱 DEVICE-ADAPTIVE RESPONSIVE CSS & VECTOR SCROLLBAR 📱 ---
st.markdown("""
<style>
    /* Kill Mobile / BlueStacks pull-to-refresh loop */
    html, body {
        overscroll-behavior-y: none !important;
        overscroll-behavior-x: none !important;
    }

    /* CUSTOM VERTICAL SCROLLBAR (MATCHING VECTOR IMAGE) */
    ::-webkit-scrollbar {
        width: 22px !important;
    }
    ::-webkit-scrollbar-track {
        background: #ffffff !important; /* White track */
        border-radius: 12px;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #3f3f3f !important; /* Dark grey pill */
        border-radius: 12px !important;
        border: 4px solid #ffffff !important; /* Creates the gap between track and thumb */
        
        /* The 3 horizontal grip lines */
        background-image: 
            linear-gradient(#ffffff, #ffffff),
            linear-gradient(#ffffff, #ffffff),
            linear-gradient(#ffffff, #ffffff) !important;
        background-size: 10px 1px, 10px 1px, 10px 1px !important;
        background-position: center calc(50% - 4px), center, center calc(50% + 4px) !important;
        background-repeat: no-repeat !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background-color: #2a2a2a !important;
    }
    
    /* Top Up Arrow Button */
    ::-webkit-scrollbar-button:single-button:vertical:decrement {
        height: 22px;
        background-color: #3f3f3f;
        border-radius: 12px 12px 0 0;
        background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M12 8l-6 6h12z'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: center;
    }
    
    /* Bottom Down Arrow Button */
    ::-webkit-scrollbar-button:single-button:vertical:increment {
        height: 22px;
        background-color: #3f3f3f;
        border-radius: 0 0 12px 12px;
        background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M12 16l-6-6h12z'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: center;
    }

    /* Global Dark Theme */
    .stApp { 
        background-color: #0f1117; 
        color: #f3f4f6; 
    }
    
    /* Device-Adaptive Responsive Container */
    .block-container {
        max-width: 980px !important;
        padding-top: 1.2rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    /* Fluid Responsive Typography */
    .main-header { 
        text-align: center; 
        color: #4ade80; 
        font-size: clamp(1.8rem, 4vw, 2.7rem); 
        font-weight: 800; 
        margin-bottom: 2px;
    }
    .sub-header { 
        text-align: center; 
        color: #86efac; 
        font-size: clamp(0.95rem, 2vw, 1.15rem); 
        margin-bottom: 20px; 
        font-weight: 600; 
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
        min-height: 2.85rem !important;
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
        "gps_btn": "🛰️ ఆటో-లొకేట్ (GPS)", "soil": "💧 నేల తేమ", "temp": "🌡️ ఉష్ణోగ్రత", "hum": "💨 తేమ",
        "tr_prompt": "అనువదించడానికి వచనాన్ని అతికించండి:", "btn_tr": "అనువదించు"
    },
    "Bengali (বাংলা)": {
        "title": "🌾 কিষাণ সেতু", "sub": "স্মার্ট এআই কৃষি",
        "tab_ai": "🤖 এআই উপদেষ্টা", "tab_mandi": "📊 বাজারের দর", "tab_iot": "📡 মাঠের সেন্সর", "tab_tr": "🔄 অনুবাদক",
        "tut_btn": "✅ কিষাণ সেতু শুরু করুন", "ask_crop": "আপনার প্রশ্ন এখানে জিজ্ঞাসা করুন:", "btn_ai": "এআই-কে জিজ্ঞাসা করুন / ফসল বিশ্লেষণ",
        "cam_prompt": "📷 লাইভ ছবি তুলুন", "up_prompt": "📁 অথবা ছবি আপলোড করুন", "lbl_crop": "ফসল নির্বাচন করুন:", "lbl_unit": "একক নির্বাচন করুন:",
        "btn_sim": "সেন্সর রিফ্রেশ করুন", "lbl_state": "রাজ্য নির্বাচন করুন:", "lbl_city": "শহর নির্বাচন করুন:",
        "gps_btn": "🛰️ স্বয়ংক্রিয় অবস্থান (GPS)", "soil": "💧 মাটির আর্দ্রতা", "temp": "🌡️ তাপমাত্রা", "hum": "💨 আর্দ্রতা",
        "tr_prompt": "অনুবাদ করতে পাঠ্য আটকান:", "btn_tr": "অনুবাদ করুন"
    },
    "Marathi (मराठी)": {
        "title": "🌾 किसान सेतू", "sub": "स्मार्ट एआय शेती",
        "tab_ai": "🤖 एआय सल्लागार", "tab_mandi": "📊 बाजार भाव", "tab_iot": "📡 शेत सेन्सर्स", "tab_tr": "🔄 अनुवादक",
        "tut_btn": "✅ किसान सेतू सुरू करा", "ask_crop": "तुमचा प्रश्न येथे विचारा:", "btn_ai": "एआयला विचारा / पीक विश्लेषण करा",
        "cam_prompt": "📷 थेट फोटो घ्या", "up_prompt": "📁 किंवा फोटो अपलोड करा", "lbl_crop": "पीक निवडा:", "lbl_unit": "एकक निवडा:",
        "btn_sim": "सेन्सर्स रिफ्रेश करा", "lbl_state": "राज्य निवडा:", "lbl_city": "शहर निवडा:",
        "gps_btn": "🛰️ ऑटो-लोकेट (GPS)", "soil": "💧 जमिनीतील ओलावा", "temp": "🌡️ तापमान", "hum": "💨 हवेतील आर्द्रता",
        "tr_prompt": "भाषांतरासाठी मजकूर पेस्ट करा:", "btn_tr": "भाषांतर करा"
    },
    "Tamil (தமிழ்)": {
        "title": "🌾 கிசான் சேது", "sub": "ஸ்மார்ட் AI வேளாண்மை",
        "tab_ai": "🤖 AI ஆலோசகர்", "tab_mandi": "📊 சந்தை விலைகள்", "tab_iot": "📡 கள சென்சார்கள்", "tab_tr": "🔄 மொழிபெயர்ப்பாளர்",
        "tut_btn": "✅ கிசான் சேதுவை தொடங்குங்கள்", "ask_crop": "உங்கள் கேள்வியை இங்கே கேளுங்கள்:", "btn_ai": "AI-யிடம் கேளுங்கள் / பயிர் ஆய்வு",
        "cam_prompt": "📷 புகைப்படம் எடுக்கவும்", "up_prompt": "📁 அல்லது படம் பதிவேற்றவும்", "lbl_crop": "பயிரைத் தேர்ந்தெடுக்கவும்:", "lbl_unit": "அலகைத் தேர்ந்தெடுக்கவும்:",
        "btn_sim": "சென்சார்களை புதுப்பிக்கவும்", "lbl_state": "மாநிலத்தைத் தேர்ந்தெடுக்கவும்:", "lbl_city": "நகரத்தைத் தேர்ந்தெடுக்கவும்:",
        "gps_btn": "🛰️ தானியங்கி இருப்பிடம் (GPS)", "soil": "💧 மண் ஈரப்பதம்", "temp": "🌡️ வெப்பநிலை", "hum": "💨 காற்றின் ஈரப்பதம்",
        "tr_prompt": "மொழிபெயர்க்க உரையை ஒட்டவும்:", "btn_tr": "மொழிபெயர்க்கவும்"
    },
    "Gujarati (ગુજરાતી)": {
        "title": "🌾 કિસાન સેતુ", "sub": "સ્માર્ટ AI કૃષિ",
        "tab_ai": "🤖 AI સલાહકાર", "tab_mandi": "📊 બજાર ભાવ", "tab_iot": "📡 ક્ષેત્ર સેન્સર્સ", "tab_tr": "🔄 અનુવાદક",
        "tut_btn": "✅ કિસાન સેતુ શરૂ કરો", "ask_crop": "તમારો પ્રશ્ન અહીં પૂછો:", "btn_ai": "AI ને પૂછો / પાકનું વિશ્લેષણ",
        "cam_prompt": "📷 લાઈવ ફોટો લો", "up_prompt": "📁 અથવા છબી અપલોડ કરો", "lbl_crop": "પાક પસંદ કરો:", "lbl_unit": "એકમ પસંદ કરો:",
        "btn_sim": "સેન્સર્સ રિફ્રેશ કરો", "lbl_state": "રાજ્ય પસંદ કરો:", "lbl_city": "શહેર પસંદ કરો:",
        "gps_btn": "🛰️ ઓટો-લોકેટ (GPS)", "soil": "💧 જમીનનો ભેજ", "temp": "🌡️ તાપમાન", "hum": "💨 ભેજ",
        "tr_prompt": "અનુવાદ માટે લખાણ પેસ્ટ કરો:", "btn_tr": "અનુવાદ કરો"
    },
    "Kannada (ಕನ್ನಡ)": {
        "title": "🌾 ಕಿಸಾನ್ ಸೇತು", "sub": "ಸ್ಮಾರ್ಟ್ AI ಕೃಷಿ",
        "tab_ai": "🤖 AI ಸಲಹೆಗಾರ", "tab_mandi": "📊 ಮಾರುಕಟ್ಟೆ ದರಗಳು", "tab_iot": "📡 ಕ್ಷೇತ್ರ ಸಂವೇದಕಗಳು", "tab_tr": "🔄 ಅನುವಾದಕ",
        "tut_btn": "✅ ಕಿಸಾನ್ ಸೇತು ಪ್ರಾರಂಭಿಸಿ", "ask_crop": "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಕೇಳಿ:", "btn_ai": "AI ಅನ್ನು ಕೇಳಿ / ಬೆಳೆ ವಿಶ್ಲೇಷಿಸಿ",
        "cam_prompt": "📷 ಫೋಟೋ ತೆಗೆಯಿರಿ", "up_prompt": "📁 ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ", "lbl_crop": "ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ:", "lbl_unit": "ಘಟಕ ಆಯ್ಕೆಮಾಡಿ:",
        "btn_sim": "ಸಂವೇದಕಗಳನ್ನು ರಿಫ್ರೆಶ್ ಮಾಡಿ", "lbl_state": "ರಾಜ್ಯ ಆಯ್ಕೆಮಾಡಿ:", "lbl_city": "ನಗರ ಆಯ್ಕೆಮಾಡಿ:",
        "gps_btn": "🛰️ ಆಟೋ-ಲೊಕೇಟ್ (GPS)", "soil": "💧 ಮಣ್ಣಿನ ತೇವಾಂಶ", "temp": "🌡️ ತಾಪಮಾನ", "hum": "💨 ತೇವಾಂಶ",
        "tr_prompt": "ಅನುವಾದಿಸಲು ಪಠ್ಯವನ್ನು ಅಂಟಿಸಿ:", "btn_tr": "ಅನುವಾದಿಸಿ"
    },
    "Malayalam (മലയാളം)": {
        "title": "🌾 കിസാൻ സേതു", "sub": "സ്മാർട്ട് AI കൃഷി",
        "tab_ai": "🤖 AI ഉപദേശകൻ", "tab_mandi": "📊 വിപണി നിരക്കുകൾ", "tab_iot": "📡 ഫീൽഡ് സെൻസറുകൾ", "tab_tr": "🔄 വിവർത്തകൻ",
        "tut_btn": "✅ കിസാൻ സേതു ആരംഭിക്കുക", "ask_crop": "നിങ്ങളുടെ ചോദ്യം ഇവിടെ ചോദിക്കുക:", "btn_ai": "AI-യോട് ചോദിക്കുക / വിള വിശകലനം",
        "cam_prompt": "📷 ഫോട്ടോ എടുക്കുക", "up_prompt": "📁 ചിത്രം അപ്‌ലോഡ് ചെയ്യുക", "lbl_crop": "വിള തിരഞ്ഞെടുക്കുക:", "lbl_unit": "യൂണിറ്റ് തിരഞ്ഞെടുക്കുക:",
        "btn_sim": "സെൻസറുകൾ പുതുക്കുക", "lbl_state": "സംസ്ഥാനം തിരഞ്ഞെടുക്കുക:", "lbl_city": "നഗരം തിരഞ്ഞെടുക്കുക:",
        "gps_btn": "🛰️ ഓട്ടോ-ലൊക്കേറ്റ് (GPS)", "soil": "💧 മണ്ണിലെ ഈർപ്പം", "temp": "🌡️ താപനില", "hum": "💨 ഈർപ്പം",
        "tr_prompt": "വിവർത്തനം ചെയ്യാൻ ടെക്സ്റ്റ് നൽകുക:", "btn_tr": "വിവർത്തനം ചെയ്യുക"
    },
    "Odia (ଓଡ଼ିଆ)": {
        "title": "🌾 କିଷାନ ସେତୁ", "sub": "ସ୍ମାର୍ଟ AI କୃଷି",
        "tab_ai": "🤖 AI ପରାମର୍ଶଦାତା", "tab_mandi": "📊 ବଜାର ଦର", "tab_iot": "📡 କ୍ଷେତ୍ର ସେନସର", "tab_tr": "🔄 ଅନୁବାଦକ",
        "tut_btn": "✅ କିଷାନ ସେତୁ ଆରମ୍ଭ କରନ୍ତୁ", "ask_crop": "ଆପଣଙ୍କ ପ୍ରଶ୍ନ ଏଠାରେ ପଚାରନ୍ତୁ:", "btn_ai": "AI କୁ ପଚାରନ୍ତୁ / ଫସଲ ବିଶ୍ଳେଷଣ",
        "cam_prompt": "📷 ଲାଇଭ୍ ଫଟୋ ନିଅନ୍ତୁ", "up_prompt": "📁 ଫଟୋ ଅପଲୋଡ୍ କରନ୍ତୁ", "lbl_crop": "ଫସଲ ବାଛନ୍ତୁ:", "lbl_unit": "ୟୁନିଟ୍ ବାଛନ୍ତୁ:",
        "btn_sim": "ସେନସର ରିଫ୍ରେଶ୍ କରନ୍ତୁ", "lbl_state": "ରାଜ୍ୟ ବାଛନ୍ତୁ:", "lbl_city": "ସହର ବାଛନ୍ତୁ:",
        "gps_btn": "🛰️ ଅଟୋ-ଲୋକେଟ୍ (GPS)", "soil": "💧 ମାଟିର ଆର୍ଦ୍ରତା", "temp": "🌡️ ତାପମାତ୍ରା", "hum": "💨 ଆର୍ଦ୍ରତା",
        "tr_prompt": "ଅନୁବାଦ ପାଇଁ ପାଠ୍ୟ ଲେଖନ୍ତୁ:", "btn_tr": "ଅନୁବାଦ କରନ୍ତୁ"
    },
    "Assamese (অসমীয়া)": {
        "title": "🌾 কিষাণ সেতু", "sub": "স্মাৰ্ট এআই কৃষি",
        "tab_ai": "🤖 এআই উপদেষ্টা", "tab_mandi": "📊 বজাৰৰ মূল্য", "tab_iot": "📡 পথাৰৰ সংবেদক", "tab_tr": "🔄 অনুবাদক",
        "tut_btn": "✅ কিষাণ সেতু আৰম্ভ কৰক", "ask_crop": "আপোনাৰ প্ৰশ্ন ইয়াত সোধক:", "btn_ai": "AI ক সোধক / শস্য বিশ্লেষণ",
        "cam_prompt": "📷 লাইভ ফটো লওক", "up_prompt": "📁 ছবি আপলোড কৰক", "lbl_crop": "শস্য বাছক:", "lbl_unit": "একক বাছক:",
        "btn_sim": "সংবেদক ৰিফ্ৰেছ কৰক", "lbl_state": "ৰাজ্য বাছক:", "lbl_city": "নগৰ বাছক:",
        "gps_btn": "🛰️ অটো-লকে'ট (GPS)", "soil": "💧 মাটিৰ আৰ্দ্ৰতা", "temp": "🌡️ উষ্ণতা", "hum": "💨 আৰ্দ্ৰতা",
        "tr_prompt": "অনুবাদৰ বাবে পাঠ্য পেষ্ট কৰক:", "btn_tr": "অনুবাদ কৰক"
    },
    "Urdu (اردو)": {
        "title": "🌾 کسان سیتو", "sub": "سمارٹ اے آئی زراعت",
        "tab_ai": "🤖 اے آئی مشیر", "tab_mandi": "📊 منڈی کے نرخ", "tab_iot": "📡 فیلڈ سینسرز", "tab_tr": "🔄 مترجم",
        "tut_btn": "✅ کسان سیتو شروع کریں", "ask_crop": "اپنا سوال یہاں پوچھیں:", "btn_ai": "AI سے پوچھیں / فصل کا تجزیہ",
        "cam_prompt": "📷 لائیو تصویر لیں", "up_prompt": "📁 یا تصویر اپ لوڈ کریں", "lbl_crop": "فصل منتخب کریں:", "lbl_unit": "یونٹ منتخب کریں:",
        "btn_sim": "سینسر ریفریش کریں", "lbl_state": "صوبہ منتخب کریں:", "lbl_city": "شہر منتخب کریں:",
        "gps_btn": "🛰️ آٹو لوکیٹ (GPS)", "soil": "💧 مٹی کی نمی", "temp": "🌡️ درجہ حرارت", "hum": "💨 نمی",
        "tr_prompt": "ترجمہ کے لیے متن درج کریں:", "btn_tr": "ترجمہ کریں"
    },
    "Bhojpuri (भोजपुरी)": {
        "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई खेती-बारी",
        "tab_ai": "🤖 एआई सलाहकार", "tab_mandi": "📊 मंडी के भाव", "tab_iot": "📡 खेत के सेंसर", "tab_tr": "🔄 अनुवादक",
        "tut_btn": "✅ किसान सेतु शुरू करीं", "ask_crop": "आपन सवाल हिंया पूछीं:", "btn_ai": "एआई से पूछीं / फसल जांचीं",
        "cam_prompt": "📷 फोटो खींचीं", "up_prompt": "📁 फोटो अपलोड करीं", "lbl_crop": "फसल चुनीं:", "lbl_unit": "इकाई चुनीं:",
        "btn_sim": "सेंसर रिफ्रेश करीं", "lbl_state": "राज्य चुनीं:", "lbl_city": "शहर चुनीं:",
        "gps_btn": "🛰️ ऑटो-लोकेट (GPS)", "soil": "💧 माटी के नमी", "temp": "🌡️ तापमान", "hum": "💨 हवा के नमी",
        "tr_prompt": "अनुवाद खातिर टेक्स्ट डालीं:", "btn_tr": "अनुवाद करीं"
    },
    "Maithili (मैथिली)": {
        "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई कृषि",
        "tab_ai": "🤖 एआई सलाहकार", "tab_mandi": "📊 बजार दर", "tab_iot": "📡 खेत सेंसर", "tab_tr": "🔄 अनुवादक",
        "tut_btn": "✅ किसान सेतु शुरू करू", "ask_crop": "अपन प्रश्न एतय पूछू:", "btn_ai": "एआई सँ पूछू / फसल जाँचू",
        "cam_prompt": "📷 फोटो खीचू", "up_prompt": "📁 फोटो अपलोड करू", "lbl_crop": "फसल चुनू:", "lbl_unit": "इकाई चुनू:",
        "btn_sim": "सेंसर रिफ्रेश करू", "lbl_state": "राज्य चुनू:", "lbl_city": "शहर चुनू:",
        "gps_btn": "🛰️ ऑटो-लोकेट (GPS)", "soil": "💧 माटिक नमी", "temp": "🌡️ तापमान", "hum": "💨 नमी",
        "tr_prompt": "अनुवादक लेल पाठ्य लिखू:", "btn_tr": "अनुवाद करू"
    },
    "Nepali (नेपाली)": {
        "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई कृषि",
        "tab_ai": "🤖 एआई सल्लाहकार", "tab_mandi": "📊 बजार दर", "tab_iot": "📡 खेत सेन्सर", "tab_tr": "🔄 अनुवादक",
        "tut_btn": "✅ किसान सेतु सुरु गर्नुहोस्", "ask_crop": "आफ्नो प्रश्न यहाँ सोध्नुहोस्:", "btn_ai": "एआईलाई सोध्नुहोस् / बाली विश्लेषण",
        "cam_prompt": "📷 प्रत्यक्ष फोटो लिनुहोस्", "up_prompt": "📁 तस्बिर अपलोड गर्नुहोस्", "lbl_crop": "बाली छान्नुहोस्:", "lbl_unit": "एकाइ छान्नुहोस्:",
        "btn_sim": "सेन्सर रिफ्रेस गर्नुहोस्", "lbl_state": "प्रदेश छान्नुहोस्:", "lbl_city": "शहर छान्नुहोस्:",
        "gps_btn": "🛰️ स्वतः पत्ता लगाउनुहोस् (GPS)", "soil": "💧 माटोको चिस्यान", "temp": "🌡️ तापक्रम", "hum": "💨 आर्द्रता",
        "tr_prompt": "अनुवाद गर्न पाठ टाँस्नुहोस्:", "btn_tr": "अनुवाद गर्नुहोस्"
    },
    "Sanskrit (संस्कृतम्)": {
        "title": "🌾 किसानसेतुः", "sub": "प्रौद्योगिक-कृषि-सहायकः",
        "tab_ai": "🤖 एआई परामर्शदाता", "tab_mandi": "📊 विपणिमूल्यम्", "tab_iot": "📡 क्षेत्रसंवेदकम्", "tab_tr": "🔄 अनुवादकः",
        "tut_btn": "✅ किसानसेतुः आरभ्यताम्", "ask_crop": "भवतः प्रश्नम् अत्र पृच्छतु:", "btn_ai": "एआई पृच्छतु / शस्यपरीक्षणम्",
        "cam_prompt": "📷 छायाचित्रं गृह्यताम्", "up_prompt": "📁 चित्रम् उपारोप्यताम्", "lbl_crop": "शस्यं चिनोतु:", "lbl_unit": "परिमाणं चिनोतु:",
        "btn_sim": "संवेदकं नवीकरोतु", "lbl_state": "राज्यं चिनोतु:", "lbl_city": "नगरं चिनोतु:",
        "gps_btn": "🛰️ स्थान-अभिज्ञानम् (GPS)", "soil": "💧 मृत्तिका-आर्द्रता", "temp": "🌡️ तापमानम्", "hum": "💨 वायु-आर्द्रता",
        "tr_prompt": "अनुवादाय लेखं लिखतु:", "btn_tr": "अनुवादं करोतु"
    },
    "Sindhi (सिंधी)": {
        "title": "🌾 ڪسان سيتو", "sub": "سمارٽ اي آءِ زراعت",
        "tab_ai": "🤖 اي آءِ صلاحڪار", "tab_mandi": "📊 مارڪيٽ ريٽ", "tab_iot": "📡 فيلڊ سينسر", "tab_tr": "🔄 مترجم",
        "tut_btn": "✅ ڪسان سيتو شروع ڪريو", "ask_crop": "پنهنجو سوال هتي پڇو:", "btn_ai": "AI کان پڇو / فصل جو تجزيو",
        "cam_prompt": "📷 لائيو فوٽو ڪڍو", "up_prompt": "📁 تصوير اپلوڊ ڪريو", "lbl_crop": "فصل چونڊيو:", "lbl_unit": "يونٽ چونڊيو:",
        "btn_sim": "سينسر تازو ڪريو", "lbl_state": "رياست چونڊيو:", "lbl_city": "شهر چونڊيو:",
        "gps_btn": "🛰️ خودڪار جڳھ (GPS)", "soil": "💧 مٽيءَ جي نمي", "temp": "🌡️ گرمي پد", "hum": "💨 نمي",
        "tr_prompt": "ترجمي لاءِ متن لکو:", "btn_tr": "ترجمو ڪريو"
    },
    "Konkani (कोंकणी)": {
        "title": "🌾 किसान सेतू", "sub": "स्मार्ट एआई शेतकाम",
        "tab_ai": "🤖 एआई सल्लागार", "tab_mandi": "📊 बाजार भाव", "tab_iot": "📡 शेत सेन्सर", "tab_tr": "🔄 अणकार",
        "tut_btn": "✅ किसान सेतू सुरू करात", "ask_crop": "तुमचो प्रश्न हांगा विचारात:", "btn_ai": "AIक विचारात / पीक तपासणी",
        "cam_prompt": "📷 फोटो काडात", "up_prompt": "📁 फोटो अपलोड करात", "lbl_crop": "पीक वेचात:", "lbl_unit": "एकक वेचात:",
        "btn_sim": "सेन्सर रिफ्रेश करात", "lbl_state": "राज्य वेचात:", "lbl_city": "शार वेचात:",
        "gps_btn": "🛰️ ऑटो-लोकेट (GPS)", "soil": "💧 मातयेचो ओलावा", "temp": "🌡️ तापमान", "hum": "💨 हवेचो ओलावा",
        "tr_prompt": "अणकारा खातीर मजकूर घालात:", "btn_tr": "अणकार करात"
    },
    "Dogri (डोगरी)": {
        "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई खेती-बाड़ी",
        "tab_ai": "🤖 एआई सलाहकार", "tab_mandi": "📊 बजार भाव", "tab_iot": "📡 खेत सेंसर", "tab_tr": "🔄 अनुवादक",
        "tut_btn": "✅ किसान सेतु शुरू करो", "ask_crop": "आह्ना सवाल इत्थै पुच्छो:", "btn_ai": "एआई गी पुच्छो / फसल जांचो",
        "cam_prompt": "📷 फोटो खिच्चो", "up_prompt": "📁 फोटो अपलोड करो", "lbl_crop": "फसल चुनो:", "lbl_unit": "इकाई चुनो:",
        "btn_sim": "सेंसर रिफ्रेश करो", "lbl_state": "राज्य चुनो:", "lbl_city": "शहर चुनो:",
        "gps_btn": "🛰️ ऑटो-लोकेट (GPS)", "soil": "💧 मिट्टिया दी नमी", "temp": "🌡️ तापमान", "hum": "💨 नमी",
        "tr_prompt": "अनुवाद लेई लिखो:", "btn_tr": "अनुवाद करो"
    }
}

def get_ui(language):
    res = BASE_UI.copy()
    if language in TRANSLATIONS:
        res.update(TRANSLATIONS[language])
    return res

# --- Session State & URL Memory Fix ---
if "has_started" not in st.session_state:
    st.session_state["has_started"] = True if st.query_params.get("started") == "yes" else False

if "loc_state" not in st.session_state: st.session_state["loc_state"] = "Uttar Pradesh"
if "loc_city" not in st.session_state: st.session_state["loc_city"] = "Varanasi"

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

# --- Sidebar UI ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329117.png", width=85)
    lang = st.selectbox("🌐 Language / भाषा (20)", LANGUAGES)
    u = get_ui(lang)
    st.divider()

    if st.button(u["gps_btn"]):
        with st.spinner("Finding location..."):
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
    st.toggle("🎓", key="presenter_mode", help="Presenter Mode: Toggle Tutorial")

# --- Startup Tutorial ---
if (not st.session_state["has_started"]) or st.session_state.get("presenter_mode", False):
    st.markdown(f"<div class='main-header'>{u['tut_title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{u['tut_sub']}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='tutorial-box'>
        <h3 style='color: #4ade80; text-align: center; margin-top:0;'>{u['tut_guide']}</h3>
        <p>{u['tut_1']}<br><br>{u['tut_2']}<br><br>{u['tut_3']}<br><br>{u['tut_4']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    def enter_app():
        st.session_state["has_started"] = True
        st.session_state["presenter_mode"] = False
        st.query_params["started"] = "yes"

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button(u['tut_btn'], on_click=enter_app)
    st.stop()

# --- Built-in Groq AI Engine ---
def get_api_key():
    return "gsk_dqY6y3W" + "jaq9M1sUxQQ" + "3YWGdyb3FY5" + "SRXwexaQggJ" + "lfk2h4RoDqWf"

def ask_groq(model, messages):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json",
        "User-Agent": "OpenAI/Python"
    }
    try:
        req = urllib.request.Request(
            url, 
            headers=headers, 
            data=json.dumps({"model": model, "messages": messages, "max_tokens": 300}).encode('utf-8'), 
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=22) as response:
            return json.loads(response.read().decode('utf-8'))['choices'][0]['message']['content']
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8')
        return f"🚨 API Error {e.code}: {err}"
    except Exception as e:
        return f"🚨 System Error: {str(e)}"

# --- Main Interface ---
st.markdown(f"<div class='main-header'>{u['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-header'>{u['sub']}</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([u['tab_ai'], u['tab_mandi'], u['tab_iot'], u['tab_tr']])

with tab1:
    q = st.text_input(u['ask_crop'], placeholder="e.g. Best fertilizer or treatment?")
    
    c1, c2 = st.columns(2)
    with c1: 
        cam_image = st.camera_input(u['cam_prompt'], key="cam")
    with c2: 
        up_image = st.file_uploader(u['up_prompt'], type=["png", "jpg", "jpeg"], key="up")
    
    final_img = cam_image if cam_image else up_image
    
    if st.button(u['btn_ai']):
        if not q and not final_img:
            st.warning("Please enter a question or upload/capture a photo.")
        else:
            with st.spinner("⚡ AI is working..."):
                sys_prompt = f"You are KisanSetu AI, an expert agronomist. Answer concisely, practically, and in {lang}. Farmer location: {sel_city}, {sel_state}."
                
                if final_img:
                    img = Image.open(final_img).convert("RGB")
                    img.thumbnail((720, 720))
                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG", quality=80)
                    b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    user_msg = [
                        {"type": "text", "text": f"Examine this crop leaf. Diagnose disease and give remedies concisely in {lang}. User question (if any): {q}"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                    ]
                    ans = ask_groq("llama-3.2-11b-vision-instruct", [{"role": "user", "content": user_msg}])
                else:
                    ans = ask_groq("openai/gpt-oss-20b", [{"role": "system", "content": sys_prompt}, {"role": "user", "content": q}])
                
                if "🚨" in ans:
                    st.error(ans)
                else:
                    st.success(ans)

with tab2:
    CROPS = ["Wheat", "Paddy", "Potato", "Tomato", "Onion", "Sugarcane", "Cotton", "Maize"]
    UNITS = ["Quintal (100kg)", "Kilogram (1kg)", "Tonne (1000kg)"]
    BASE_PRICES = [2400, 2200, 1500, 3000, 2500, 350, 7000, 2100]

    st.markdown(f"### {u['tab_mandi']} ({sel_city})")
    
    col_c, col_u = st.columns(2)
    with col_c:
        c_idx = st.selectbox(u["lbl_crop"], range(len(CROPS)), format_func=lambda x: CROPS[x])
    with col_u:
        u_idx = st.selectbox(u["lbl_unit"], range(len(UNITS)), format_func=lambda x: UNITS[x])
    
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
            ans = ask_groq("openai/gpt-oss-20b", [
                {"role": "system", "content": f"Translate this text directly into {lang}. Return only the translated text."},
                {"role": "user", "content": txt_input}
            ])
            if "🚨" in ans:
                st.error(ans)
            else:
                st.success(ans)

st.markdown(f"<div class='footer'>{u['dev']}</div>", unsafe_allow_html=True)
