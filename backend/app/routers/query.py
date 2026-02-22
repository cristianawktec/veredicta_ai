from fastapi import APIRouter

from app.schemas import QueryRequest, QueryResponse


router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
def run_query(payload: QueryRequest) -> QueryResponse:
    return QueryResponse(
        answer=(
            "Pipeline RAG ainda não implementado. Esta resposta confirma que a API "
            "base está pronta para a Fase 3."
        ),
        sources=[],
        confidence_score=0.0,
    )
