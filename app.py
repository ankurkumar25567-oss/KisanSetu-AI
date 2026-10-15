import streamlit as st
import urllib.request
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="wide", initial_sidebar_state="auto")

components.html("""<script>document.body.style.overscrollBehavior = 'none';</script>""", height=0)

st.markdown("""
<style>
    :root {
        --safe-top: env(safe-area-inset-top, 35px);
    }
    .stApp {
        margin-top: var(--safe-top) !important;
        background-color: #07090e !important;
        color: #f3f4f6 !important;
    }
    [data-testid="stAppViewContainer"] {
        padding-top: calc(var(--safe-top) + 20px) !important;
        background-color: #07090e !important;
        color: #f3f4f6 !important;
    }
    .block-container {
        max-width: 980px !important;
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .main-header { text-align: center; color: #4ade80; font-size: clamp(2rem, 5vw, 2.8rem); font-weight: 800; }
    .sub-header { text-align: center; color: #86efac; font-size: 1.1rem; margin-bottom: 25px; }
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

LANGUAGES = [
    "English", "Hindi (हिंदी)", "Assamese (অসমীয়া)", "Bengali (বাংলা)", 
    "Bodo (बड़ो)", "Dogri (डोगरी)", "Gujarati (ગુજરાતી)", "Kannada (ಕನ್ನಡ)", 
    "Kashmiri (कॉशुर)", "Konkani (कोंकणी)", "Maithili (मैथिली)", "Malayalam (മലയാളം)", 
    "Manipuri (মৈতৈলোন্)", "Marathi (मराठी)", "Nepali (नेपाली)", "Odia (ଓଡ଼ିଆ)", 
    "Punjabi (ਪੰਜਾਬੀ)", "Sanskrit (संस्कृतम्)", "Santali (संताली)", "Sindhi (सिंधी)", 
    "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Urdu (اردو)"
]

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

MANDI_CROPS = {
    "Wheat (गेहूं)": 2400, "Paddy/Rice (धान)": 2200, "Maize (मक्का)": 2100, "Bajra (बाजरा)": 2500,
    "Jowar (ज्वार)": 3100, "Ragi (रागी)": 3800, "Barley (जौ)": 1850, "Tur / Arhar (अरहर)": 7000,
    "Moong (मूंग)": 8500, "Urad (उड़द)": 6900, "Chana / Gram (चना)": 5400, "Masoor (मसूर)": 6000,
    "Groundnut (मूंगफली)": 6300, "Mustard / Rai (सरसों)": 5650, "Soybean (सोयाबीन)": 4600, "Sunflower (सूरजमुखी)": 6760,
    "Safflower (कुसुम)": 5800, "Sesamum / Til (तिल)": 8630, "Nigerseed (रामतिल)": 7730, "Cotton (कपास)": 7000,
    "Jute (जूट)": 5050, "Sugarcane (गन्ना)": 350, "Potato (आलू)": 1500, "Onion (प्याज)": 2500,
    "Garlic (लहसुन)": 8000, "Ginger (अदरक)": 6000, "Turmeric (हल्दी)": 12000, "Coriander (धनिया)": 7000,
    "Cumin / Jeera (जीरा)": 25000, "Fennel / Saunf (सौंफ)": 10000, "Fenugreek / Methi (मेथी)": 5500, "Black Pepper (काली मिर्च)": 50000,
    "Cardamom (इलायची)": 120000, "Tea (चाय पत्ती)": 20000, "Coffee (कॉफी)": 18000, "Coconut (नारियल)": 3000,
    "Banana (केला)": 2000, "Mango (आम)": 4500, "Apple (सेब)": 8000, "Orange (संतरा)": 4000,
    "Grapes (अंगूर)": 6000, "Papaya (पपीता)": 2500, "Pomegranate (अनार)": 9000, "Guava (अमरूद)": 3500,
    "Pineapple (अनानास)": 3000, "Jackfruit (कठहल)": 2000
}

UI_TEXT = {
    "English": {
        "title": "🌾 KisanSetu", "sub": "Smart AI Agriculture Platform",
        "tab0": "🏠 Overview & Features", "tab1": "🤖 AI Advisor", "tab2": "📊 Market Rates", "tab3": "📜 Govt Schemes", "tab4": "🔄 Translator",
        "ask": "💬 Ask your farming question or crop query:", "ask_ph": "Think deeply, ask or attach media...",
        "attach_img": "📎 Attach Images", "speech": "🎙️ Speech-to-Text", "img_mode": "🖼️ Images Mode", "btn_ai": "Ask AI / Analyze Crop",
        "mandi_title": "📊 Mandi Prices for", "crop_lbl": "Select Crop:", "unit_lbl": "Select Unit:",
        "tr_title": "🔄 Multilingual Translator", "tr_ph": "Enter text or upload document/image to translate:",
        "tr_btn": "Translate Text / Image", "dev": "Developed by Ankur Kumar & Vikalp Chaubey<br>The Aryan International School, Varanasi",
        "qp1": "How to grow wheat", "qp2": "How to grow rice", "qp3": "What happened to my tomatoes?",
        "sidebar_lang": "🌐 Language", "sidebar_state": "Select State / UT", "sidebar_city": "Select District / City",
        "warn_empty": "Please enter a query or attach media.", "analyzing": "⚡ Analyzing data...", "translating": "Translating..."
    },
    "Hindi (हिंदी)": {
        "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई कृषि प्लेटफॉर्म",
        "tab0": "🏠 परिचय और विशेषताएँ", "tab1": "🤖 एआई सलाहकार", "tab2": "📊 बाजार भाव", "tab3": "📜 सरकारी योजनाएं", "tab4": "🔄 अनुवादक",
        "ask": "💬 अपना कृषि प्रश्न या फसल संबंधी जिज्ञासा पूछें:", "ask_ph": "गहराई से सोचें, पूछें या मीडिया संलग्न करें...",
        "attach_img": "📎 छवियां संलग्न करें", "speech": "🎙️ स्पीच-टू-टेक्स्ट", "img_mode": "🖼️ छवि मोड", "btn_ai": "एआई से पूछें / फसल विश्लेषण करें",
        "mandi_title": "📊 मंडी भाव:", "crop_lbl": "फसल चुनें:", "unit_lbl": "इकाई चुनें:",
        "tr_title": "🔄 बहुभाषी अनुवादक", "tr_ph": "अनुवाद के लिए टेक्स्ट दर्ज करें या दस्तावेज़/छवि अपलोड करें:",
        "tr_btn": "टेक्स्ट / छवि का अनुवाद करें", "dev": "अंकुर कुमार और विकल्प चौबे द्वारा विकसित<br>द आर्यन इंटरनेशनल स्कूल, वाराणसी",
        "qp1": "गेहूं कैसे उगाएं", "qp2": "चावल कैसे उगाएं", "qp3": "मेरे टमाटर को क्या हुआ?",
        "sidebar_lang": "🌐 भाषा", "sidebar_state": "राज्य / केंद्र शासित प्रदेश चुनें", "sidebar_city": "जिला / शहर चुनें",
        "warn_empty": "कृपया कोई प्रश्न दर्ज करें या मीडिया संलग्न करें।", "analyzing": "⚡ डेटा विश्लेषण किया जा रहा है...", "translating": "अनुवाद हो रहा है..."
    },
    "Punjabi (ਪੰਜਾਬੀ)": {
        "title": "🌾 ਕਿਸਾਨ ਸੇਤੂ", "sub": "ਸਮਾਰਟ ਏਆਈ ਖੇਤੀਬਾੜੀ ਪਲੇਟਫਾਰਮ",
        "tab0": "🏠 ਜਾਣਕਾਰੀ ਅਤੇ ਵਿਸ਼ੇਸ਼ਤਾਵਾਂ", "tab1": "🤖 ਏਆਈ ਸਲਾਹਕਾਰ", "tab2": "📊 ਬਾਜ਼ਾਰ ਭਾਵ", "tab3": "📜 ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ", "tab4": "🔄 ਅਨੁਵਾਦਕ",
        "ask": "💬 ਆਪਣਾ ਖੇਤੀਬਾੜੀ ਸਵਾਲ ਪੁੱਛੋ:", "ask_ph": "ਡੂੰਘਾਈ ਨਾਲ ਸੋਚੋ, ਪੁੱਛੋ ਜਾਂ ਮੀਡੀਆ ਜੋੜੋ...",
        "attach_img": "📎 ਫੋਟੋਆਂ ਜੋੜੋ", "speech": "🎙️ ਸਪੀਚ-ਟੂ-ਟੈਕਸਟ", "img_mode": "🖼️ ਚਿੱਤਰ ਮੋਡ", "btn_ai": "ਏਆਈ ਤੋਂ ਪੁੱਛੋ",
        "mandi_title": "📊 ਮੰਡੀ ਭਾਵ:", "crop_lbl": "ਫਸਲ ਚੁਣੋ:", "unit_lbl": "ਯੂਨਿਟ ਚੁਣੋ:",
        "tr_title": "🔄 ਅਨੁਵਾਦਕ", "tr_ph": "ਅਨੁਵਾਦ ਲਈ ਟੈਕਸਟ ਦਰਜ ਕਰੋ:", "tr_btn": "ਅਨੁਵਾਦ ਕਰੋ",
        "dev": "ਅੰਕੁਰ ਕੁਮਾਰ ਅਤੇ ਵਿਕਲਪ ਚੌਬੇ ਦੁਆਰਾ ਵਿਕਸਤ<br>ਦ ਆਰੀਅਨ ਇੰਟਰਨੈਸ਼ਨਲ ਸਕੂਲ, ਵਾਰਾਣਸੀ",
        "qp1": "ਕਣਕ ਕਿਵੇਂ ਉਗਾਉਣੀ ਹੈ", "qp2": "ਝੋਨਾ ਕਿਵੇਂ ਉਗਾਉਣਾ ਹੈ", "qp3": "ਮੇਰੇ ਟਮਾਟਰਾਂ ਨੂੰ ਕੀ ਹੋਇਆ?",
        "sidebar_lang": "🌐 ਭਾਸ਼ਾ", "sidebar_state": "ਰਾਜ / UT ਚੁਣੋ", "sidebar_city": "ਜ਼ਿਲ੍ਹਾ / ਸ਼ਹਿਰ ਚੁਣੋ",
        "warn_empty": "ਕਿਰਪਾ ਕਰਕੇ ਸਵਾਲ ਦਰਜ ਕਰੋ ਜਾਂ ਮੀਡੀਆ ਜੋੜੋ।", "analyzing": "⚡ ਡਾਟਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ...", "translating": "ਅਨੁਵਾਦ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ..."
    },
    "Telugu (తెలుగు)": {
        "title": "🌾 కిసాన్ సేతు", "sub": "స్మార్ట్ AI వ్యవసాయ వేదిక",
        "tab0": "🏠 అవలోకనం & ఫీచర్లు", "tab1": "🤖 AI సలహాదారు", "tab2": "📊 మార్కెట్ ధరలు", "tab3": "📜 ప్రభుత్వ పథకాలు", "tab4": "🔄 అనువాదకుడు",
        "ask": "💬 మీ వ్యవసాయ ప్రశ్నను అడగండి:", "ask_ph": "లోతుగా ఆలోచించండి, అడగండి లేదా మీడియా జోడించండి...",
        "attach_img": "📎 చిత్రాలను జోడించండి", "speech": "🎙️ స్పీచ్-టూ-టెక్స్ట్", "img_mode": "🖼️ ఇమేజ్ మోడ్", "btn_ai": "AIని అడగండి",
        "mandi_title": "📊 మార్కెట్ ధరలు:", "crop_lbl": "పంటను ఎంచుకోండి:", "unit_lbl": "యూనిట్ ఎంచుకోండి:",
        "tr_title": "🔄 అనువాదకుడు", "tr_ph": "అనువదించడానికి టెక్స్ట్ నమోదు చేయండి:", "tr_btn": "అనువదించు",
        "dev": "అంకుర్ కుమార్ & వికల్ప్ చౌబే ద్వారా అభివృద్ధి చేయబడింది",
        "qp1": "గోధుమలు ఎలా పండించాలి", "qp2": "వరి ఎలా సాగు చేయాలి", "qp3": "నా టమాటాలకు ఏమైంది?",
        "sidebar_lang": "🌐 భాష", "sidebar_state": "రాష్ట్రం / UT ఎంచుకోండి", "sidebar_city": "జిల్లా / నగరం ఎంచుకోండి",
        "warn_empty": "దయచేసి ప్రశ్నను నమోదు చేయండి లేదా మీడియాను జోడించండి.", "analyzing": "⚡ డేటా విశ్లేషించబడుతోంది...", "translating": "అనువదించబడుతోంది..."
    },
    "Bengali (বাংলা)": {
        "title": "🌾 কিষাণ সেতু", "sub": "স্মার্ট এআই কৃষি প্ল্যাটফর্ম",
        "tab0": "🏠 ওভারভিউ এবং বৈশিষ্ট্য",
        "tab1": "🤖 এআই উপদেষ্টা",
        "tab2": "📊 বাজার দর",
        "tab3": "📜 সরকারি স্কিম",
        "tab4": "🔄 অনুবাদক",
        "ask": "💬 আপনার কৃষির প্রশ্ন জিজ্ঞাসা করুন:",
        "ask_ph": "গভীরভাবে চিন্তা করুন, জিজ্ঞাসা করুন বা মিডিয়া সংযুক্ত করুন...",
        "attach_img": "📎 ছবি সংযুক্ত করুন",
        "speech": "🎙️ স্পিচ-টু-টেক্সট",
        "img_mode": "🖼️ ছবি মোড",
        "btn_ai": "এআই কে জিজ্ঞাসা করুন",
        "mandi_title": "📊 বাজার দর:",
        "crop_lbl": "ফসল বাছুন:",
        "unit_lbl": "একক বাছুন:",
        "tr_title": "🔄 অনুবাদক",
        "tr_ph": "অনুবাদ করতে টেক্সট লিখুন:",
        "tr_btn": "অনুবাদ করুন",
        "dev": "অঙ্কুর কুমার এবং বিকল্প চৌবে দ্বারা বিকশিত",
        "qp1": "কীভাবে গম চাষ করবেন",
        "qp2": "কীভাবে ধান চাষ করবেন",
        "qp3": "আমার টমেটোর কী হয়েছে?",
        "sidebar_lang": "🌐 ভাষা",
        "sidebar_state": "রাজ্য / UT বাছুন",
        "sidebar_city": "জেলা / শহর বাছুন",
        "warn_empty": "দয়া করে একটি প্রশ্ন লিখুন বা মিডিয়া সংযুক্ত করুন।",
        "analyzing": "⚡ ডেটা বিশ্লেষণ করা হচ্ছে...",
        "translating": "অনুবাদ করা হচ্ছে..."
    }
}

def get_ui(lang_name):
    base = UI_TEXT.get("English", {})
    localized = UI_TEXT.get(lang_name, {})
    for k, v in base.items():
        if k not in localized:
            localized[k] = v
    return localized

PRE_MADE_ANSWERS = {
    "How to grow wheat": "🌾 **Wheat Guide:** Use well-drained loamy soil, sow in mid-November, and provide 4-6 irrigations.",
    "गेहूं कैसे उगाएं": "🌾 **गेहूं गाइड:** अच्छी तरह से सूखा हुआ दोमट मिट्टी का उपयोग करें, मध्य नवंबर में बुवाई करें, और 4-6 सिंचाई करें。",
    "ਕਣਕ ਕਿਵ
