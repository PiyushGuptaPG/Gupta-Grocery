import io
import os
import streamlit as st
import pandas as pd
import google.generativeai as genai

# ---------------- Sidebar: settings ----------------
st.sidebar.image("Gupta Kirana logo.png", use_column_width=True)
st.sidebar.title("Bot Settings")

MODEL_NAME = st.sidebar.selectbox(
    "Model",
    ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
    index=1,
    key="gemini_model"
)

API_KEY = st.sidebar.text_input("Gemini API Key", type="password")

# ---------------- Header ----------------
st.title("CSV Chatbot — Gupta Kirana")
st.caption("Upload a CSV and ask questions about it.")

# ---------------- File upload ----------------
uploaded = st.file_uploader("Upload CSV", type=["csv"])

# ---------------- Key check ----------------
if not API_KEY:
    st.info("Please add your Google API key to continue.")
    st.stop()

genai.configure(api_key=API_KEY)
gmodel = genai.GenerativeModel(MODEL_NAME)

# ---------------- Session state ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None
if "chat" not in st.session_state:
    st.session_state.chat = gmodel.start_chat(history=[])

# ---------------- Load CSV into DataFrame ----------------
def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)

if uploaded is not None:
    try:
        st.session_state.df = load_csv(uploaded)
        if not any(m["role"] == "assistant" for m in st.session_state.messages):
            st.session_state.messages.append({
                "role": "assistant",
                "content": "CSV uploaded! Ask me anything about this dataset."
            })
    except Exception as e:
        st.error(f"Could not read CSV: {e}")

# ---------------- Helper: build context from DataFrame ----------------
def df_context_text(df: pd.DataFrame, max_rows: int = 2000, sample_rows: int = 200) -> str:
    """
    If the CSV is small, include the whole CSV text.
    Otherwise, include schema + head/tail + random sample for grounding.
    """
    buffer = io.StringIO()
    size_estimate = df.shape[0] * (len(df.columns) + 1)

    schema = " | ".join([f"{c} ({str(t)})" for c, t in zip(df.columns, df.dtypes)])
    head_txt = df.head(10).to_csv(index=False)
    tail_txt = df.tail(10).to_csv(index=False)

    if df.shape[0] <= max_rows:
        df.to_csv(buffer, index=False)
        csv_text = buffer.getvalue()
        return f"""[SCHEMA]\n{schema}\n\n[CSV_FULL]\n{csv_text}"""
    else:
        sample = df.sample(min(sample_rows, len(df)), random_state=42)
        return (
            f"[SCHEMA]\n{schema}\n\n"
            f"[HEAD]\n{head_txt}\n"
            f"[TAIL]\n{tail_txt}\n"
            f"[SAMPLE_{len(sample)}ROWS]\n{sample.to_csv(index=False)}"
        )

# ---------------- Render chat history ----------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- Chat input ----------------
prompt = st.chat_input("Ask about the CSV (e.g., top categories, summary, outliers, trends)")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if st.session_state.df is None:
        st.error("Please upload a CSV first.")
    else:
        context = df_context_text(st.session_state.df)

        system_prompt = f"""
You are a careful data assistant. Use the CSV context to answer.
- Show calculations clearly and be concise.
- When aggregating, say exactly which columns you grouped by.
- If the context sample may miss rows, state that results are approximate.
- Prefer bullet points and small tables when helpful.

{context}

Now answer the user's question:
{prompt}
"""
        try:
            response = st.session_state.chat.send_message(system_prompt)
            reply = response.text
        except Exception as e:
            reply = f"Sorry, something went wrong: {e}"

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply) 