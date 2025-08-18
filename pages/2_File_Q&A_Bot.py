import streamlit as st
import google.generativeai as genai

# --- Sidebar: branding & settings ---
st.sidebar.image("Gupta Kirana logo.png", use_column_width=True)
st.sidebar.title("Bot Settings")
selected_model = st.sidebar.selectbox(
    "Select Your Model",
    ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
    key="gemini_model"
)
gemini_api_key = st.sidebar.text_input("Gemini API Key", key="gemini_api_key", type="password")

# --- Header ---
st.title("File Q&A with Gupta Kirana Gemini Bot")
st.caption("Chat with your uploaded file")

# --- File upload ---
uploaded_file = st.file_uploader("Upload your file here", type=("txt", "md"))

# --- API key check ---
if not gemini_api_key:
    st.info("Please add your Google API key to continue")
    st.stop()

genai.configure(api_key=gemini_api_key)
gmodel = genai.GenerativeModel(selected_model)

# --- Session state init ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "article_text" not in st.session_state:
    st.session_state.article_text = ""
if "chat" not in st.session_state:
    # keep one persistent chat for context
    st.session_state.chat = gmodel.start_chat(history=[])

# --- Read uploaded file ---
if uploaded_file:
    try:
        st.session_state.article_text = uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception as e:
        st.error(f"Could not read file: {e}")
    else:
        if not any(m["role"] == "assistant" for m in st.session_state.messages):
            st.session_state.messages.append({
                "role": "assistant",
                "content": "File uploaded! You can now ask questions about it."
            })

# --- Render history ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- Chat input ---
if prompt := st.chat_input("Ask me something about the file"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if st.session_state.article_text.strip():
        chat_prompt = f"""
You are an AI assistant helping summarize and explain files.
Here is the file content:
<article>
{st.session_state.article_text}
</article>

Now answer this question clearly and concisely:
{prompt}
"""
        try:
            response = st.session_state.chat.send_message(chat_prompt)
            reply = response.text
        except Exception as e:
            reply = f"Sorry, something went wrong: {e}"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
    else:
        st.error("Please upload a file first.")