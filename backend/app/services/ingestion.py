import os
from pathlib import Path
from typing import Optional
from uuid import uuid4

from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
from pypdf import PdfReader

from app.db import (
    create_document,
    create_document_chunks,
    get_connection,
    get_or_create_default_case,
    get_or_create_system_user,
)


UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./data/uploads"))
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))


def _ensure_upload_dir() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _extract_pdf_text(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    pages_text = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages_text.append(text)
    return "\n".join(pages_text).strip()


def _split_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = [chunk.strip() for chunk in splitter.split_text(text) if chunk.strip()]
    return chunks


def _generate_embeddings(chunks: list[str]) -> tuple[list[Optional[list[float]]], bool]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return [None for _ in chunks], False

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=EMBED_MODEL, input=chunks)
    embeddings = [item.embedding for item in response.data]
    return embeddings, True


async def ingest_pdf(
    file,
    case_id: Optional[str],
    document_type: Optional[str],
) -> dict[str, object]:
    _ensure_upload_dir()

    suffix = Path(file.filename or "document.pdf").suffix
    if suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported")

    stored_name = f"{uuid4()}{suffix}"
    stored_path = UPLOAD_DIR / stored_name
    content = await file.read()
    stored_path.write_bytes(content)

    text = _extract_pdf_text(stored_path)
    if not text:
        raise ValueError("No text could be extracted from the PDF")

    chunks = _split_text(text)
    embeddings, embeddings_created = _generate_embeddings(chunks)

    with get_connection() as connection:
        if not case_id:
            user_id = get_or_create_system_user(connection)
            case_id = get_or_create_default_case(connection, user_id)

        document_id = create_document(
            connection,
            case_id=case_id,
            filename=file.filename or stored_name,
            file_path=str(stored_path),
            document_type=document_type,
        )
        chunk_count = create_document_chunks(
            connection,
            document_id=document_id,
            chunks=chunks,
            embeddings=embeddings,
        )

    return {
        "document_id": document_id,
        "case_id": case_id,
        "filename": file.filename or stored_name,
        "stored_path": str(stored_path),
        "chunk_count": chunk_count,
        "embeddings_created": embeddings_created,
    }
