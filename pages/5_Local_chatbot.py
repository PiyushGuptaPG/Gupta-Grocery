import streamlit as st
import ollama

# ---------------- Sidebar ----------------
st.sidebar.image("Gupta Kirana logo.png", use_column_width=True)
st.sidebar.title("Bot Settings")

with st.sidebar:
    model = st.text_input("Model Name", value="gemma:2b", key="model_name")
    st.markdown("⚡ Make sure your Ollama model is running locally")

# ---------------- Header ----------------
st.title("Gupta Kirana Local ChatBot")
st.caption("Hello from Gemma Chatbot powered by Ollama 🚀")

# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]

# Render past messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- Chat Input ----------------
if prompt := st.chat_input("Type your message here..."):
    if not model:
        st.info("Please add your model name to continue")
        st.stop()

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Query Ollama
    with st.spinner("🤖 Bot is thinking..."):
        try:
            response = ollama.chat(model=model, messages=st.session_state.messages)
            answer = response["message"]["content"]
        except Exception as e:
            answer = f"⚠️ Error: {e}"

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)