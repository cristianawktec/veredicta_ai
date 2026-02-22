from fastapi import APIRouter

from app.schemas import AutonomousReviewRequest, AutonomousReviewResponse


router = APIRouter(tags=["review"])


@router.post("/run-autonomous-review", response_model=AutonomousReviewResponse)
def run_autonomous_review(
    payload: AutonomousReviewRequest,
) -> AutonomousReviewResponse:
    return AutonomousReviewResponse(
        report=(
            "Orquestração multi-agent ainda não implementada. Endpoint ativo para "
            "evolução na Fase 4."
        ),
        status="pending_implementation",
    )
