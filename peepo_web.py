import streamlit as st
from google import genai
import os

# Initialize session state variables at the very beginning to prevent AttributeErrors
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None 

if "google470ff30df2261297.html" in st.query_params:
    st.write("google-site-verification: google470ff30df2261297.html")
    st.stop()

st.set_page_config(page_title="Peepo 3 AI", page_icon="peepo-ai-preview.png")

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

def reset_everything():
    st.session_state.bg_p = "#0e1117"
    st.session_state.side_p = "#262730"
    st.session_state.text_p = "#fafafa"
    st.session_state.accent_p = "#A6A0A0"
 
    for i in range(0, 7):
        k = "text" if i == 0 else f"text{i}"
        st.session_state[k] = ""

def Light_Mode():
    st.session_state.bg_p = "#FFFFFF"
    st.session_state.side_p = "#F0F2F6"
    st.session_state.text_p = "#262730"
    st.session_state.accent_p = "#A6A0A0"
 
    for i in range(0, 7):
        k = "text" if i == 0 else f"text{i}"
        st.session_state[k] = ""
        
if "bg_p" not in st.session_state:
    st.session_state.bg_p = "#0e1117"
if "side_p" not in st.session_state:
    st.session_state.side_p = "#262730"
if "text_p" not in st.session_state:
    st.session_state.text_p = "#fafafa"
if "accent_p" not in st.session_state:
    st.session_state.accent_p = "#A6A0A0"

st.sidebar.title("Theme Customization 🎨")
bgcolorpick = st.sidebar.color_picker("• Choose a color for your background", key="bg_p")
sidebgcolorpick = st.sidebar.color_picker("• Choose a color for your sidebar background", key="side_p")
textcolorpick = st.sidebar.color_picker("• Choose a color for the text", key="text_p")
primarycolorpick = st.sidebar.color_picker("• Choose an accent color", key="accent_p")


st.sidebar.button("Dark Mode Default Theme", on_click=reset_everything)
st.sidebar.button("Light Mode Default Theme", on_click=Light_Mode)
    

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bgcolorpick}; }}
    section[data-testid="stSidebar"] {{ background-color: {sidebgcolorpick} !important; }}
    .stApp, p, h1, h2, h3, span {{ color: {textcolorpick} !important; }}
    button, [data-baseweb="button"] {{ 
        background-color: {primarycolorpick} !important; 
        color: white !important; 
    }}
    /* Keeps input fields light grey as seen in your screenshot */
    .stTextInput>div>div>input {{
        background-color: #F0F2F6 !important;
        color: #31333F !important;
    }}
    </style>
    """, unsafe_allow_html=True)
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
.centered-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: -40px;
}
</style>
""", unsafe_allow_html=True)

try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("API Key missing! Add it to Streamlit Secrets.")

LOGO_PATH = "peepo-ai-preview.png"
if st.session_state.current_chat is None:
    st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=130)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Welcome to Peepo 3</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>How can I assist you today? </p>", unsafe_allow_html=True)
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
        st.error(f"⚠️ Error: {e}")
