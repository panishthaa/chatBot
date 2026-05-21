import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Banking Support Chatbot",
    page_icon="💳",
    layout="centered"
)

st.title("💳 AI Banking Support Chatbot")

st.markdown(
    "Ask banking-related questions using AI + RAG"
)

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Upload Section
with st.sidebar:

    st.header("Upload Banking Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"]
    )

    if uploaded_file is not None:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue()
            )
        }

        response = requests.post(
            f"{API_URL}/upload",
            files=files
        )

        st.success(response.json()["message"])

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input(
    "Ask a banking question..."
)

if user_input:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Bot response
    loader_placeholder = st.empty()

    with loader_placeholder.container():
     st.markdown("⏳ **AI is analyzing your documents...**")
     st.progress(70)

    response = requests.post(
        f"{API_URL}/chat",
        json={"message": user_input}
    )

    loader_placeholder.empty()

    if response.status_code == 200:
        bot_response = response.json()["response"]
    else:
        bot_response = "Backend error occurred. Please check the backend terminal."
        st.error(response.text)

    st.markdown(bot_response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response
    })