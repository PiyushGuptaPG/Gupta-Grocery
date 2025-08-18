import streamlit as st
import google.generativeai as genai
# Install Google GenAI SDK 




st.sidebar.image("Gupta Kirana logo.png", use_column_width=True)

st.sidebar.title('Bot Settings')

with st.sidebar:
    model = st.selectbox(
        "Select Your Model",
        ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
        key="gemini_model"
    )
    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")

st.title("Gupta Kirana Bot")
st.caption("Hello from Gemini Bot By Gupta Kirana")


if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistance", "content": "Hello! How can I assist You Today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    if not gemini_api_key:
        st.info("Please add your Google API key to continue.")
        st.stop()

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(model)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)


    st.session_state.messages.append({"role": "assistance", "content": response.text})
    st.chat_message("assistant").write(response.text)