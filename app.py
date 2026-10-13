import streamlit as st
import urllib.request
import json
from PIL import Image
import io
import streamlit.components.v1 as components

st.set_page_config(page_title="KisanSetu - Smart Ag", page_icon="🌾", layout="wide")

components.html("""
<script>
    document.body.style.overscrollBehavior = 'none';
</script>
""", height=0)

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
    api_key_check = st.secrets.get("BYTEZ_API_KEY", "Missing")
    st.write(f"Key loaded: {'✅' if api_key_check != 'Missing' else '❌'}")

def ask_bytez(prompt_text):
    key = st.secrets["BYTEZ_API_KEY"]
    url = "https://api.bytez.com/model/v2/meta-llama/Llama-3.1-8B-Instruct"
    headers = {"Authorization": key, "Content-Type": "application/json"}
    payload = {"messages": [{"role": "user", "content": prompt_text}]}
    
    req = urllib.request.Request(url, headers=headers, data=json.dumps(payload).encode('utf-8'), method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        if "output" in data:
            return data["output"]
        elif "choices" in data:
            return data["choices"][0]["message"]["content"]
        return str(data)

st.markdown("<div class='main-header'>🌾 KisanSetu</div><div class='sub-header'>Development Mode</div>", unsafe_allow_html=True)

q = st.text_input("Ask your farming question:")
if st.button("Ask AI"):
    if not q:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Calling Bytez API..."):
            try:
                ans = ask_bytez(f"Provide practical farming advice in {lang}: {q}")
                st.success(ans)
            except Exception as e:
                st.error(f"API Error: {str(e)}")
                
