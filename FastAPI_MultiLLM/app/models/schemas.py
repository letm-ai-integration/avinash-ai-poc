from pydantic import BaseModel
from typing import List


class Message(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    model_name: str
    messages: List[Message]
    temperature: float = 0.6
    max_tokens: int = 50


class QueryResponse(BaseModel):
    model_name: str
    response: str
