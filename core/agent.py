# agent/code_agent.py
from core.vector_store import vector_store_instance
from core.vector_store import load_vector_store
from core.utillls import load_config
from dotenv import load_dotenv
import os 
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
print(f"Using Groq API Key: {groq_api_key}")
# from openai import OpenAI
from groq import Groq

CONFIG = load_config()

class CodeAgent:
    def __init__(self):
        self.client = Groq(api_key=groq_api_key)
        self.model = CONFIG['llm']['model']
        self.temperature = CONFIG['llm']['temperature']
        self.max_tokens = CONFIG['llm']['max_tokens']
        load_vector_store()

    def build_prompt(self, user_query, context_chunks):
        system_prompt = CONFIG['agent']['system_prompt']
        context = "\n\n".join([chunk['content'] for chunk in context_chunks])
        full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser Query:\n{user_query}"
        return full_prompt

    def run(self, query: str) -> str:
        chunks = vector_store_instance.search(query)
        prompt = self.build_prompt(query, chunks)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": CONFIG['agent']['system_prompt']},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content.strip()

# Example usage:
if __name__ == "__main__":
    agent = CodeAgent()
    query = "Create an MVC structure for Header"
    answer = agent.run(query)
    print("\n=== AI Agent Response ===\n")
    print(answer)
