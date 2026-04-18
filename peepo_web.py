import streamlit as st
import google.generativeai as genai
import os

# 1. SETUP THE BRAIN (The White Hat System Prompt)
# This part makes sure the AI knows its mission is ethical hacking and defense.
SYSTEM_PROMPT = """
You are Peepo-Sec, a world-class White Hat Hacker and Cybersecurity Researcher. 
Your mission is to help the user learn how to protect devices, find vulnerabilities 
legally, and stop dangerous cyber-attacks. 

Your goals:
1. Explain how 'bad actors' think so the user can build better defenses.
2. Teach the user about Penetration Testing, Firewalls, and Digital Forensics.
3. If the user asks about dangerous people, help them understand how to protect 
   their own data and report threats to the authorities.
4. Always stay on the legal and ethical side of hacking.
"""

# 2. CONFIGURE API
# Make sure your API Key is set in your environment or Streamlit secrets
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")

# Set up the model with the latest version you are using
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # You can change this to 3.1 if supported
    system_instruction=SYSTEM_PROMPT
)

# 3. STREAMLIT UI SETUP
st.set_page_config(page_title="Peepo 3 AI - White Hat Edition", page_icon="🛡️")
st.title("🛡️ Peepo 3 AI: Security Expert")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. CHAT LOGIC
if prompt := st.chat_input("Ask Peepo-Sec about security..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Peepo-Sec
    with st.chat_message("assistant"):
        try:
            # We send the whole history to keep context
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("If you see a 503 error, the server is just busy. Wait 1 minute and refresh!")
