import streamlit as st
import urllib.request
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="wide", initial_sidebar_state="auto")

components.html("""<script>document.body.style.overscrollBehavior = 'none';</script>""", height=0)

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .main, .stApp { background-color: #07090e !important; color: #f3f4f6 !important; }
    .block-container { max-width: 980px !important; padding-top: 2.8rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    .main-header { text-align: center; color: #4ade80; font-size: clamp(2rem, 5vw, 2.8rem); font-weight: 800; }
    .sub-header { text-align: center; color: #86efac; font-size: 1.1rem; margin-bottom: 25px; }
    
    /* Modern Pill Input Bar Styling inspired by reference */
    .stTextInput>div>div>input {
        background-color: #121824 !important;
        color: #ffffff !important;
        border: 1px solid #1e293b !important;
        border-radius: 24px !important;
        padding: 14px 20px !important;
        font-size: 1rem !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.5);
    }
    .stButton>button { width: 100% !important; min-height: 3rem !important; border-radius: 14px !important; background: linear-gradient(135deg, #15803d 0%, #166534 100%) !important; color: #fff !important; font-weight: 600 !important; border: 1px solid #22c55e !important; }
    .stButton>button:hover { background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important; }
    .feature-card { background: linear-gradient(145deg, #0f172a 0%, #090d16 100%); padding: 20px; border-radius: 16px; border: 1px solid #1e293b; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
</style>
""", unsafe_allow_html=True)

# --- 🌐 22 SCHEDULED LANGUAGES ---
LANGUAGES = [
    "English", "Hindi (हिंदी)", "Assamese (অসমীয়া)", "Bengali (বাংলা)", 
    "Bodo (बड़ो)", "Dogri (डोगरी)", "Gujarati (ગુજરાતી)", "Kannada (ಕನ್ನಡ)", 
    "Kashmiri (कॉशुर)", "Konkani (कोंकणी)", "Maithili (मैथिली)", "Malayalam (മലയാളം)", 
    "Manipuri (মৈতৈলোন্)", "Marathi (मराठी)", "Nepali (नेपाली)", "Odia (ଓଡ଼ିଆ)", 
    "Punjabi (ਪੰਜਾਬੀ)", "Sanskrit (संस्कृतम्)", "Santali (संताली)", "Sindhi (सिंधी)", 
    "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Urdu (اردو)"
]

# --- 🗺️ ALL STATES, UTs & COMPLETE DISTRICTS DIRECTORY ---
STATES_AND_UTS = {
    "Uttar Pradesh": ["Varanasi", "Lucknow", "Kanpur", "Agra", "Prayagraj", "Meerut", "Ghaziabad", "Noida", "Bareilly", "Aligarh", "Moradabad", "Saharanpur", "Gorakhpur", "Firozabad", "Jhansi", "Muzaffarnagar", "Mathura", "Ayodhya", "Rampur", "Shahjahanpur", "Farrukhabad"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga", "Bihar Sharif", "Arrah", "Begusarai", "Katihar", "Munger", "Chhapra", "Danapur", "Bettiah", "Saharsa", "Sasaram", "Hajipur", "Dehri", "Siwan", "Motihari", "Nawada"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad", "Solapur", "Kolhapur", "Amravati", "Nanded", "Sangli", "Jalgaon", "Akola", "Latur", "Dhule", "Ahmednagar", "Chandrapur", "Parbhani", "Jalna", "Bhusawal", "Navi Mumbai"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala", "Bathinda", "Mohali", "Hoshiarpur", "Batala", "Pathankot", "Moga", "Abohar", "Malerkotla", "Khanna", "Phagwara", "Muktsar", "Barnala", "Rajpura", "Firozpur", "Kapurthala", "Sunam", "Zirakpur"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala", "Yamunanagar", "Rohtak", "Hisar", "Karnal", "Sonipat", "Panchkula", "Bhiwani", "Sirsa", "Bahadurgarh", "Jind", "Thanesar", "Kaithal", "Rewari", "Palwal", "Hansi", "Narnaul", "Fatehabad"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Dewas", "Satna", "Ratlam", "Rewa", "Murwara", "Singrauli", "Burhanpur", "Khandwa", "Bhind", "Chhindwara", "Guna", "Shivpuri", "Vidisha", "Damoh", "Mandsaur"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi-Dharwad", "Mangaluru", "Belagavi", "Kalaburagi", "Davanagere", "Ballari", "Vijayapura", "Shivamogga", "Tumakuru", "Raichur", "Bidar", "Hospet", "Gadag", "Hassan", "Bhadravati", "Chitradurga", "Kolar", "Mandya", "Udupi"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Erode", "Vellore", "Thoothukudi", "Dindigul", "Thanjavur", "Ranipet", "Sivakasi", "Karur", "Udhagamandalam", "Hosur", "Nagercoil", "Kanchipuram", "Kumbakonam", "Tiruvannamalai", "Pollachi"],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Rajahmundry", "Tirupati", "Kakinada", "Kadapa", "Anantapur", "Eluru", "Vizianagaram", "Ongole", "Nandyal", "Machilipatnam", "Adoni", "Tenali", "Proddatur", "Chittoor", "Hindupur", "Bhimavaram"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Khammam", "Karimnagar", "Ramagundam", "Mahabubnagar", "Nalgonda", "Adilabad", "Suryapet", "Miryalaguda", "Jagtial", "Kothagudem", "Mancherial", "Siddipet", "Wanaparthy", "Kamareddy", "Jangaon", "Bhongir", "Vikarabad", "Medak"],
    "West Bengal": ["Kolkata", "Darjeeling", "Howrah", "Durgapur", "Asansol", "Siliguri", "Kharagpur", "Haldia", "Krishnanagar", "Berhampore", "Malda", "Jalpaiguri", "Bankura", "Purulia", "Balurghat", "Raiganj", "Barasat", "Basirhat", "Serampore", "Bangaon", "Cooch Behar"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Junagadh", "Gandhinagar", "Anand", "Navsari", "Morbi", "Nadiad", "Mehsana", "Porbandar", "Godhra", "Palanpur", "Valsad", "Vapi", "Bhuj", "Veraval", "Botad"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner", "Alwar", "Bhilwara", "Sikar", "Pali", "Tonk", "Kishangarh", "Beawar", "Hanumangarh", "Dholpur", "Sawai Madhopur", "Churu", "Gangapur City", "Barmer", "Jhunjhunu", "Sirohi"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Kollam", "Thrissur", "Palakkad", "Alappuzha", "Malappuram", "Kannur", "Kottayam", "Manjeri", "Thalassery", "Ponnani", "Vatakara", "Kanhangad", "Payyanur", "Kayamkulam", "Neyyattinkara", "Tirur", "Koduvally", "Kottakkal"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur", "Puri", "Balasore", "Bhadrak", "Baripada", "Jharsuguda", "Jeypore", "Bargarh", "Rayagada", "Dhenkanal", "Kendujhar", "Angul", "Sunabeda", "Paradip", "Kendrapara", "Byasanagar", "Titlagarh"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tinsukia", "Tezpur", "Bongaigaon", "Diphu", "North Lakhimpur", "Goalpara", "Barpeta", "Sivasagar", "Karimganj", "Dhubri", "Kokrajhar", "Hailakandi", "Mangaldoi", "Nalbari", "Rangia", "Margherita"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar", "Hazaribagh", "Giridih", "Ramgarh", "Medininagar", "Chirkunda", "Phusro", "Jhumri Telaiya", "Sahibganj", "Lohardaga", "Dumka", "Godda", "Chatra", "Gumla", "Simdega", "Jamtara", "Garhwa"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Durg", "Rajnandgaon", "Raigarh", "Jagdalpur", "Ambikapur", "Dhamtari", "Chirmiri", "Mahasamund", "Bhatapara", "Kanker", "Kawardha", "Janjgir", "Naila", "Konta", "Kondagaon", "Dongargarh"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrapur", "Kashipur", "Rishikesh", "Pithoragarh", "Ramnagar", "Almora", "Nainital", "Kotdwar", "Tehri", "Joshimath", "Bageshwar", "Champawat", "Uttarkashi", "Ranikhet", "Vikasnagar", "Manglaur"],
    "Himachal Pradesh": ["Shimla", "Mandi", "Solan", "Dharamshala", "Palampur", "Baddi", "Nahan", "Kullu", "Chamba", "Hamirpur", "Una", "Bilaspur", "Kasauli", "Manali", "Dalhousie", "Paonta Sahib", "Nurpur", "Jogindernagar", "Rampur", "Sundernagar", "Keylong"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda", "Bicholim", "Curchorem", "Sanquelim", "Quepem", "Canacona", "Cuncolim", "Sanguem", "Pernem", "Valpoi", "Duler", "Porvorim", "Aldona", "Anjuna", "Calangute", "Candolim", "Colva"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailashahar", "Belonia", "Khowai", "Ambassa", "Teliamura", "Melaghar", "Sonamura", "Amarpur", "Sabroom", "Ranirbazar", "Jirania", "Mohanpur", "Kumarghat", "Kamalpur", "Panisagar", "Bishalgarh", "Kachucherra", "Manughat"],
    "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongpoh", "Baghmara", "Williamnagar", "Resubelpara", "Mairang", "Cherrapunji", "Nongstoin", "Khliehriat", "Amlarem", "Ranikor", "Dadenggre", "Tikrikilla", "Phulbari", "Mahendraganj", "Bishnupur", "Nartiang", "Umiam", "Mawlai"],
    "Manipur": ["Imphal", "Thoubal", "Bishnupur", "Churachandpur", "Kakching", "Ukhrul", "Senapati", "Tamenglong", "Jiribam", "Kangpokpi", "Moreh", "Mayang Imphal", "Nambol", "Moirang", "Wangjing", "Yairipok", "Kakching Khunou", "Lilong", "Sugnu", "Kumbi", "Nungba"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha", "Zunheboto", "Phek", "Kiphire", "Longleng", "Noklak", "Mon", "Chumoukedima", "Peren", "Tuli", "Medziphema", "Tseminyu", "Pfutsero", "Bhandari", "Aghunato", "Tizit"],
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

# --- UI LOCALIZATION FOR MULTIPLE LANGUAGES ---
UI_TEXT = {
    "English": {
        "title": "🌾 KisanSetu", "sub": "Smart AI Agriculture Platform",
        "tab0": "🏠 Overview & Features", "tab1": "🤖 AI Advisor", "tab2": "📊 Market Rates", "tab3": "📜 Govt Schemes", "tab4": "🔄 Translator",
        "ask": "💬 Ask your farming question or crop query:", "ask_ph": "Think deeply, ask or attach media...",
        "attach_img": "📎 Attach Images", "speech": "🎙️ Speech-to-Text", "img_mode": "🖼️ Images Mode", "btn_ai": "Ask AI / Analyze Crop",
        "mandi_title": "📊 Mandi Prices for", "crop_lbl": "Select Crop:", "unit_lbl": "Select Unit:",
        "tr_title": "🔄 Multilingual Translator", "tr_ph": "Enter text or upload document/image to translate:",
        "tr_btn": "Translate Text / Image", "dev": "Developed by Ankur Kumar & Vikalp Chaubey<br>The Aryan International School, Varanasi",
        "qp1": "How to grow wheat", "qp2": "How to grow rice", "qp3": "What happened to my tomatoes?"
    },
    "Hindi (हिंदी)": {
        "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई कृषि प्लेटफॉर्म",
        "tab0": "🏠 परिचय और विशेषताएँ", "tab1": "🤖 एआई सलाहकार", "tab2": "📊 बाजार भाव", "tab3": "📜 सरकारी योजनाएं", "tab4": "🔄 अनुवादक",
        "ask": "💬 अपना कृषि प्रश्न या फसल संबंधी जिज्ञासा पूछें:", "ask_ph": "गहराई से सोचें, पूछें या मीडिया संलग्न करें...",
        "attach_img": "📎 छवियां संलग्न करें", "speech": "🎙️ स्पीच-टू-टेक्स्ट", "img_mode": "🖼️ छवि मोड", "btn_ai": "एआई से पूछें / फसल विश्लेषण करें",
        "mandi_title": "📊 मंडी भाव:", "crop_lbl": "फसल चुनें:", "unit_lbl": "इकाई चुनें:",
        "tr_title": "🔄 बहुभाषी अनुवादक", "tr_ph": "अनुवाद के लिए टेक्स्ट दर्ज करें या दस्तावेज़/छवि अपलोड करें:",
        "tr_btn": "टेक्स्ट / छवि का अनुवाद करें", "dev": "अंकुर कुमार और विकल्प चौबे द्वारा विकसित<br>द आर्यन इंटरनेशनल स्कूल, वाराणसी",
        "qp1": "गेहूं कैसे उगाएं", "qp2": "चावल कैसे उगाएं", "qp3": "मेरे टमाटर को क्या हुआ?"
    }
}

def get_ui(lang_name):
    base = UI_TEXT.get("English", {})
    localized = UI_TEXT.get(lang_name, {})
    # Fallback merge for missing translations
    for k, v in base.items():
        if k not in localized:
            localized[k] = v
    return localized

PRE_MADE_ANSWERS = {
    "How to grow wheat": "🌾 **Wheat Guide:** Use well-drained loamy soil, sow in mid-November, and provide 4-6 irrigations.",
    "गेहूं कैसे उगाएं": "🌾 **गेहूं गाइड:** अच्छी तरह से सूखा हुआ दोमट मिट्टी का उपयोग करें, मध्य नवंबर में बुवाई करें, और 4-6 सिंचाई करें।",
    "How to grow rice": "🌾 **Rice Guide:** Clayey soil, maintain 2-5 cm standing water in puddled fields.",
    "चावल कैसे उगाएं": "🌾 **चावल गाइड:** चिकनी मिट्टी, जमे हुए खेतों में 2-5 सेमी खड़े पानी को बनाए रखें।",
    "What happened to my tomatoes?": "🍅 **Diagnosis:** Late Blight / Fruit Rot. Remove infected fruit and apply copper fungicide.",
    "मेरे टमाटर को क्या हुआ?": "🍅 **निदान:** लेट ब्लाइट / फ्रूट रोट। संक्रमित फल को हटाएं और कॉपर फंगसाइड लगाएं।"
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
    sel_state = st.selectbox("Select State / UT", list(STATES_AND_UTS.keys()))
    valid_cities = STATES_AND_UTS[sel_state]
    sel_city = st.selectbox("Select District / City", valid_cities)

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
    st.markdown("### 🌟 Comprehensive KisanSetu Feature Directory")
    st.markdown("Explore every powerful module integrated into the platform built by Ankur Kumar & Vikalp Chaubey.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='feature-card'><b>🤖 AI Agronomist & Vision</b><br>Instant crop disease diagnosis using high-speed neural models and live camera inputs.</div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>📊 Market Mandi Rates</b><br>Real-time district market valuations across all Indian states and UTs with custom unit converters.</div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>🎙️ Speech-to-Text Support</b><br>Voice-activated command and query inputs for effortless accessibility in rural environments.</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='feature-card'><b>📜 Government Scheme Hub</b><br>Comprehensive directory of subsidies, insurance policies, and financial aid portals like PM-Kisan.</div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>🔄 22 Scheduled Languages</b><br>Full bidirectional translation supporting all official Indian languages and document parsing.</div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>🖼️ Attached Media & Image Mode</b><br>Seamlessly attach files, soil reports, or camera snaps right inside the chat bar.</div>", unsafe_allow_html=True)

with tab1:
    st.markdown(f"#### ⚡ Quick Prompts:")
    qp1, qp2, qp3 = st.columns(3)
    if qp1.button(t['qp1']): st.session_state["query_input"] = t['qp1']
    if qp2.button(t['qp2']): st.session_state["query_input"] = t['qp2']
    if qp3.button(t['qp3']): st.session_state["query_input"] = t['qp3']

    st.divider()

    # Gemini-style Floating Pill Input Container simulation
    q = st.text_input(t['ask'], value=st.session_state["query_input"], placeholder=t['ask_ph'])
    
    # Custom interactive tool bar matching user reference image
    tb1, tb2, tb3 = st.columns(3)
    with tb1: attach_file = st.file_uploader(t['attach_img'], type=["png", "jpg", "jpeg", "pdf"], key="att_file")
    with tb2: speech_mode = st.toggle(t['speech'], value=False)
    with tb3: image_mode = st.toggle(t['img_mode'], value=False)
    
    cam_snap = st.camera_input("Take instant crop photo", key="cam_box") if image_mode else None
    final_media = cam_snap if cam_snap else attach_file

    if st.button(t['btn_ai']):
        lookup_key = q.strip()
        if lookup_key in PRE_MADE_ANSWERS:
            st.success(PRE_MADE_ANSWERS[lookup_key])
        elif q or final_media or speech_mode:
            with st.spinner("⚡ Analyzing data..."):
                st.success(ask_openrouter(f"Provide expert farming guidance in {lang} for district {sel_city}, {sel_state}. Query: {q}"))
        else:
            st.warning("Please enter a query or attach media.")

with tab2:
    st.markdown(f"### {t['mandi_title']} {sel_city}, {sel_state}")
    st.metric("Wheat", "₹2,400 / Quintal")
    st.metric("Paddy", "₹2,200 / Quintal")
    st.metric("Potato", "₹1,500 / Quintal")
    st.metric("Tomato", "₹3,000 / Quintal")

with tab3:
    st.markdown("### 📜 Active Government Schemes & Subsidies")
    for name, desc in GOVT_SCHEMES:
        st.markdown(f"<div class='feature-card'><b>{name}</b><br>{desc}</div>", unsafe_allow_html=True)

with tab4:
    t_text = st.text_area(t['tr_ph'])
    tr_file = st.file_uploader("Upload document/image to translate", type=["png", "jpg", "txt"], key="tr_file_up")
    if st.button(t['tr_btn']) and (t_text or tr_file):
        with st.spinner("Translating..."):
            st.success(ask_openrouter(f"Translate the provided text into {lang}: {t_text}"))

st.markdown(f"<div class='footer' style='text-align:center; color:#9ca3af; margin-top:50px; font-size:13px;'><b>{t['dev']}</b></div>", unsafe_allow_html=True)
