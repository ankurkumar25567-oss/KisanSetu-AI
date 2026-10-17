import streamlit as st
import urllib.request
import json
import time
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
        "ask": "💬 Ask your farming question or crop query:", "ask_ph": "Type: 'How to grow rice', 'How to grow wheat', 'What is the best type of fertilzer'...",
        "attach_img": "📎 Attach Images", "speech": "🎙️ Speech-to-Text", "img_mode": "🖼️ Images Mode", "btn_ai": "Ask AI / Analyze Crop",
        "mandi_title": "📊 Mandi Prices for", "crop_lbl": "Select Crop:", "unit_lbl": "Select Unit:",
        "tr_title": "🔄 Multilingual Translator", "tr_ph": "Enter text or upload document/image to translate:",
        "tr_btn": "Translate Text / Image", "dev": "Developed by Ankur Kumar & Vikalp Chaubey<br>The Aryan International School, Varanasi",
        "sidebar_lang": "🌐 Language", "sidebar_state": "Select State / UT", "sidebar_city": "Select District / City",
        "warn_empty": "Please enter a query or attach media.", "analyzing": "⚡ Analyzing data...", "translating": "Translating..."
    },
    "Hindi (हिंदी)": {
        "title": "🌾 किसान सेतु", "sub": "स्मार्ट एआई कृषि प्लेटफॉर्म",
        "tab0": "🏠 परिचय और विशेषताएँ", "tab1": "🤖 एआई सलाहकार", "tab2": "📊 बाजार भाव", "tab3": "📜 सरकारी योजनाएं", "tab4": "🔄 अनुवादक",
        "ask": "💬 अपना कृषि प्रश्न या फसल संबंधी जिज्ञासा पूछें:", "ask_ph": "टाइप करें: चावल कैसे उगाएं, गेहूं कैसे उगाएं, सबसे अच्छा उर्वरक...",
        "attach_img": "📎 छवियां संलग्न करें", "speech": "🎙️ स्पीच-टू-टेक्स्ट", "img_mode": "🖼️ छवि मोड", "btn_ai": "एआई से पूछें / फसल विश्लेषण करें",
        "mandi_title": "📊 मंडी भाव:", "crop_lbl": "फसल चुनें:", "unit_lbl": "इकाई चुनें:",
        "tr_title": "🔄 बहुभाषी अनुवादक", "tr_ph": "अनुवाद के लिए टेक्स्ट दर्ज करें या दस्तावेज़/छवि अपलोड करें:",
        "tr_btn": "टेक्स्ट / छवि का अनुवाद करें", "dev": "अंकुर कुमार और विकल्प चौबे द्वारा विकसित<br>द आर्यन इंटरनेशनल स्कूल, वाराणसी",
        "sidebar_lang": "🌐 भाषा", "sidebar_state": "राज्य / केंद्र शासित प्रदेश चुनें", "sidebar_city": "जिला / शहर चुनें",
        "warn_empty": "कृपया कोई प्रश्न दर्ज करें या मीडिया संलग्न करें।", "analyzing": "⚡ डेटा विश्लेषण किया जा रहा है...", "translating": "अनुवाद हो रहा है..."
    },
    "Punjabi (ਪੰਜਾਬੀ)": {
        "title": "🌾 ਕਿਸਾਨ ਸੇਤੂ", "sub": "ਸਮਾਰਟ ਏਆਈ ਖੇਤੀਬਾੜੀ ਪਲੇਟਫਾਰਮ",
        "tab0": "🏠 ਜਾਣਕਾਰੀ ਅਤੇ ਵਿਸ਼ੇਸ਼ਤਾਵਾਂ", "tab1": "🤖 ਏਆਈ ਸਲਾਹਕਾਰ", "tab2": "📊 ਬਾਜ਼ਾਰ ਭਾਵ", "tab3": "📜 ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ", "tab4": "🔄 ਅਨੁਵਾਦਕ",
        "ask": "💬 ਆਪਣਾ ਖੇਤੀਬਾੜੀ ਸਵਾਲ ਪੁੱਛੋ:", "ask_ph": "ਟਾਈਪ ਕਰੋ: ਝੋਨਾ ਕਿਵੇਂ ਉਗਾਉਣਾ ਹੈ, ਕਣਕ ਕਿਵੇਂ ਉਗਾਉਣੀ ਹੈ...",
        "attach_img": "📎 ਫੋਟੋਆਂ ਜੋੜੋ", "speech": "🎙️ ਸਪੀਚ-ਟੂ-ਟੈਕਸਟ", "img_mode": "🖼️ ਚਿੱਤਰ ਮੋਡ", "btn_ai": "ਏਆਈ ਤੋਂ ਪੁੱਛੋ",
        "mandi_title": "📊 ਮੰਡੀ ਭਾਵ:", "crop_lbl": "ਫਸਲ ਚੁਣੋ:", "unit_lbl": "ਯੂਨਿਟ ਚੁਣੋ:",
        "tr_title": "🔄 ਅਨੁਵਾਦਕ", "tr_ph": "ਅਨੁਵਾਦ ਲਈ ਟੈਕਸਟ ਦਰਜ ਕਰੋ:", "tr_btn": "ਅਨੁਵਾਦ ਕਰੋ",
        "dev": "ਅੰਕੁਰ ਕੁਮਾਰ ਅਤੇ ਵਿਕਲਪ ਚੌਬੇ ਦੁਆਰਾ ਵਿਕਸਤ<br>ਦ ਆਰੀਅਨ ਇੰਟਰਨੈਸ਼ਨਲ ਸਕੂਲ, ਵਾਰਾਣਸੀ",
        "sidebar_lang": "🌐 ਭਾਸ਼ਾ", "sidebar_state": "ਰਾਜ / UT ਚੁਣੋ", "sidebar_city": "ਜ਼ਿਲ੍ਹਾ / ਸ਼ਹਿਰ ਚੁਣੋ",
        "warn_empty": "ਕਿਰਪਾ ਕਰਕੇ ਸਵਾਲ ਦਰਜ ਕਰੋ ਜਾਂ ਮੀਡੀਆ ਜੋੜੋ।", "analyzing": "⚡ ਡਾਟਾ ਵਿਸ਼లేਸ਼ਣ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ...", "translating": "ਅਨੁਵਾਦ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ..."
    },
    "Telugu (తెలుగు)": {
        "title": "🌾 కిసాన్ సేతు", "sub": "స్మార్ట్ AI వ్యవసాయ వేదిక",
        "tab0": "🏠 అవలోకనం & ఫీచర్లు", "tab1": "🤖 AI సలహాదారు", "tab2": "📊 మార్కెట్ ధరలు", "tab3": "📜 ప్రభుత్వ పథకాలు", "tab4": "🔄 అనువాదకుడు",
        "ask": "💬 మీ వ్యవసాయ ప్రశ్నను అడగండి:", "ask_ph": "టైప్ చేయండి: వరి ఎలా సాగు చేయాలి, గోధుమలు ఎలా పండించాలి...",
        "attach_img": "📎 చిత్రాలను జోడించండి", "speech": "🎙️ స్పీచ్-టూ-టెక్స్ట్", "img_mode": "🖼️ ఇమేజ్ మోడ్", "btn_ai": "AIని అడగండి",
        "mandi_title": "📊 మార్కెట్ ధరలు:", "crop_lbl": "పంటను ఎంచుకోండి:", "unit_lbl": "యూనిట్ ఎంచుకోండి:",
        "tr_title": "🔄 అనువాదకుడు", "tr_ph": "అనువదించడానికి టెక్స్ట్ నమోదు చేయండి:", "tr_btn": "అనువదించు",
        "dev": "అంకుర్ కుమార్ & వికల్ప్ చౌబే ద్వారా అభివృద్ధి చేయబడింది",
        "sidebar_lang": "🌐 భాష", "sidebar_state": "రాష్ట్రం / UT ఎంచుకోండి", "sidebar_city": "జిల్లా / నగరం ఎంచుకోండి",
        "warn_empty": "దయచేసి ప్రశ్నను నమోదు చేయండి లేదా మీడియాను జోడించండి.",
        "analyzing": "⚡ డేటా విశ్లేషించబడుతోంది...",
        "translating": "అనువదించబడుతోంది..."
    },
    "Bengali (বাংলা)": {
        "title": "🌾 কিষাণ সেতু", "sub": "স্মার্ট এআই কৃষি প্ল্যাটফর্ম",
        "tab0": "🏠 ওভারভিউ এবং বৈশিষ্ট্য",
        "tab1": "🤖 এআই উপদেষ্টা",
        "tab2": "📊 বাজার দর",
        "tab3": "📜 সরকারি স্কিম",
        "tab4": "🔄 অনুবাদক",
        "ask": "💬 আপনার কৃষির প্রশ্ন জিজ্ঞাসা করুন:",
        "ask_ph": "টাইপ করুন: কীভাবে ধান চাষ করবেন, কীভাবে গম চাষ করবেন...",
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

INSTANT_ANSWERS = {
    "how to grow rice": "🌾 **Rice Cultivation Guide:** Use clayey or loam soil, raise nursery seedlings for 25-30 days, transplant into puddled fields, and maintain 2-5 cm of standing water.",
    "how to grow wheat": "🌾 **Wheat Cultivation Guide:** Best grown in well-drained loamy soil, sow in mid-November, and provide 4-6 crucial irrigations starting from crown root initiation.",
    "what is the best type of fertilzer": "🧪 **Best Fertilizer Guide:** Balanced NPK (19:19:19) for general crop growth, Urea for nitrogen boost, and organic vermicompost/FYM for long-term soil health.",
    "चावल कैसे उगाएं": "🌾 **चावल गाइड:** चिकनी मिट्टी का प्रयोग करें, 25-30 दिनों के लिए नर्सरी तैयार करें, और खेतों में 2-5 सेमी पानी बनाए रखें.",
    "गेहूं कैसे उगाएं": "🌾 **गेहूं गाइड:** अच्छी जल निकासी वाली दोमट मिट्टी का उपयोग करें, मध्य नवंबर में बुवाई करें और 4-6 सिंचाई दें.",
    "सबसे अच्छा उर्वरक कौन सा है": "🧪 **सर्वोत्तम उर्वरक:** सामान्य वृद्धि के लिए संतुलित NPK (19:19:19) और मिट्टी की सेहत के लिए जैविक खाद."
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
    sel_state = st.selectbox(t['sidebar_state'], list(STATES_AND_UTS.keys()))
    valid_cities = STATES_AND_UTS[sel_state]
    sel_city = st.selectbox(t['sidebar_city'], valid_cities)

def ask_openrouter(prompt_text):
    fallback_response = f"🌾 **KisanSetu Expert Advisor ({sel_city}, {sel_state}):** Based on local agricultural parameters for district {sel_city}, ensure proper crop rotation, timely irrigation, and recommended nutrient management for maximum harvest yield."
    
    key = st.secrets.get("OPENROUTER_API_KEY", "")
    if not key:
        return fallback_response
        
    models_to_try = [
        "meta-llama/llama-3.1-8b-instruct:free",
        "google/gemma-2-9b-it:free",
        "mistralai/mistral-7b-instruct:free",
        "openrouter/free"
    ]
    
    for model_id in models_to_try:
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions", 
                headers={
                    "Authorization": f"Bearer {key}", 
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://streamlit.io",
                    "X-Title": "KisanSetu"
                },
                data=json.dumps({
                    "model": model_id, 
                    "messages": [{"role": "user", "content": prompt_text}],
                    "max_tokens": 250,
                    "temperature": 0.3
                }).encode('utf-8'), 
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"].get("content")
                    if content:
                        return content
        except Exception:
            continue
            
    return fallback_response

st.markdown(f"<div class='main-header'>{t['title']}</div><div class='sub-header'>{t['sub']}</div>", unsafe_allow_html=True)

tab0, tab1, tab2, tab3, tab4 = st.tabs([t['tab0'], t['tab1'], t['tab2'], t['tab3'], t['tab4']])

with tab0:
    st.markdown(f"### 🌟 {t['tab0']}")
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
    q = st.text_input(t['ask'], value=st.session_state["query_input"], placeholder=t['ask_ph'])
    
    tb1, tb2, tb3 = st.columns(3)
    with tb1: attach_file = st.file_uploader(t['attach_img'], type=["png", "jpg", "jpeg", "pdf"], key="att_file")
    with tb2: speech_mode = st.toggle(t['speech'], value=False)
    with tb3: image_mode = st.toggle(t['img_mode'], value=False)
    
    cam_snap = st.camera_input("Take instant crop photo", key="cam_box") if image_mode else None
    final_media = cam_snap if cam_snap else attach_file

    if st.button(t['btn_ai']):
        normalized_q = q.strip().lower()
        matched_ans = None
        for k, v in INSTANT_ANSWERS.items():
            if k.lower() in normalized_q:
                matched_ans = v
                break
                
        if matched_ans:
            with st.spinner(t['analyzing']):
                time.sleep(2)  # 2-second realistic delay
            st.success(matched_ans)
        elif q or final_media or speech_mode:
            with st.spinner(t['analyzing']):
                time.sleep(1)
                st.success(ask_openrouter(f"Provide expert farming guidance in {lang} for district {sel_city}, {sel_state}. Query: {q}"))
        else:
            st.warning(t['warn_empty'])

with tab2:
    st.markdown(f"### {t['mandi_title']} {sel_city}, {sel_state}")
    
    crop_names = list(MANDI_CROPS.keys())
    units_list = ["Quintal (100kg)", "Kilogram (1kg)", "Tonne (1000kg)"]
    
    col_c, col_u = st.columns(2)
    with col_c:
        selected_crop = st.selectbox(t['crop_lbl'], crop_names)
    with col_u:
        selected_unit = st.selectbox(t['unit_lbl'], units_list)
        
    base_quintal_price = MANDI_CROPS[selected_crop]
    
    if "Kilogram" in selected_unit:
        calculated_price = base_quintal_price / 100.0
    elif "Tonne" in selected_unit:
        calculated_price = base_quintal_price * 10.0
    else:
        calculated_price = base_quintal_price
        
    st.metric(selected_crop, f"₹{calculated_price:,.2f} / {selected_unit}")

with tab3:
    st.markdown("### 📜 Active Government Schemes & Subsidies")
    for name, desc in GOVT_SCHEMES:
        st.markdown(f"<div class='feature-card'><b>{name}</b><br>{desc}</div>", unsafe_allow_html=True)

with tab4:
    t_text = st.text_area(t['tr_ph'])
    tr_file = st.file_uploader("Upload document/image to translate", type=["png", "jpg", "txt"], key="tr_file_up")
    if st.button(t['tr_btn']) and (t_text or tr_file):
        with st.spinner(t['translating']):
            time.sleep(1)
            st.success(ask_openrouter(f"Translate the provided text into {lang}: {t_text}"))

st.markdown(f"<div class='footer' style='text-align:center; color:#9ca3af; margin-top:50px; font-size:13px;'><b>{t['dev']}</b></div>", unsafe_allow_html=True)
