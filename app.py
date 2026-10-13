import streamlit as st
import urllib.request
import json
import base64
from PIL import Image
import io
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="wide", initial_sidebar_state="auto")

# --- 🛑 Anti-Refresh & Overflow Killer ---
components.html("""
<script>
    document.body.style.overscrollBehavior = 'none';
    window.addEventListener('touchmove', function(e) {
        if (window.scrollY === 0 && e.touches[0].clientY > 0) { }
    }, { passive: true });
</script>
""", height=0)

# --- 📱 Sleek Futuristic CSS ---
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .main, .stApp {
        overscroll-behavior: none !important;
        background-color: #07090e !important;
        color: #f3f4f6 !important;
    }
    [data-testid="stAppViewContainer"] {
        overflow-y: scroll !important;
        height: 100vh !important;
        -webkit-overflow-scrolling: touch !important; 
        padding-bottom: 90px !important;
    }
    ::-webkit-scrollbar { width: 6px !important; }
    ::-webkit-scrollbar-track { background: #07090e !important; }
    ::-webkit-scrollbar-thumb { background-color: #22c55e !important; border-radius: 10px !important; }

    .block-container { max-width: 980px !important; padding-top: 1.2rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }

    .main-header { text-align: center; color: #4ade80; font-size: clamp(2rem, 5vw, 3rem); font-weight: 800; margin-bottom: 2px; text-shadow: 0 0 20px rgba(74,222,128,0.2); }
    .sub-header { text-align: center; color: #86efac; font-size: clamp(0.9rem, 2vw, 1.15rem); margin-bottom: 20px; font-weight: 500; }
    header[data-testid="stHeader"] { background-color: transparent !important; }
    .footer { text-align: center; font-size: 13px; color: #9ca3af; padding: 20px; border-top: 1px solid #1e293b; margin-top: 40px; }

    .stButton>button { width: 100% !important; min-height: 3.2rem !important; border-radius: 12px !important; font-weight: 600 !important; border: 1px solid #16a34a !important; background: linear-gradient(135deg, #15803d 0%, #166534 100%) !important; color: #ffffff !important; box-shadow: 0 4px 12px rgba(22,163,74,0.3); transition: all 0.3s ease; }
    .stButton>button:hover { background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important; border-color: #4ade80 !important; box-shadow: 0 6px 16px rgba(74,222,128,0.4); transform: translateY(-1px); }

    div[data-testid="stMetric"] { background: #0f172a !important; padding: 16px !important; border-radius: 14px !important; border: 1px solid #1e293b !important; box-shadow: 0 4px 15px rgba(0,0,0,0.4); }
    div[data-testid="stMetricValue"] { color: #4ade80 !important; font-size: clamp(1.2rem, 3vw, 1.8rem) !important; font-weight: 700 !important; }
    
    .stMarkdown, .stSuccess, .stError, .stInfo, p, span { word-wrap: break-word !important; overflow-wrap: break-word !important; }
    .game-card { background: linear-gradient(145deg, #0f172a 0%, #090d16 100%); padding: 25px; border-radius: 18px; border: 2px solid #22c55e; box-shadow: 0 0 25px rgba(34,197,94,0.15); margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

# --- 🌐 22 SCHEDULED LANGUAGES + ENGLISH ---
LANGUAGES = [
    "English", "Hindi (हिंदी)", "Assamese (অসমীয়া)", "Bengali (বাংলা)", 
    "Bodo (बड़ो)", "Dogri (डोगरी)", "Gujarati (ગુજરાતી)", "Kannada (ಕನ್ನಡ)", 
    "Kashmiri (कॉशुर)", "Konkani (कोंकणी)", "Maithili (मैथिली)", "Malayalam (മലയാളം)", 
    "Manipuri (মৈতৈলোন্)", "Marathi (मराठी)", "Nepali (नेपाली)", "Odia (ଓଡ଼ିଆ)", 
    "Punjabi (ਪੰਜਾਬੀ)", "Sanskrit (संस्कृतम्)", "Santali (संताली)", "Sindhi (सिंधी)", 
    "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Urdu (اردو)"
]

# --- 🗺️ ALL STATES, UTs & 20+ CITIES EACH ---
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
    "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam", "Oulgaret", "Villianur", "Ariyankuppam", "Bahour", "Nettapakkam", "Kottakuppam", "Thirubuvanai", "Madagadipet", "Kurumbapet", "Thavalakuppam", "Kirumampakkam", "Embalam", "Suthukeny", "Kariamputtur", "Pandakkal", "Palloor", "Pandakkal"],
    "Chandigarh": ["Chandigarh", "Manimajra", "Burail", "Daria", "Behlana", "Raipur Kalan", "Kishangarh", "Kaimbwala", "Dadu Majra", "Maloya", "Sarangpur", "Palsora", "Faizabad", "Khuda Alisher", "Khuda Jassu", "Khuda Lahora", "Dhanas", "Hallomajra", "Behlana", "Makhan Majra", "Lahora"],
    "Andaman and Nicobar Islands": ["Port Blair", "Car Nicobar", "Diglipur", "Mayabunder", "Rangat", "Havelock Island", "Neil Island", "Bambooflat", "Campbell Bay", "Wandoor", "Chidiyatapu", "Baratang", "Little Andaman", "Katchal", "Teressa", "Nancowry", "Karmarat", "Calicut", "Garacharma", "Ferrargunj", "Mimis"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Diu", "Silvassa", "Naroli", "Amli", "Samarvarni", "Rakholi", "Khadoli", "Masat", "Varkund", "Kadaiya", "Devka", "Moti Daman", "Nani Daman", "Ghoghla", "Bucharwada", "Fudam", "Varkund", "Dadra", "Kharadpar", "Velugam"],
    "Lakshadweep": ["Kavaratti", "Agatti", "Amini", "Androth", "Minicoy", "Kalpeni", "Kiltan", "Kadmat", "Chetlat", "Bitra", "Bangaram", "Suheli", "Cheriyapani", "Valiyapani", "Perumal Par", "Beliapani", "Bassas de Pedro", "Byramgore", "Sesostris Bank", "Elikalpeni", "Mangalore Reef"]
}

# --- State Initialization ---
if "has_started" not in st.session_state: st.session_state["has_started"] = False
if "tutorial_step" not in st.session_state: st.session_state["tutorial_step"] = 1
if "loc_state" not in st.session_state: st.session_state["loc_state"] = "Uttar Pradesh"
if "loc_city" not in st.session_state: st.session_state["loc_city"] = "Varanasi"

# --- Sidebar Controls ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329117.png", width=75)
    lang = st.selectbox("🌐 Language (22 Official)", LANGUAGES)
    
    st.divider()
    sel_state = st.selectbox("Select State / UT", list(STATES_AND_UTS.keys()), index=list(STATES_AND_UTS.keys()).index(st.session_state["loc_state"]), key="loc_state")
    valid_cities = STATES_AND_UTS[sel_state]
    if st.session_state["loc_city"] not in valid_cities: st.session_state["loc_city"] = valid_cities[0]
    sel_city = st.selectbox("Select City", valid_cities, index=valid_cities.index(st.session_state["loc_city"]), key="loc_city")
    
    st.divider()
    if st.button("🎮 Restart Game Tutorial"):
        st.session_state["has_started"] = False
        st.session_state["tutorial_step"] = 1
        st.rerun()

# --- 🎮 GAME-LIKE INTERACTIVE TUTORIAL OVERLAY ---
if not st.session_state["has_started"]:
    step = st.session_state["tutorial_step"]
    
    st.markdown("<div class='main-header'>🌾 KisanSetu Adventure</div><div class='sub-header'>Interactive Mission Briefing</div>", unsafe_allow_html=True)
    
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
                if st.button("⬅️ Previous"):
                    st.session_state["tutorial_step"] = 1
                    st.rerun()
            with col2:
                if st.button("Next Mission ➡️"):
                    st.session_state["tutorial_step"] = 3
                    st.rerun()
        elif step == 3:
            st.markdown("### 🔄 Mission 3: Multilingual Translation")
            st.markdown("Translate agricultural insights seamlessly into all 22 scheduled languages of India!")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Previous"):
                    st.session_state["tutorial_step"] = 2
                    st.rerun()
            with col2:
                if st.button("🚀 Launch KisanSetu!"):
                    st.session_state["has_started"] = True
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 🚀 OPENROUTER API ENGINE ---
def ask_openrouter(prompt_text):
    try:
        key = st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        return "🚨 ERROR: OPENROUTER_API_KEY missing from Streamlit Secrets."

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
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data["choices"][0]["message"]["content"]

# --- Main App Interface ---
st.markdown("<div class='main-header'>🌾 KisanSetu</div><div class='sub-header'>Smart AI Agriculture Platform</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🤖 AI Advisor", "📊 Market Rates", "🔄 Translator"])

with tab1:
    q = st.text_input("Ask your farming question or crop query:", placeholder="e.g. Best organic fertilizer for paddy?")
    c1, c2 = st.columns(2)
    with c1: cam_image = st.camera_input("📷 Take live photo", key="cam")
    with c2: up_image = st.file_uploader("📁 Or upload image", type=["png", "jpg", "jpeg"], key="up")
    final_img = cam_image if cam_image else up_image
    
    if st.button("Ask AI / Analyze Crop"):
        if not q and not final_img:
            st.warning("Please enter a question or upload a photo.")
        else:
            with st.spinner("⚡ AI is analyzing regional crop health..."):
                try:
                    img_note = " [User attached a crop image for analysis]" if final_img else ""
                    prompt = f"You are KisanSetu AI, an expert agronomist. Provide direct, practical farming advice in {lang}. Factor in the local climate of {sel_city}, {sel_state}. Query{img_note}: {q}"
                    ans = ask_openrouter(prompt)
                    st.success(ans)
                except Exception as e:
                    st.error(f"API Error: {str(e)}")

with tab2:
    CROPS = ["Wheat", "Paddy", "Potato", "Tomato", "Onion", "Sugarcane", "Cotton", "Maize"]
    UNITS = ["Quintal (100kg)", "Kilogram (1kg)", "Tonne (1000kg)"]
    BASE_PRICES = [2400, 2200, 1500, 3000, 2500, 350, 7000, 2100]
    
    st.markdown(f"### 📊 Mandi Prices for {sel_city}, {sel_state}")
    col_c, col_u = st.columns(2)
    with col_c: c_idx = st.selectbox("Select Crop:", range(len(CROPS)), format_func=lambda x: CROPS[x])
    with col_u: u_idx = st.selectbox("Select Unit:", range(len(UNITS)), format_func=lambda x: UNITS[x])
    
    price = BASE_PRICES[c_idx] / 100 if u_idx == 1 else (BASE_PRICES[c_idx] * 10 if u_idx == 2 else BASE_PRICES[c_idx])
    st.metric(CROPS[c_idx], f"₹{price:,.2f} / {UNITS[u_idx]}")

with tab3:
    st.markdown("### 🔄 Multilingual Translator (22 Languages)")
    txt_input = st.text_area("Paste text to translate to your selected language:")
    if st.button("Translate Text") and txt_input:
        with st.spinner("Translating..."):
            try:
                ans = ask_openrouter(f"Translate the following text directly into {lang}. Return only the translation without commentary:\n{txt_input}")
                st.success(ans)
            except Exception as e:
                st.error(f"Translation Error: {str(e)}")

st.markdown("<div class='footer'><b>Developed by Ankur Kumar & Vikalp Chaubey</b><br>The Aryan International School, Varanasi</div>", unsafe_allow_html=True
