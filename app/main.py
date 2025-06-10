import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.vector_store import build_vector_store, load_vector_store
from core.agent import CodeAgent
from core.github_loader import clone_remote_repo
from core.history_handler import save_history, load_history

st.title("🧠 RAG Code Agent")

# Load previous history
history = load_history()

# Use a selectbox to show suggestions, but allow manual typing
selected_repo = st.selectbox("Previously Used Repos", [""] + history["repos"] )
github_url = st.text_input("Paste your GitHub Repo URL", value=selected_repo)
  
if github_url in history["repos"]:
    st.info("This repo has been used before. You can load it directly.")
    
github_token = st.text_input("Enter your GitHub Access Token (if private)", type="password")

repo_path = None

if st.button("Load Repo"):
    if github_url:
        os.environ["DYNAMIC_GITHUB_URL"] = github_url
        if github_token:
            os.environ["GITHUB_TOKEN"] = github_token
            os.environ["GITHUB_PRIVATE_REPO"] = "true"
        else:
            os.environ["GITHUB_PRIVATE_REPO"] = "false"

        st.info("Cloning and indexing repo. This may take a few seconds...")

        try:
            repo_path = clone_remote_repo(github_url)
            build_vector_store(repo_path=repo_path)
            load_vector_store()
            st.success("Repo loaded and indexed successfully!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Prompt suggestion
selected_prompt = st.selectbox("Previous Prompts", [""] + history["prompts"])
prompt = st.text_area("Ask a question about the code", value=selected_prompt)

if st.button("Run Agent") and prompt:
    agent = CodeAgent()

    answer = agent.run(prompt)
    print(prompt)
    st.write("### ✅ AI Agent Response")
    st.write(answer)

    # Save to history
    save_history(github_url, prompt)
