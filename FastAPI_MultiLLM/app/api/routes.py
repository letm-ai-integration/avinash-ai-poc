from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.llms.registry import AVAILABLE_MODELS
from app.services.llm_service import query_llm

router = APIRouter()


@router.get("/models")
def list_models():
    return {"available_models": list(AVAILABLE_MODELS.keys())}


@router.post("/query", response_model=QueryResponse)
def query_model(request: QueryRequest):
    if request.model_name not in AVAILABLE_MODELS:
        raise HTTPException(status_code=404, detail="Model not found")

    answer = query_llm(request)
    return QueryResponse(model_name=request.model_name, response=answer)
