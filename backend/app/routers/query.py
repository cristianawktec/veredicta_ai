from fastapi import APIRouter, HTTPException

from app.schemas import QueryRequest, QueryResponse
from app.services.query import run_rag_query


router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
def run_query(payload: QueryRequest) -> QueryResponse:
    try:
        result = run_rag_query(payload.question, payload.top_k)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Failed to execute RAG query") from exc

    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence_score=result["confidence_score"],
    )
