import streamlit as st
from google import genai
from google.genai import types
import os
import time

# ==========================================
# 1. GOOGLE VERIFICATION & SEO
# ==========================================
st.set_page_config(page_title="peepo 3 ai", page_icon="image_13ffcc.png")

# ==========================================
# 2. THEME & STYLING (ZOOMED OUT LOOK)
# ==========================================
st.markdown(r"""
<style>
/* LIGHT MODE GRADIENT */
[data-theme="light"] .stApp, .stApp {
    background: linear-gradient(135deg, #d1e9ff 0%, #e1d5f5 50%, #ffffff 100%) !important;
}

/* DARK MODE FIX */
[data-theme="dark"] .stApp, [data-theme="dark"] [data-testid="stHeader"] {
    background-color: #000000 !important;
}

/* LOGO BOX */
.centered-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    padding-top: 40px;
}

/* MAIN TITLE - BIG AND BOLD */
.main-title {
    font-size: 85px !important; 
    font-weight: 900 !important;
    text-align: center;
    margin-top: -10px;
    letter-spacing: -1.5px;
    color: #31333F;
}

/* SUBTITLE - ZOOMED OUT */
.main-subtitle {
    font-size: 22px !important;
    text-align: center;
    color: #666;
    margin-top: -20px;
}

/* DARK MODE TEXT COLOR */
[data-theme="dark"] .main-title { color: #ffffff !important; }
[data-theme="dark"] .main-subtitle { color: #cccccc !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. PEEPO-SEC BRAIN (SYSTEM PROMPT)
# ==========================================
SYSTEM_INSTRUCTION = """
You are Peepo-Sec, a world-class White Hat Hacker and Cybersecurity Researcher. 
Your mission is to help the user learn how to protect devices, find vulnerabilities 
legally, and stop dangerous cyber-attacks. 
Always prioritize teaching 'Defense' and 'Ethical Research'.
"""

# ==========================================
# 4. API & SESSION SETUP
# ==========================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("⚠️ API Key missing in Streamlit Secrets!")

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None 

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

# ==========================================
# 5. WELCOME SCREEN
# ==========================================
if st.session_state.current_chat is None:
    st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=120) 
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<p class="main-title">peepo 3 ai</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">ask me for anything!</p>', unsafe_allow_html=True)
else:
    for message in st.session_state.all_chats[st.session_state.current_chat]:
        avatar = LOGO_PATH if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# ==========================================
# 6. CHAT INPUT (GEMINI 3.1 FLASH)
# ==========================================
if prompt := st.chat_input("Message peepo 3 ai..."):
    if st.session_state.current_chat is None:
        new_title = prompt[:25] + "..." if len(prompt) > 25 else prompt
        st.session_state.current_chat = new_title
        st.session_state.all_chats[new_title] = []
    
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    try:
        # UPDATED: Set to Gemini 3.1 Flash
        response = client.models.generate_content(
            model="gemini-3.1-flash", 
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            ),
            contents=prompt
        )
        
        st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": response.text})
        st.rerun() 

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            st.warning("🚦 Peepo 3.1 is working hard! Waiting 5s to bypass rate limit...")
            time.sleep(5)
            st.rerun()
        else:
            st.error(f"Error: {e}")
