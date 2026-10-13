import streamlit as st
import urllib.request
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="wide")

components.html("""<script>document.body.style.overscrollBehavior = 'none';</script>""", height=0)

st.markdown("""
<style>
    .stApp { background-color: #0f1117; color: #f3f4f6; }
    .main-header { text-align: center; color: #4ade80; font-size: 2.5rem; font-weight: 800; }
    .sub-header { text-align: center; color: #86efac; font-size: 1.1rem; margin-bottom: 20px; }
    .stButton>button { width: 100%; background-color: #15803d; color: white; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

LANGUAGES = ["English", "Hindi (हिंदी)", "Punjabi (ਪੰਜਾਬੀ)", "Telugu (తెలుగు)", "Bengali (বাংলা)"]

with st.sidebar:
    lang = st.selectbox("🌐 Language", LANGUAGES)
    api_key_check = st.secrets.get("GEMINI_API_KEY", "Missing")
    st.write(f"Key loaded: {'✅' if api_key_check != 'Missing' else '❌'}")

def ask_gemini(prompt_text):
    key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    
    req = urllib.request.Request(url, headers=headers, data=json.dumps(payload).encode('utf-8'), method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data['candidates'][0]['content']['parts'][0]['text']

st.markdown("<div class='main-header'>🌾 KisanSetu</div><div class='sub-header'>Development Mode</div>", unsafe_allow_html=True)

q = st.text_input("Ask your farming question:")
if st.button("Ask AI"):
    if not q:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Calling Gemini AI..."):
            try:
                ans = ask_gemini(f"Provide practical farming advice in {lang}: {q}")
                st.success(ans)
            except Exception as e:
                st.error(f"API Error: {str(e)}")
                
