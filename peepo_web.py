# --- 8. CHAT INPUT BAR (THE FIX) ---
if prompt := st.chat_input("Message Peepo 3..."):
    if st.session_state.current_chat is None:
        new_title = prompt[:25] + "..." if len(prompt) > 25 else prompt
        st.session_state.current_chat = new_title
        st.session_state.all_chats[new_title] = []
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar=LOGO_PATH):
        try:
            # Check if user wants an image to know which quota path to take
            if 'action": "dalle.text2im' in prompt.lower() or any(x in prompt.lower() for x in ["draw", "image of", "generate image"]):
                model_for_tools = "gemini-3-flash" # Tools use standard flash quota
                tool_contents = f"dalle.text2im prompt: '{prompt}'"
                
                # Create a placeholder to give instant feedback so you don't hang
                status_placeholder = st.empty()
                status_placeholder.spinner(f"✨ Peepo is planning your image...")
                
                # Check for available tool quota
                try:
                    # Special short pre-flight call to Imagen loop
                    quota_check = client.models.generate_content(model=model_for_tools, contents="QUOTA_CHECK")
                except Exception as qc_e:
                    # THE FIX: We caught the 429 *before* Imagen logic
                    if "429" in str(qc_e):
                        status_placeholder.error("🚦 Gemini tool servers are very busy. Your image will not generate right now. Please wait 60 seconds!")
                        st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": "🚦 Generation blocked due to rate limit."})
                        st.rerun() # Stop immediately and refresh the UI
                    else:
                        raise qc_e # Pass-through other unexpected errors
                
                # Normal image generation if quota check passed
                try:
                    image_response = client.models.generate_content(model=model_for_tools, contents=tool_contents)
                    st.image(image_response.image_part, caption=f"✨ Result for: '{prompt}'", use_container_width=True)
                    st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": f"Here is the result for your request: '{prompt}'."})
                except Exception as tool_e:
                    # Final safety check for errors during Imagen generation
                    st.error(f"⚠️ Failed to bridge to DALL-E: {tool_e}")
                    
                st.rerun() # Stop immediately to prevent the prompt from appending a second time

            else:
                # Normal chat logic remains unchanged
                response = client.models.generate_content(model="gemini-3.1-flash-lite-preview", contents=prompt)
                st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": response.text})
                st.rerun() 
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
