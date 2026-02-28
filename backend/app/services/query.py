import os
from time import perf_counter
from typing import Optional
from uuid import uuid4

import google.generativeai as genai
from sqlalchemy import text

from app.db import get_connection, get_or_create_default_case, get_or_create_system_user


EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "models/text-embedding-004")


def _generate_query_embedding(question: str) -> Optional[list[float]]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    genai.configure(api_key=api_key)
    result = genai.embed_content(
        model=EMBED_MODEL,
        content=question,
        task_type="retrieval_query",
    )
    embedding = result.get("embedding")
    return embedding if isinstance(embedding, list) else None


def _retrieve_chunks(connection, query_embedding: Optional[list[float]], top_k: int) -> list[dict[str, object]]:
    if query_embedding:
        rows = connection.execute(
            text(
                """
                SELECT
                    dc.id,
                    dc.chunk_index,
                    dc.content,
                    d.filename,
                    (dc.embedding <=> :query_embedding) AS distance
                FROM document_chunks dc
                JOIN documents d ON d.id = dc.document_id
                WHERE dc.embedding IS NOT NULL
                ORDER BY dc.embedding <=> :query_embedding
                LIMIT :top_k
                """
            ),
            {"query_embedding": query_embedding, "top_k": top_k},
        ).fetchall()
    else:
        rows = connection.execute(
            text(
                """
                SELECT
                    dc.id,
                    dc.chunk_index,
                    dc.content,
                    d.filename,
                    NULL::float AS distance
                FROM document_chunks dc
                JOIN documents d ON d.id = dc.document_id
                ORDER BY dc.created_at DESC
                LIMIT :top_k
                """
            ),
            {"top_k": top_k},
        ).fetchall()

    chunks: list[dict[str, object]] = []
    for row in rows:
        chunks.append(
            {
                "id": str(row[0]),
                "chunk_index": int(row[1]),
                "content": str(row[2]),
                "filename": str(row[3]),
                "distance": float(row[4]) if row[4] is not None else None,
            }
        )
    return chunks


def _build_answer(question: str, chunks: list[dict[str, object]]) -> str:
    if not chunks:
        return (
            "Não encontrei conteúdo processado para responder à pergunta. "
            "Faça upload de pelo menos um PDF e tente novamente."
        )

    excerpts = []
    for chunk in chunks[:3]:
        text_excerpt = str(chunk["content"]).replace("\n", " ").strip()
        excerpts.append(f"- {text_excerpt[:280]}")

    excerpts_text = "\n".join(excerpts)
    return (
        f"Pergunta: {question}\n\n"
        "Resposta preliminar baseada nos trechos recuperados:\n"
        f"{excerpts_text}"
    )


def _build_sources(chunks: list[dict[str, object]]) -> list[str]:
    seen = set()
    sources: list[str] = []

    for chunk in chunks:
        source = f"{chunk['filename']} [chunk {chunk['chunk_index']}]"
        if source not in seen:
            seen.add(source)
            sources.append(source)

    return sources


def _calculate_confidence(chunks: list[dict[str, object]]) -> float:
    distances = [chunk["distance"] for chunk in chunks if chunk["distance"] is not None]
    if not distances:
        return 0.5 if chunks else 0.0

    avg_distance = sum(distances) / len(distances)
    confidence = 1.0 - avg_distance
    confidence = max(0.0, min(confidence, 1.0))
    return round(confidence, 3)


def _persist_query_response(
    connection,
    *,
    question: str,
    confidence_score: float,
    latency_ms: int,
    chunks: list[dict[str, object]],
) -> None:
    user_id = get_or_create_system_user(connection)
    case_id = get_or_create_default_case(connection, user_id)

    query_id = str(uuid4())
    response_id = str(uuid4())

    connection.execute(
        text(
            """
            INSERT INTO queries (id, case_id, user_id, query_text, mode)
            VALUES (:id, :case_id, :user_id, :query_text, :mode)
            """
        ),
        {
            "id": query_id,
            "case_id": case_id,
            "user_id": user_id,
            "query_text": question,
            "mode": "rag",
        },
    )

    connection.execute(
        text(
            """
            INSERT INTO responses (id, query_id, response_text, confidence_score, latency_ms)
            VALUES (:id, :query_id, :response_text, :confidence_score, :latency_ms)
            """
        ),
        {
            "id": response_id,
            "query_id": query_id,
            "response_text": "RAG query executed",
            "confidence_score": confidence_score,
            "latency_ms": latency_ms,
        },
    )

    for chunk in chunks:
        similarity_score = None
        if chunk["distance"] is not None:
            similarity_score = max(0.0, min(1.0, 1.0 - float(chunk["distance"])))

        connection.execute(
            text(
                """
                INSERT INTO retrieved_chunks (id, query_id, chunk_id, similarity_score)
                VALUES (:id, :query_id, :chunk_id, :similarity_score)
                """
            ),
            {
                "id": str(uuid4()),
                "query_id": query_id,
                "chunk_id": chunk["id"],
                "similarity_score": similarity_score,
            },
        )


def run_rag_query(question: str, top_k: int) -> dict[str, object]:
    cleaned_question = question.strip()
    if len(cleaned_question) < 3:
        raise ValueError("Question must have at least 3 characters")

    started_at = perf_counter()

    query_embedding = _generate_query_embedding(cleaned_question)
    with get_connection() as connection:
        chunks = _retrieve_chunks(connection, query_embedding, top_k)

        answer = _build_answer(cleaned_question, chunks)
        sources = _build_sources(chunks)
        confidence_score = _calculate_confidence(chunks)

        latency_ms = int((perf_counter() - started_at) * 1000)
        _persist_query_response(
            connection,
            question=cleaned_question,
            confidence_score=confidence_score,
            latency_ms=latency_ms,
            chunks=chunks,
        )

    return {
        "answer": answer,
        "sources": sources,
        "confidence_score": confidence_score,
    }
