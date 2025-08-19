import streamlit as st
import google.generativeai as genai
import os

# ---------------- Sidebar: Branding + Settings ----------------
st.sidebar.image("Gupta Kirana logo.png", use_column_width=True)
st.sidebar.title("Bot Settings")

with st.sidebar:
    selected_model = st.selectbox(
        "Select Your Model",
        ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
        key="gemini_model"
    )
    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")

# ---------------- Header ----------------
st.title("Gupta Kirana Bot")
st.caption("Hello from Gemini Bot By Gupta Kirana")

# ---------------- API Key Check ----------------
if not gemini_api_key:
    st.info("Please add your Google API key in the sidebar to continue.")
    st.stop()

genai.configure(api_key=gemini_api_key)

# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# ---------------- Show Chat History ----------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- Chat Input ----------------
if prompt := st.chat_input():
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Create model and start chat
    model_obj = genai.GenerativeModel(selected_model)
    chat = model_obj.start_chat(history=[])

    # Get response
    response = chat.send_message(prompt)
    reply = response.text

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)