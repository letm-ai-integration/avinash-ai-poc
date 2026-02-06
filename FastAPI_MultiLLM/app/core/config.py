import os
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.environ["HF_API_TOKEN"]
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
