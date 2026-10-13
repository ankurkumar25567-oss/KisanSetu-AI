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
    "
    
