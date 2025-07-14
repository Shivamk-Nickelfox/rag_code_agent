import streamlit as st
import os
import time
import uuid
import tempfile
import shutil
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.vector_store import build_vector_store, load_vector_store
from core.agent import CodeAgent

st.set_page_config(layout="wide")

# --- Session State ---
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# --- Chat Sidebar with History ---
st.sidebar.title("💬 Chats")

for chat_id, chat_data in st.session_state.chat_sessions.items():
    col1, col2 = st.sidebar.columns([0.8, 0.2])
    if col1.button(chat_data["title"], key=chat_id):
        st.session_state.current_chat_id = chat_id
    if col2.button("❌", key=f"del_{chat_id}"):
        del st.session_state.chat_sessions[chat_id]
        if st.session_state.current_chat_id == chat_id:
            st.session_state.current_chat_id = None
        st.rerun()

if st.sidebar.button("➕ New Chat"):
    new_id = str(uuid.uuid4())
    st.session_state.chat_sessions[new_id] = {
        "title": f"Chat {len(st.session_state.chat_sessions)+1}",
        "messages": []
    }
    st.session_state.current_chat_id = new_id
    st.rerun()

# --- Main Chat Interface ---
if st.session_state.current_chat_id:
    chat_id = st.session_state.current_chat_id
    chat_data = st.session_state.chat_sessions[chat_id]
    st.title(chat_data["title"])

    # --- ZIP Upload ---
    uploaded_file = st.file_uploader("Upload your codebase ZIP", type="zip")
    if uploaded_file:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "uploaded.zip")
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            shutil.unpack_archive(zip_path, tmpdir)
            build_vector_store(tmpdir)
            load_vector_store()
            st.success("Codebase indexed.")

    # --- Prompt Box ---
    prompt = st.chat_input("Ask something about your code")
    if prompt:
        agent = CodeAgent()
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            placeholder = st.empty()
            response = ""
            for chunk in agent.run(prompt):  # Assumes streaming support
                response += chunk
                placeholder.markdown(response + "▌")
            placeholder.markdown(response)

        chat_data["messages"].append({"role": "user", "content": prompt})
        chat_data["messages"].append({"role": "assistant", "content": response})

    # --- Display past chat ---
    for msg in chat_data.get("messages", []):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

else:
    st.title("💬 Please create or select a chat from the sidebar")
