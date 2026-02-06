from openai import OpenAI
from groq import Groq
from app.core.config import HF_API_TOKEN, GROQ_API_KEY

hf_client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_TOKEN,
)

groq_client = Groq(api_key=GROQ_API_KEY)
