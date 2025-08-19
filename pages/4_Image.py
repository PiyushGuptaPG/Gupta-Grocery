
# import streamlit as st
# from google import genai
# from google.genai import types
# from PIL import Image
# from io import BytesIO
# import base64

# # ---------------- Sidebar: settings ----------------
# st.sidebar.image("Gupta Kirana logo.png", use_column_width=True)
# st.sidebar.title("Bot Settings")

# with st.sidebar:
#     gemini_api_key = st.text_input("Gemini API key", key="gemini_api_key", type="password")


# # ---------------- Header ----------------
# st.title("Create with Gupta Kirana")
# st.caption("Create attractive images on Gemini on Gupta Kirana ImageBot.")


# if 'messages' not in st.session_state:
#     st.session_state.messages = [{"role": "assistant", "content": "Hello"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# # if prompt := st.chat_input():

#     if not gemini_api_key:
#         st.info("Please add your Google API to continue.")
#         st.stop()

#     client = genai.Client()

#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     response = client.models.generate_content(
#         model="gemini-2.0-flash-preview-image-generation",
#         contents=prompt,
#         config=types.GenerateContentConfig(
#             response_modalities=["TEXT", "IMAGE"]
#         )
#     )

#     for part in response.candidates[0].content.parts:
#         if part.text is not None:
#             st.session_state.messages.append({"role": "assistant", "content": part.text})
#             st.chat_message("assistant").write(part.text)
#         elif part.inline_data is not None: 
#             image = Image.open(BytesIO(base64.b64decode(part.inline_data.data)))
#             st.image(image, caption="Generated Image")

import streamlit as st
from google import genai
from google.genai import types

st.sidebar.image("Gupta Kirana logo.png", use_column_width=True)
st.sidebar.title("Bot Settings")
with st.sidebar:
    gemini_api_key = st.text_input("Gemini API key", key="gemini_api_key", type="password")

st.title("Create with Gupta Kirana")
st.caption("Gemini demo (text only — image generation not available via public SDK).")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Describe what you want (text response)"):
    if not gemini_api_key:
        st.info("Please add your Google API key to continue.")
        st.stop()

    client = genai.Client(api_key=gemini_api_key)  # ✅ API key passed

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Use a valid text model
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(response_modalities=["TEXT"])
    )

    text = response.candidates[0].content.parts[0].text if response.candidates else "No response."
    st.session_state.messages.append({"role": "assistant", "content": text})
    st.chat_message("assistant").write(text)