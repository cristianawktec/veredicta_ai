from datetime import datetime, timezone

from fastapi import APIRouter


router = APIRouter(tags=["metrics"])


@router.get("/metrics")
def metrics() -> dict[str, object]:
    return {
        "service": "veredicta-ai",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "latency_ms": None,
        "requests_count": 0,
        "avg_confidence_score": None,
    }
