import streamlit as st
from google import genai
import os

# --- 1. THE ULTIMATE VERIFICATION DOOR ---
if "google470ff30df2261297.html" in st.query_params:
    st.write("google-site-verification: google470ff30df2261297.html")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Peepo 3 AI", page_icon="image_13ffcc.png")

# --- 3. THEME STYLING ---
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

# --- 4. API SETUP ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("API Key missing! Add it to Streamlit Secrets.")

# --- 5. SESSION STATE ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None 

# --- 6. SIDEBAR ---
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

# --- 7. MAIN INTERFACE ---
LOGO_PATH = "image_13ffcc.png"
if st.session_state.current_chat is None:
    st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=130)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Welcome to Peepo 3</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ready for some Arduino coding, science help, or generating images?</p>", unsafe_allow_html=True)
else:
    for message in st.session_state.all_chats[st.session_state.current_chat]:
        avatar = LOGO_PATH if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            if "image" in message:
                st.image(message["image"])
            if "content" in message and message["content"]:
                st.markdown(message["content"])

# --- 8. CHAT INPUT BAR ---
if prompt := st.chat_input("Message Peepo 3..."):
    if st.session_state.current_chat is None:
        new_title = prompt[:25] + "..." if len(prompt) > 25 else prompt
        st.session_state.current_chat = new_title
        st.session_state.all_chats[new_title] = []
    
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    try:
        # Check if user wants an image
        if any(word in prompt.lower() for word in ["draw", "generate image", "make a picture", "image of"]):
            # Use the Imagen model for drawing
            response = client.models.generate_image(
                model="imagen-3",
                prompt=prompt,
            )
            image = response.generated_images[0].image.show() # This triggers the image generation
            st.session_state.all_chats[st.session_state.current_chat].append({
                "role": "assistant", 
                "content": f"Here is your image for: '{prompt}'",
                "image": response.generated_images[0].image
            })
        else:
            # Normal text chat
            response = client.models.generate_content(model="gemini-3.1-flash-lite-preview", contents=prompt)
            st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": response.text})
        
        st.rerun() 
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
