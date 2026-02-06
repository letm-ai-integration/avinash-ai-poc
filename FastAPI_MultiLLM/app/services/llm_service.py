from app.core.clients import hf_client, groq_client
from app.llms.registry import AVAILABLE_MODELS
from app.models.schemas import QueryRequest


def query_llm(request: QueryRequest) -> str:
    model_info = AVAILABLE_MODELS[request.model_name]
    provider = model_info["provider"]
    model_id = model_info["model_id"]

    if provider == "huggingface":
        completion = hf_client.chat.completions.create(
            model=model_id,
            messages=[m.dict() for m in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return completion.choices[0].message.content

    if provider == "groq":
        completion = groq_client.chat.completions.create(
            model=model_id,
            messages=[m.dict() for m in request.messages],
            temperature=request.temperature,
            max_completion_tokens=request.max_tokens,
            top_p=1,
            reasoning_effort="medium",
            stream=False,
        )
        return completion.choices[0].message.content

    raise ValueError("Unsupported provider")
