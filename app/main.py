# app/main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from core.agent import CodeAgent

def main():
    st.set_page_config(page_title="RAG Code Assistant", layout="wide")
    st.title("🧠 RAG Code Assistant")

    agent = CodeAgent()

    user_input = st.text_area("Enter your prompt:", height=150)

    if st.button("Generate Answer") and user_input.strip():
        with st.spinner("Thinking..."):
            response = agent.run(user_input)
        st.markdown("### 💡 Response:")
        st.code(response, language='markdown')

if __name__ == "__main__":
    main()
