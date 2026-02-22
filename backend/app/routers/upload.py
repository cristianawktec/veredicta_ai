from uuid import uuid4

from fastapi import APIRouter, File, UploadFile

from app.schemas import UploadResponse


router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    document_id = str(uuid4())
    return UploadResponse(
        document_id=document_id,
        filename=file.filename,
        status="received",
    )
