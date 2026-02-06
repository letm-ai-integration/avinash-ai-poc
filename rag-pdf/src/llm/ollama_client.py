import ollama
from src.config.settings import OLLAMA_MODEL

def ask_ollama(context, question):
    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    

    return response["message"]["content"]
