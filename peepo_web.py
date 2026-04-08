import streamlit as st
from google import genai
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Peepo 3 AI", page_icon="image_13ffcc.png")

# --- 2. THEME STYLING ---
st.markdown("""
<style>
/* LIGHT MODE: Your custom gradient */
.stApp {
    background: linear-gradient(135deg, #d1e9ff 0%, #e1d5f5 50%, #ffffff 100%);
}

/* DARK MODE: Pure black background and White Logo */
@media (prefers-color-scheme: dark) {
    .stApp, [data-testid="stHeader"] {
        background-color: #000000 !important;
        background-image: none !important;
    }
    
    /* Flip the Black 'P' sticker to White only in Dark Mode */
    .p-sticker, [data-testid="stchatAvatarAssistant"] img, [data-testid="stImage"] img {
        filter: invert(1) brightness(2);
        background: transparent !important;
    }

    /* Make sidebar match the black theme */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
    }

    /* Keep text white in dark mode */
    h1, h2, h3, p, span {
        color: #ffffff !important;
    }
}

/* Layout & Logo Fixes */
.centered-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: -40px;
}

.p-sticker {
    border-radius: 50%; /* Keeps the 'P' clean */
}
</style>
""", unsafe_allow_html=True)

# --- 3. API SETUP ---
# Fetch the key from Streamlit Secrets
API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
MODEL_ID = "gemini-3.1-flash-lite-preview"
client = genai.Client(api_key=API_KEY)

# --- 4. SESSION STATE ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None 

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("📂 Peepo History")
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_chat = None 
        st.rerun()
    st.divider()
    search_query = st.text_input("🔍 Search chats...", placeholder="Type to filter...")
    for chat_title in reversed(list(st.session_state.all_chats.keys())):
        if not search_query or search_query.lower() in chat_title.lower():
            if st.button(chat_title, key=chat_title, use_container_width=True):
                st.session_state.current_chat = chat_title
                st.rerun()

# --- 6. LOGO PATH ---
LOGO_PATH = "image_13ffcc.png"

# --- 7. MAIN INTERFACE ---
if st.session_state.current_chat is None:
    # WELCOME SCREEN
    st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        # We give it a specific class so the CSS can find it
        st.image(LOGO_PATH, width=130)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>Welcome to Peepo 3</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.8;'>Ready for some Arduino coding or science help?</p>", unsafe_allow_html=True)

else:
    # ACTIVE CHAT HEADER
    header_col1, header_col2 = st.columns([1, 6])
    with header_col1:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=50)
    with header_col2:
        st.markdown(f"<h2 style='margin-top: 5px;'>{st.session_state.current_chat}</h2>", unsafe_allow_html=True)

    # Message Display
    for message in st.session_state.all_chats[st.session_state.current_chat]:
        # Use the 'P' logo for the assistant
        avatar = LOGO_PATH if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# --- 8. CHAT INPUT ---
if prompt := st.chat_input("Message Peepo 3..."):
    if st.session_state.current_chat is None:
        new_title = prompt[:25] + "..." if len(prompt) > 25 else prompt
        st.session_state.current_chat = new_title
        st.session_state.all_chats[new_title] = []

    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.models.generate_content(model=MODEL_ID, contents=prompt)
        ai_text = response.text
        st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": ai_text})
        with st.chat_message("assistant", avatar=LOGO_PATH):
            st.markdown(ai_text)
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
