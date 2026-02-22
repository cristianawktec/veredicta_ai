from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(default=5, ge=1, le=20)


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence_score: float


class AutonomousReviewRequest(BaseModel):
    case_description: str = Field(..., min_length=10)
    document_ids: list[str] = Field(default_factory=list)


class AutonomousReviewResponse(BaseModel):
    report: str
    status: str


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
