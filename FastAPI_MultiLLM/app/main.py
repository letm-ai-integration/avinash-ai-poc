from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="OpenAI-Compatible Multi-Model API")

app.include_router(router)
