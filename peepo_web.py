import streamlit as st
from google import genai
import os
import json # New required library

# --- 1. THE ULTIMATE VERIFICATION DOOR ---
if "google470ff30df2261297.html" in st.query_params:
    st.write("google-site-verification: google470ff30df2261297.html")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Peepo 3 AI", page_icon="image_13ffcc.png")

# --- 3. THEME STYLING (ZOOMED LOOK) ---
st.markdown(r"""
<style>
[data-theme="light"] .stApp, .stApp {
    background: linear-gradient(135deg, #d1e9ff 0%, #e1d5f5 50%, #ffffff 100%) !important;
}
[data-theme="dark"] .stApp, [data-theme="dark"] [data-testid="stHeader"] {
    background-color: #000000 !important;
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
    st.markdown("<p style='text-align: center;'>Ask for some Arduino help or an image!</p>", unsafe_allow_html=True)
else:
    for message in st.session_state.all_chats[st.session_state.current_chat]:
        avatar = LOGO_PATH if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# --- 8. CHAT INPUT BAR (THE FIX) ---
if prompt := st.chat_input("Message Peepo 3..."):
    if st.session_state.current_chat is None:
        new_title = prompt[:25] + "..." if len(prompt) > 25 else prompt
        st.session_state.current_chat = new_title
        st.session_state.all_chats[new_title] = []
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    try:
        response = client.models.generate_content(model="gemini-3.1-flash-lite-preview", contents=prompt)
        text_output = response.text
        
        # 🚀 NEW HANDLER LOGIC:
        # Check if the output is the raw "dalle.text2im" plan
        if 'action": "dalle.text2im' in text_output:
            with st.spinner("✨ Peepo is contacting DALL-E..."):
                try:
                    # 1. Parse the plan from the text string
                    # We look for the JSON block starting with { "action": ... }
                    start_index = text_output.find('{"action":')
                    if start_index != -1:
                        tool_call_str = text_output[start_index:]
                        tool_call = json.loads(tool_call_str)
                        
                        # 2. Extract the prompt
                        action_input = json.loads(tool_call['action_input'])
                        actual_prompt = action_input['prompt']
                        
                        # 3. Request the image from Imagen loop (DALL-E)
                        image_response = client.models.generate_content(
                            model="gemini-3-flash", # Use standard Flash for image tools
                            contents=f"draw an image of: {actual_prompt}"
                        )
                        
                        # 4. Display the image and store the proper assistant message
                        # We use simple st.image so it appears immediately after generation
                        st.image(image_response.image_part, caption=f"✨ Result for: '{prompt}'", use_container_width=True)
                        st.session_state.all_chats[st.session_state.current_chat].append({
                            "role": "assistant", 
                            "content": f"Here is the result I generated for '{actual_prompt}'."
                        })
                    else:
                        st.error("🚦 The model planned an image but I failed to extract the prompt.")
                except Exception as tool_e:
                    st.error(f"⚠️ Failed to bridge to DALL-E: {tool_e}")
        else:
            # Normal chat output
            st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": text_output})
        
        st.rerun() 
    except Exception as e:
        if "429" in str(e):
            st.error("🚦 Peepo is busy (Rate Limit). Please wait 60 seconds!")
        else:
            st.error(f"⚠️ Error: {e}")
