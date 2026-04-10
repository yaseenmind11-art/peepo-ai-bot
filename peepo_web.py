import streamlit as st
from google import genai
import os

# ==========================================
# 1. GOOGLE BACKDOOR VERIFICATION (DO NOT REMOVE)
# ==========================================
# This uses your Measurement ID to verify ownership via Google Analytics
st.markdown(
    """
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-EBWJ79E1EE"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-EBWJ79E1EE');
    </script>
    <meta name="google-site-verification" content="W9JcAjDYAJtTHQz2toGnqDUsgQo34tcEmQSf-NItZug" />
    """,
    unsafe_allow_html=True
)

# This handles the specific HTML file check if Google looks for it
if "google470ff30df2261297.html" in st.query_params:
    st.write("google-site-verification: google470ff30df2261297.html")
    st.stop()

# ==========================================
# 2. PAGE CONFIG & THEME
# ==========================================
st.set_page_config(page_title="Peepo 3 AI", page_icon="image_13ffcc.png")

st.markdown(r"""
<style>
/* LIGHT THEME */
[data-theme="light"] .stApp, .stApp {
    background: linear-gradient(135deg, #d1e9ff 0%, #e1d5f5 50%, #ffffff 100%) !important;
}
/* DARK THEME */
[data-theme="dark"] .stApp, [data-theme="dark"] [data-testid="stHeader"] {
    background-color: #000000 !important;
    background-image: none !important;
}
[data-theme="dark"] .p-sticker, 
[data-theme="dark"] [data-testid="stchatAvatarAssistant"] img {
    filter: invert(1) brightness(2) !important;
}
[data-theme="dark"] [data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
}
/* LAYOUT */
.centered-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: -40px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. PEEPO 3 AI LOGIC
# ==========================================
try:
    # Remove quotes or extra spaces from the API Key
    API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("⚠️ API Key missing! Please add it to your Streamlit Secrets.")

# Chat history initialization
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None 

# Sidebar Management
with st.sidebar:
    st.title("📂 Peepo History")
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_chat = None 
        st.rerun()
    st.divider()
    
    # Simple search/filter for history
    search_query = st.text_input("🔍 Search chats...", placeholder="Type to filter...")
    for chat_title in reversed(list(st.session_state.all_chats.keys())):
        if not search_query or search_query.lower() in chat_title.lower():
            if st.button(chat_title, key=chat_title, use_container_width=True):
                st.session_state.current_chat = chat_title
                st.rerun()

# Main Interface
LOGO_PATH = "image_13ffcc.png"

if st.session_state.current_chat is None:
    # Start Screen
    st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=130)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Welcome to Peepo 3</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.8;'>Arduino code, science help, or just a chat—I'm ready!</p>", unsafe_allow_html=True)
else:
    # Active Chat Header
    header_col1, header_col2 = st.columns([1, 6])
    with header_col1:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=50)
    with header_col2:
        st.markdown(f"<h2 style='margin-top: 5px;'>{st.session_state.current_chat}</h2>", unsafe_allow_html=True)
    
    # Display Messages
    for message in st.session_state.all_chats[st.session_state.current_chat]:
        avatar = LOGO_PATH if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# User Input Logic
if prompt := st.chat_input("Message Peepo 3..."):
    if st.session_state.current_chat is None:
        # Create a new chat title based on the first message
        new_title = prompt[:25] + "..." if len(prompt) > 25 else prompt
        st.session_state.current_chat = new_title
        st.session_state.all_chats[new_title] = []
    
    # Add User Message
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    # Generate AI Response
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
            contents=prompt
        )
        ai_text = response.text
        st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": ai_text})
        st.rerun() 
    except Exception as e:
        st.error(f"⚠️ Peepo Error: {e}")
