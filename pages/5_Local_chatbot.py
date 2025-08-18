import streamlit as st
import ollama

st.sidebar.image("Gupta Kirana logo.png", use_column_width=True)
st.sidebar.title("Bot Settings")

with st.sidebar:
    model = st.text_input("Model Name", value="gemma3:1b", key="model_name")
    st.markdown("Make sure your model is running")


# # ---------------- Header ----------------
st.title("Gupta Kirana Local ChatBot")
st.caption("Hello From Gemma Chatbot By Gupta Kirana.")

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not model:
        st.info("Please add your model name to continue")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Bot is Thinking...."):
        response = ollama.chat(model=model, messages=st.session_state.messages)
        answer = response['message']['content']

    st.session_state.messages.append({"role": "assistant", "content": prompt})
    st.chat_message("assistant").write(answer)