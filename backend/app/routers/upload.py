from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas import UploadResponse
from app.services.ingestion import ingest_pdf


router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    case_id: str | None = Form(default=None),
    document_type: str | None = Form(default=None),
) -> UploadResponse:
    try:
        result = await ingest_pdf(file, case_id, document_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to ingest document") from exc

    return UploadResponse(
        document_id=result["document_id"],
        case_id=result["case_id"],
        filename=result["filename"],
        status="ingested",
        chunks_created=result["chunk_count"],
        embeddings_created=result["embeddings_created"],
    )
