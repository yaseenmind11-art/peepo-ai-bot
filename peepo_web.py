import streamlit as st
from google import genai
import os

# ==========================================
# 1. THE ULTIMATE VERIFICATION BLOCK
# ==========================================
# This injects the ID: G-EBWJ79E1EE multiple ways so Google CANNOT miss it.
st.set_page_config(page_title="Peepo 3 AI", page_icon="image_13ffcc.png")

# Injection 1: The Google Analytics Script
st.markdown(
    """
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-EBWJ79E1EE"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-EBWJ79E1EE');
    </script>
    """, 
    unsafe_allow_html=True
)

# Injection 2: The Meta Tag & Visible fallback
st.markdown('<meta name="google-site-verification" content="W9JcAjDYAJtTHQz2toGnqDUsgQo34tcEmQSf-NItZug" />', unsafe_allow_html=True)
st.write("", unsafe_allow_html=True)

# Injection 3: A physical link for the bot to crawl
if "verify" in st.query_params:
    st.write("Verification ID: G-EBWJ79E1EE")
    st.stop()

# ==========================================
# 2. PEEPO 3 DESIGN & STYLE
# ==========================================
st.markdown(r"""
<style>
[data-theme="light"] .stApp { background: linear-gradient(135deg, #d1e9ff 0%, #e1d5f5 100%) !important; }
[data-theme="dark"] .stApp { background-color: #000000 !important; }
.centered-logo { display: flex; justify-content: center; align-items: center; margin-bottom: -40px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. PEEPO 3 AI LOGIC
# ==========================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("API Key missing!")

if "all_chats" not in st.session_state: st.session_state.all_chats = {} 
if "current_chat" not in st.session_state: st.session_state.current_chat = None 

with st.sidebar:
    st.title("📂 Peepo History")
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_chat = None 
        st.rerun()
    st.divider()
    for chat_title in reversed(list(st.session_state.all_chats.keys())):
        if st.button(chat_title, key=chat_title, use_container_width=True):
            st.session_state.current_chat = chat_title
            st.rerun()

LOGO_PATH = "image_13ffcc.png"
if st.session_state.current_chat is None:
    st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=130)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Welcome to Peepo 3</h1>", unsafe_allow_html=True)
else:
    for message in st.session_state.all_chats[st.session_state.current_chat]:
        avatar = LOGO_PATH if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

if prompt := st.chat_input("Message Peepo 3..."):
    if st.session_state.current_chat is None:
        new_title = prompt[:25] + "..." if len(prompt) > 25 else prompt
        st.session_state.current_chat = new_title
        st.session_state.all_chats[new_title] = []
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    try:
        response = client.models.generate_content(model="gemini-3.1-flash-lite-preview", contents=prompt)
        st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": response.text})
        st.rerun() 
    except Exception as e:
        st.error(f"Error: {e}")
