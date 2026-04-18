import streamlit as st
from google import genai
import os
from PIL import Image
import requests
from io import BytesIO

# --- 1. THE ULTIMATE VERIFICATION DOOR ---
if "google470ff30df2261297.html" in st.query_params:
    st.write("google-site-verification: google470ff30df2261297.html")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Peepo 3 AI", page_icon="image_13ffcc.png")

# --- 3. THEME STYLING (ZOOMED LOOK) ---
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
[data-theme="dark"] [data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
}
.centered-logo {
    display: flex; justify-content: center; align-items: center; margin-bottom: -40px;
}
</style>
""", unsafe_allow_html=True)

# --- 4. API SETUP ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
    # New client initialized with Imagen endpoint compatibility
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("⚠️ API Key missing in Streamlit Secrets!")

# --- 5. SESSION STATE ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None 

# --- 6. SIDEBAR & HISTORY ---
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
    st.markdown("<p style='text-align: center;'>Tell me what image you want to see!</p>", unsafe_allow_html=True)
else:
    for message in st.session_state.all_chats[st.session_state.current_chat]:
        avatar = LOGO_PATH if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            # Display generated images with a clean boundary
            if "image_url" in message:
                st.image(message["image_url"], caption=message["prompt_used"], use_container_width=True)
            else:
                st.markdown(message["content"])

# --- 8. CHAT INPUT BAR (IMAGEN INTEGRATION) ---
if prompt := st.chat_input("Describe the image... (e.g., 'a cat in space')"):
    if st.session_state.current_chat is None:
        new_title = prompt[:25] + "..." if len(prompt) > 25 else prompt
        st.session_state.current_chat = new_title
        st.session_state.all_chats[new_title] = []
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar=LOGO_PATH):
        with st.spinner(f"✨ Generating image of '{prompt}'..."):
            try:
                # 🚀 Switched to standard image generation endpoint
                # model="gemini-3-flash" or "gemini-3-pro" is required here
                response = client.models.generate_content(
                    model="gemini-3-flash", 
                    contents=prompt
                )
                
                # Check if the generation produced an image
                if response.image_part:
                    generated_image = response.image_part
                    # Streamlit handles the object directly
                    st.image(generated_image, caption=f"Result for: '{prompt}'", use_container_width=True)
                    
                    # Store the result in history so it doesn't disappear
                    st.session_state.all_chats[st.session_state.current_chat].append({
                        "role": "assistant",
                        "image_object": generated_image,
                        "prompt_used": prompt
                    })
                else:
                    st.warning("🚦 The model couldn't create that image right now.")
                    st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": "🚦 Generation failed."})

                st.rerun() 

            except Exception as e:
                # Optimized error handling for free-tier users
                if "429" in str(e):
                    st.error("🚦 Peepo is at capacity (Rate Limit). Please wait 60 seconds!")
                else:
                    st.error(f"⚠️ Error: {e}")
