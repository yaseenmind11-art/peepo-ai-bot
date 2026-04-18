import streamlit as st
from google import genai
from google.genai import types
import os

# ==========================================
# 1. BRUTE FORCE VERIFICATION & SEO
# ==========================================
st.set_page_config(page_title="Peepo 3 AI - White Hat Edition", page_icon="image_13ffcc.png")

VERIFICATION_FILE = "google470ff30df2261297.html" 

if VERIFICATION_FILE in st.query_params or "verify" in st.query_params:
    st.write(f"google-site-verification: {VERIFICATION_FILE}")
    st.stop()

st.markdown(f'<meta name="google-site-verification" content="{VERIFICATION_FILE.replace(".html", "")}" />', unsafe_allow_html=True)

# Google Analytics
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

# ==========================================
# 2. RESTORE COLORS & THEME
# ==========================================
st.markdown(r"""
<style>
[data-theme="light"] .stApp, .stApp {
    background: linear-gradient(135deg, #d1e9ff 0%, #e1d5f5 50%, #ffffff 100%) !important;
}
[data-theme="dark"] .stApp, [data-theme="dark"] [data-testid="stHeader"] {
    background-color: #000000 !important;
    background-image: none !important;
}
[data-theme="dark"] [data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
}
.centered-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: -40px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. PEEPO-SEC LOGIC (THE BRAIN)
# ==========================================
SYSTEM_INSTRUCTION = """
You are Peepo-Sec, a world-class White Hat Hacker and Cybersecurity Researcher. 
Your mission is to help the user learn how to protect devices, find vulnerabilities 
legally, and stop dangerous cyber-attacks. 
Always prioritize teaching 'Defense' and 'Ethical Research'. 
If the user asks about a 'bad person', explain how to report them or 
how to build a defense against their specific type of attack.
"""

try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("⚠️ API Key missing! Check your Streamlit Secrets.")

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None 

# Sidebar History
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
    # WELCOME SCREEN
    st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=130)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Welcome to Peepo 3: White Hat</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555;'>Ask Peepo-Sec about cybersecurity and defense.</p>", unsafe_allow_html=True)
else:
    # DISPLAY MESSAGES
    for message in st.session_state.all_chats[st.session_state.current_chat]:
        avatar = LOGO_PATH if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# CHAT INPUT
if prompt := st.chat_input("Message Peepo-Sec..."):
    if st.session_state.current_chat is None:
        new_title = prompt[:25] + "..." if len(prompt) > 25 else prompt
        st.session_state.current_chat = new_title
        st.session_state.all_chats[new_title] = []
    
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    try:
        # Generate Content with System Instructions
        response = client.models.generate_content(
            model="gemini-2.0-flash", # Using a stable latest model
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            ),
            contents=prompt
        )
        
        st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": response.text})
        st.rerun() 
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("If it says '503 Unavailable', the AI is busy. Wait 1 minute and refresh!")
