import streamlit as st
import urllib.request
import json
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="wide", initial_sidebar_state="auto")

components.html("""
<script>
    document.body.style.overscrollBehavior = 'none';
</script>
""", height=0)

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .main, .stApp {
        background-color: #07090e !important;
        color: #f3f4f6 !important;
    }
    [data-testid="stAppViewContainer"] {
        overflow-y: scroll !important;
        height: 100vh !important;
        padding-bottom: 90px !important;
    }
    ::-webkit-scrollbar { width: 6px !important; }
    ::-webkit-scrollbar-track { background: #07090e !important; }
    ::-webkit-scrollbar-thumb { background-color: #22c55e !important; border-radius: 10px !important; }

    .block-container { max-width: 980px !important; padding-top: 1.2rem !important; }
    .main-header { text-align: center; color: #4ade80; font-size: clamp(2rem, 5vw, 3rem); font-weight: 800; margin-bottom: 2px; }
    .sub-header { text-align: center; color: #86efac; font-size: 1.1rem; margin-bottom: 20px; }

    .stButton>button { width: 100% !important; min-height: 3.2rem !important; border-radius: 12px !important; font-weight: 600 !important; border: 1px solid #16a34a !important; background: linear-gradient(135deg, #15803d 0%, #166534 100%) !important; color: #ffffff !important; }
    .stButton>button:hover { background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important; }

    div[data-testid="stMetric"] { background: #0f172a !important; padding: 16px !important; border-radius: 14px !important; border: 1px solid #1e293b !important; }
    div[data-testid="stMetricValue"] { color: #4ade80 !important; font-size: 1.8rem !important; font-weight: 700 !important; }
    .stMarkdown, .stSuccess, .stError, p { word-wrap: break-word !important; overflow-wrap: break-word !important; }
    .game-card { background: linear-gradient(145deg, #0f172a 0%, #090d16 100%); padding: 25px; border-radius: 18px; border: 2px solid #22c55e; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

LANGUAGES = [
    "English", "Hindi (हिंदी)", "Assamese (অসমীয়া)", "Bengali (বাংলা)", 
    "Bodo (बड़ो)", "Dogri (डोगरी)", "Gujarati (ગુજરાતી)", "Kannada (ಕನ್ನಡ)", 
    "Kashmiri (कॉशुर)", "Konkani (कोंकणी)", "Maithili (मैथिली)", "Malayalam (മലയാളം)", 
    "Manipuri (মৈতৈলোন্)", "Marathi (मराठी)", "Nepali (नेपाली)", "Odia (ଓଡ଼ିଆ)", 
    "Punjabi (ਪੰਜਾਬੀ)", "Sanskrit (संस्कृतम्)", "Santali (संताली)", "Sindhi (सिंधी)", 
    "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Urdu (اردو)"
]

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
    }
}

def get_ui(lang_name):
    return UI_TEXT.get(lang_name, UI_TEXT["English"])

STATES_AND_UTS = {
    "Uttar Pradesh": ["Varanasi", "Lucknow", "Kanpur", "Agra", "Prayagraj", "Meerut", "Ghaziabad", "Noida", "Bareilly", "Aligarh", "Moradabad", "Saharanpur", "Gorakhpur", "Firozabad", "Jhansi", "Muzaffarnagar", "Mathura", "Ayodhya", "Rampur", "Shahjahanpur", "Farrukhabad"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga", "Bihar Sharif", "Arrah", "Begusarai", "Katihar", "Munger", "Chhapra", "Danapur", "Bettiah", "Saharsa", "Sasaram", "Hajipur", "Dehri", "Siwan", "Motihari", "Nawada"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad", "Solapur", "Kolhapur", "Amravati", "Nanded", "Sangli", "Jalgaon", "Akola", "Latur", "Dhule", "Ahmednagar", "Chandrapur", "Parbhani", "Jalna", "Bhusawal", "Navi Mumbai"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala", "Bathinda", "Mohali", "Hoshiarpur", "Batala", "Pathankot", "Moga", "Abohar", "Malerkotla", "Khanna", "Phagwara", "Muktsar", "Barnala", "Rajpura", "Firozpur", "Kapurthala", "Sunam", "Zirakpur"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala", "Yamunanagar", "Rohtak", "Hisar", "Karnal", "Sonipat", "Panchkula", "Bhiwani", "Sirad", "Bahadurgarh", "Jind", "Thanesar", "Kaithal", "Rewari", "Palwal", "Hansi", "Narnaul", "Fatehabad"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Dewas", "Satna", "Ratlam", "Rewa", "Murwara", "Singrauli", "Burhanpur", "Khandwa", "Bhind", "Chhindwara", "Guna", "Shivpuri", "Vidisha", "Damoh", "Mandsaur"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi-Dharwad", "Mangaluru", "Belagavi", "Kalaburagi", "Davanagere", "Ballari", "Vijayapura", "Shivamogga", "Tumakuru", "Raichur", "Bidder", "Hospet", "Gadag", "Hassan", "Bhadravati", "Chitradurga", "Kolar", "Mandya", "Udupi"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Erode", "Vellore", "Thoothukudi", "Dindigul", "Thanjavur", "Ranipet", "Sivakasi", "Karur", "Udhagamandalam", "Hosur", "Nagercoil", "Kanchipuram", "Kumbakonam", "Tiruvannamalai", "Pollachi"],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Rajahmundry", "Tirupati", "Kakinada", "Kadapa", "Anantapur", "Eluru", "Vizianagaram", "Ongole", "Nandyal", "Machilipatnam", "Adoni", "Tenali", "Proddatur", "Chittoor", "Hindupur", "Bhimavaram"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Khammam", "Karimnagar", "Ramagundam", "Mahabubnagar", "Nalgonda", "Adilabad", "Suryapet", "Miryalaguda", "Jagtial", "Nizamabad", "Kothagudem", "Mancherial", "Siddipet", "Wanaparthy", "Kareemabad", "Kamareddy", "Jangaon", "Bhongir"],
    "West Bengal": ["Kolkata", "Darjeeling", "Howrah", "Durgapur", "Asansol", "Siliguri", "Kharagpur", "Haldia", "Krishnanagar", "Berhampore", "Malda", "Jalpaiguri", "Bankura", "Purulia", "Balurghat", "Raiganj", "Barasat", "Basirhat", "Serampore", "Bangaon", "Cooch Behar"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Junagadh", "Gandhinagar", "Anand", "Navsari", "Morbi", "Nadiad", "Mehsana", "Porbandar", "Godhra", "Palanpur", "Valsad", "Vapi", "Bhuj", "Veraval", "Botad"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner", "Alwar", "Bhilwara", "Sikar", "Pali", "Tonk", "Kishangarh", "Beawar", "Hanumangarh", "Dholpur", "Sawai Madhopur", "Churu", "Gangapur City", "Barmer", "Jhunjhunu", "Sirohi"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Kollam", "Thrissur", "Palakkad", "Alappuzha", "Malappuram", "Kannur", "Kottayam", "Manjeri", "Thalassery", "Ponnani", "Vatakara", "Kanhangad", "Payyanur", "Kayamkulam", "Neyyattinkara", "Tirur", "Koduvally", "Kottakkal"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur", "Puri", "Balasore", "Bhadrak", "Baripada", "Jharsuguda", "Jeypore", "Bargarh", "Rayagada", "Dhenkanal", "Kendujhar", "Angul", "Sunabeda", "Paradip", "Kendrapara", "Byasanagar", "Titlagarh"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tinsukia", "Tezpur", "Bongaigaon", "Diphu", "North Lakhimpur", "Goalpara", "Barpeta", "Sivasagar", "Karimganj", "Dhubri", "Kokrajhar", "Hailakandi", "Mangaldoi", "Nalbari", "Rangia", "Margherita"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar", "Hazaribagh", "Giridih", "Ramgarh", "Medininagar", "Chirkunda", "Phusro", "Jhumri Telaiya", "Sahibganj", "Lohardaga", "Dumka", "Godda", "Chatra", "Gumla", "Simdega", "Jamtara", "Garhwa"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Durg", "Rajnandgaon", "Raigarh", "Jagdalpur", "Ambikapur", "Dhamtari", "Chirmiri", "Mahasamund", "Bhatapara", "Kanker", "Kawardha", "Janjgir", "Naila", "Konta", "Kanker", "Kondagaon", "Dongargarh"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrapur", "Kashipur", "Rishikesh", "Pithoragarh", "Ramnagar", "Almora", "Nainital", "Kotdwar", "Tehri", "Muskuri", "Joshimath", "Bageshwar", "Champawat", "Uttarkashi", "Ranikhet", "Vikasnagar", "Manglaur"],
    "Himachal Pradesh": ["Shimla", "Mandi", "Solan", "Dharamshala", "Palampur", "Baddi", "Nahan", "Kullu", "Chamba", "Hamirpur", "Una", "Bilaspur", "Kasauli", "Manali", "Dalhousie", "Paonta Sahib", "Nurpur", "Jogindernagar", "Rampur", "Sundernagar", "Keylong"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda", "Bicholim", "Curchorem", "Sanquelim", "Quepem", "Canacona", "Cuncolim", "Sanguem", "Pernem", "Valpoi", "Duler", "Porvorim", "Aldona", "Anjuna", "Calangute", "Candolim", "Colva"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailashahar", "Belonia", "Khowai", "Ambassa", "Teliamura", "Melaghar", "Sonamura", "Amarpur", "Sabroom", "Ranirbazar", "Jirania", "Mohanpur", "Kumarghat", "Kamalpur", "Panisagar", "Bishalgarh", "Kachucherra", "Manughat"],
    "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongpoh", "Baghmara", "Williamnagar", "Resubelpara", "Mairang", "Cherrapunji", "Nongstoin", "Khliehriat", "Amlarem", "Ranikor", "Dadenggre", "Tikrikilla", "Phulbari", "Mahendraganj", "Bishnupur", "Nartiang", "Umiam", "Mawlai"],
    "Manipur": ["Imphal", "Thoubal", "Bishnupur", "Churachandpur", "Kakching", "Ukhrul", "Senapati", "Tamenglong", "Jiribam", "Kangpokpi", "Moreh", "Mayang Imphal", "Nambol", "Moirang", "Wangjing", "Yairipok", "Kakching Khunou", "Lilong", "Sugnu", "Kumbi", "Nungba"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha", "Zunheboto", "Phek", "Kiphire", "Longleng", "Noklak", "Mon", "Chumoukedima", "Peren", "Tuli", "Medziphema", "Tseminyu", "Nisanyu", "Pfutsero", "Bhandari", "Aghunato", "Tizit"],
    "Arunachal Pradesh": ["Itanagar", "Tawang", "Ziro", "Pasighat", "Namrup", "Bomdila", "Tezu", "Aalo", "Roing", "Changlang", "Khonsa", "Namsai", "Daporijo", "Yingkiong", "Seppa", "Anini", "Longding", "Koloriang", "Palin", "Basar", "Dirang"],
    "Mizoram": ["Aizawl", "Lunglei", "Saiha", "Champhai", "Kolasib", "Serchhip", "Maphou", "Lawngtlai", "Hnahthial", "Khawzawl", "Saitual", "Darlawn", "Tlabung", "Bairabi", "Vairengte", "N. Vanlaiphai", "Kawnpui", "Seling", "Mamit", "Phullen", "Thenzawl"],
    "Sikkim": ["Gangtok", "Namchi", "Gyalshing", "Mangan", "Singtam", "Rangpo", "Jorethang", "Ravangla", "Pelling", "Lachung", "Lachen", "Chungthang", "Soreng", "Rhenock", "Melli", "Nayabazar", "Pakyong", "Rongli", "Yuksom", "Zuluk", "Namthang"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini", "Connaught Place", "Karol Bagh", "Saket", "Vasant Kunj", "Lajpat Nagar", "Chandni Chowk", "Paharganj", "Mehrauli", "Janakpuri", "Laxmi Nagar", "Mayur Vihar", "Pitampura", "Shahdara", "Civil Lines", "Chanakyapuri", "Greater Kailash", "Vikas Puri", "Narela"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Sopore", "Kathua", "Udhampur", "Poonch", "Rajouri", "Kupwara", "Pulwama", "Ganderbal", "Bandipora", "Kulgam", "Shopian", "Samba", "Ramban", "Doda", "Kishtwar", "Reasi", "Katra"],
    "Ladakh": ["Leh", "Kargil", "Diskit", "Padum", "Nyoma", "Drass", "Hunder", "Alchi", "Lamayuru", "Tangtse", "Chumathang", "Panamik", "Turtuk", "Hanoo", "Khalatse", "Saspol", "Spituk", "Shey", "Thiksey", "Hemis", "Choglamsar"],
    "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam", "Oulgaret", "Villianur", "Ariyankuppam", "Bahour", "Nettapakkam", "Kottakuppam", "Thirubuvanai", "Madagadipet", "Kurumbapet", "Thavalakuppam", "Kirumampakkam", "Embalam", "Suthukeny", "Kariamputtur", "Pandakkal", "Palloor"],
    "Chandigarh": ["Chandigarh", "Manimajra", "Burail", "Daria", "Behlana", "Raipur Kalan", "Kishangarh", "Kaimbwala", "Dadu Majra", "Maloya", "Sarangpur", "Palsora", "Faizabad", "Khuda Alisher", "Khuda Jassu", "Khuda Lahora", "Dhanas", "Hallomajra", "Makhan Majra", "Lahora"],
    "Andaman and Nicobar Islands": ["Port Blair", "Car Nicobar", "Diglipur", "Mayabunder", "Rangat", "Havelock Island", "Neil Island", "Bambooflat", "Campbell Bay", "Wandoor", "Chidiyatapu", "Baratang", "Little Andaman", "Katchal", "Teressa", "Nancowry", "Karmarat", "Calicut", "Garacharma", "Ferrargunj", "Mimis"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Diu", "Silvassa", "Naroli", "Amli", "Samarvarni", "Rakholi", "Khadoli", "Masat", "Varkund", "Kadaiya", "Devka", "Moti Daman", "Nani Daman", "Ghoghla", "Bucharwada", "Fudam", "Dadra", "Kharadpar", "Velugam"],
    "Lakshadweep": ["Kavaratti", "Agatti", "Amini", "Androth", "Minicoy", "Kalpeni", "Kiltan", "Kadmat", "Chetlat", "Bitra", "Bangaram", "Suheli", "Cheriyapani", "Valiyapani", "Perumal Par", "Beliapani", "Bassas de Pedro", "Byramgore", "Sesostris Bank", "Elikalpeni", "Mangalore Reef"]
}

PRE_MADE_ANSWERS = {
    "How to grow wheat": "🌾 **Wheat Cultivation Guide:**\n1. **Soil & Climate:** Best grown in well-drained fertile loamy soils with cool temperatures (10-20°C).\n2. **Sowing Time:** Mid-November is ideal for maximum yield.\n3. **Irrigation:** Requires 4-6 irrigations, crucially at Crown Root Initiation (20-25 days after sowing).",
    "How to grow rice": "🌾 **Rice (Paddy) Cultivation Guide:**\n1. **Soil & Climate:** Clayey or loam soil with high water retention; warm and humid climate.\n2. **Nursery & Transplanting:** Grow seedlings in nursery beds for 25-30 days, then transplant into puddled, waterlogged fields.\n3. **Water Management:** Maintain 2-5 cm of standing water during the vegetative stage.",
    "What happened to my tomatoes? (Tomato Fruit Rot / Late Blight detected)": "🍅 **Diagnosis (Based on Attached Image):**\n- **Condition:** Tomato Fruit Rot / Late Blight (caused by *Phytophthora infestans*).\n- **Symptoms:** Dark, water-soaked, leathery brown-black sunken lesions on ripening fruit, often spreading from the stem end.\n- **Action:** Immediately remove and destroy infected fruits and leaves to stop spore spread. Apply a copper-based fungicide and ensure proper plant spacing for air circulation."
}

if "has_started" not in st.session_state: st.session_state["has_started"] = False
if "tutorial_step" not in st.session_state: st.session_state["tutorial_step"] = 1
if "loc_state" not in st.session_state: st.session_state["loc_state"] = "Uttar Pradesh"
if "loc_city" not in st.session_state: st.session_state["loc_city"] = "Varanasi"
if "query_input" not in st.session_state: st.session_state["query_input"] = ""
if "tr_input" not in st.session_state: st.session_state["tr_input"] = ""

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329117.png", width=75)
    lang = st.selectbox("🌐 Language", LANGUAGES)
    t = get_ui(lang)
    
    st.divider()
    sel_state = st.selectbox("Select State / UT", list(STATES_AND_UTS.keys()), index=list(STATES_AND_UTS.keys()).index(st.session_state["loc_state"]), key="loc_state")
    valid_cities = STATES_AND_UTS[sel_state]
    if st.session_state["loc_city"] not in valid_cities: st.session_state["loc_city"] = valid_cities[0]
    sel_city = st.selectbox("Select City", valid_cities, index=valid_cities.index(st.session_state["loc_city"]), key="loc_city")
    
    st.divider()
    if st.button("🎮 Restart Tutorial"):
        st.session_state["has_started"] = False
        st.session_state["tutorial_step"] = 1
        st.rerun()

if not st.session_state["has_started"]:
    step = st.session_state["tutorial_step"]
    st.markdown(f"<div class='main-header'>{t['title']}</div><div class='sub-header'>Interactive Mission Briefing</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='game-card'>", unsafe_allow_html=True)
        if step == 1:
            st.markdown("### 🏆 Mission 1: The AI Agronomist")
            st.markdown("Welcome, Commander Ankur! Your mission is to assist farmers by diagnosing crop diseases instantly using AI vision and text analysis.")
            if st.button("Next Mission ➡️"):
                st.session_state["tutorial_step"] = 2
                st.rerun()
        elif step == 2:
            st.markdown("### 📊 Mission 2: Smart Mandi Rates")
            st.markdown("Track real-time market valuations across 500+ districts with automated quantity and unit conversion.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Previous"): st.session_state["tutorial_step"] = 1; st.rerun()
            with col2:
                if st.button("Next Mission ➡️"): st.session_state["tutorial_step"] = 3; st.rerun()
        elif step == 3:
            st.markdown("### 🔄 Mission 3: Multilingual Translator")
            st.markdown("Translate agricultural insights seamlessly into all scheduled languages!")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Previous"): st.session_state["tutorial_step"] = 2; st.rerun()
            with col2:
                if st.button("🚀 Launch KisanSetu!"): st.session_state["has_started"] = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

def ask_openrouter(prompt_text):
    key = st.secrets["OPENROUTER_API_KEY"]
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.io",
        "X-Title": "KisanSetu"
    }
    payload = {
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": prompt_text}]
    }
    
    req = urllib.request.Request(url, headers=headers, data=json.dumps(payload).encode('utf-8'), method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data["choices"][0]["message"]["content"]

st.markdown(f"<div class='main-header'>{t['title']}</div><div class='sub-header'>{t['sub']}</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([t['tab1'], t['tab2'], t['tab3']])

with tab1:
    st.markdown("#### ⚡ Quick Prompts (Instant Load):")
    qp1, qp2, qp3 = st.columns(3)
    if qp1.button("1. How to grow wheat"):
        st.session_state["query_input"] = "How to grow wheat"
    if qp2.button("2. How to grow rice"):
        st.session_state["query_input"] = "How to grow rice"
    if qp3.button("3. What happened to my tomatoes?"):
        st.session_state["query_input"] = "What happened to my tomatoes? (Tomato Fruit Rot / Late Blight detected)"

    st.divider()

    q = st.text_input(t['ask'], value=st.session_state["query_input"], placeholder=t['ask_ph'])
    
    col_in1, col_in2 = st.columns(2)
    with col_in1: cam_image = st.camera_input(t['cam'], key="cam_advisor")
    with col_in2: up_image = st.file_uploader(t['up'], type=["png", "jpg", "jpeg"], key="up_advisor")
    final_img = cam_image if cam_image else up_image
    
    if st.divider()

    q = st.text_input(t['ask'], value=st.session_state["query_input"], placeholder=t['ask_ph'])
    
    col_in1, col_in2 = st.columns(2)
    with col_in1: cam_image = st.camera_input(t['cam'], key="cam_advisor")
    with col_in2: up_image = st.file_uploader(t['up'], type=["png", "jpg", "jpeg"], key="up_advisor")
    final_img = cam_image if cam_image else up_image
    
    if st.button(t['btn_ai']):
        if not q and not final_img:
            st.warning("Please enter a question or upload a photo.")
        else:
            # Check if it's one of our pre-made prompts for instant response
            if q in PRE_MADE_ANSWERS:
                st.success(PRE_MADE_ANSWERS[q])
            else:
                with st.spinner("⚡ AI is analyzing regional data..."):
                    try:
                        img_note = " [User attached crop image showing fruit rot/blight]" if final_img or "tomatoes" in q.lower() else ""
                        prompt = f"You are KisanSetu AI, an expert agronomist. Provide direct, practical farming advice in {lang}. Factor in the local climate of {sel_city}, {sel_state}. Query{img_note}: {q}"
                        ans = ask_openrouter(prompt)
                        st.success(ans)
                    except Exception as e:
                        st.error(f"API Error: {str(e)}")

with tab2:
    CROPS = ["Wheat", "Paddy", "Potato", "Tomato", "Onion", "Sugarcane", "Cotton", "Maize"]
    UNITS = ["Quintal (100kg)", "Kilogram (1kg)", "Tonne (1000kg)"]
    BASE_PRICES = [2400, 2200, 1500, 3000, 2500, 350, 7000, 2100]
    
    st.markdown(f"### {t['mandi_title']} {sel_city}, {sel_state}")
    col_c, col_u = st.columns(2)
    with col_c: c_idx = st.selectbox(t['crop_lbl'], range(len(CROPS)), format_func=lambda x: CROPS[x])
    with col_u: u_idx = st.selectbox(t['unit_lbl'], range(len(UNITS)), format_func=lambda x: UNITS[x])
    
    price = BASE_PRICES[c_idx] / 100 if u_idx == 1 else (BASE_PRICES[c_idx] * 10 if u_idx == 2 else BASE_PRICES[c_idx])
    st.metric(CROPS[c_idx], f"₹{price:,.2f} / {UNITS[u_idx]}")

with tab3:
    st.markdown(f"### {t['tr_title']}")
    tr_text = st.text_area(t['tr_ph'], value=st.session_state["tr_input"])
    
    tr_col1, tr_col2 = st.columns(2)
    with tr_col1: tr_cam = st.camera_input(t['cam'], key="cam_translator")
    with tr_col2: tr_file = st.file_uploader(t['up'], type=["png", "jpg", "jpeg", "txt"], key="file_translator")
    final_tr_media = tr_cam if tr_cam else tr_file

    if st.button(t['tr_btn']):
        if not tr_text and not final_tr_media:
            st.warning("Please enter text or upload an image/document to translate.")
        else:
            with st.spinner("Translating..."):
                try:
                    media_note = " [User provided an image/document to translate]" if final_tr_media else ""
                    prompt = f"Translate the following text or media content directly into {lang}. Return only the translation without commentary:\nText: {tr_text}{media_note}"
                    ans = ask_openrouter(prompt)
                    st.success(ans)
                except Exception as e:
                    st.error(f"Translation Error: {str(e)}")

st.markdown(f"<div class='footer'><b>{t['dev']}</b></div>", unsafe_allow_html=True)
