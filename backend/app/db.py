import os
from contextlib import contextmanager
from typing import Iterable, Optional
from uuid import uuid4

from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://veredicta_user:veredicta_pass@postgres:5432/veredicta",
)

engine: Engine = create_engine(DATABASE_URL, pool_pre_ping=True)


@event.listens_for(engine, "connect")
def _register_vector(dbapi_connection, _connection_record) -> None:
    register_vector(dbapi_connection)


@contextmanager
def get_connection():
    with engine.begin() as connection:
        yield connection


def get_or_create_system_user(connection) -> str:
    email = os.getenv("SYSTEM_USER_EMAIL", "system@veredicta.local")
    name = os.getenv("SYSTEM_USER_NAME", "System")
    password_hash = os.getenv("SYSTEM_USER_PASSWORD_HASH", "not-set")
    role = os.getenv("SYSTEM_USER_ROLE", "system")

    existing = connection.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": email},
    ).fetchone()
    if existing:
        return str(existing[0])

    user_id = str(uuid4())
    connection.execute(
        text(
            """
            INSERT INTO users (id, name, email, password_hash, role)
            VALUES (:id, :name, :email, :password_hash, :role)
            """
        ),
        {
            "id": user_id,
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "role": role,
        },
    )
    return user_id


def get_or_create_default_case(connection, user_id: str) -> str:
    title = os.getenv("DEFAULT_CASE_TITLE", "Default Case")
    description = os.getenv("DEFAULT_CASE_DESCRIPTION", "Default case for uploads")
    existing = connection.execute(
        text(
            """
            SELECT id FROM cases
            WHERE user_id = :user_id AND title = :title
            ORDER BY created_at ASC
            LIMIT 1
            """
        ),
        {"user_id": user_id, "title": title},
    ).fetchone()
    if existing:
        return str(existing[0])

    case_id = str(uuid4())
    connection.execute(
        text(
            """
            INSERT INTO cases (id, user_id, title, description, status)
            VALUES (:id, :user_id, :title, :description, :status)
            """
        ),
        {
            "id": case_id,
            "user_id": user_id,
            "title": title,
            "description": description,
            "status": "open",
        },
    )
    return case_id


def create_document(
    connection,
    case_id: str,
    filename: str,
    file_path: str,
    document_type: Optional[str],
) -> str:
    document_id = str(uuid4())
    connection.execute(
        text(
            """
            INSERT INTO documents (id, case_id, filename, file_path, document_type)
            VALUES (:id, :case_id, :filename, :file_path, :document_type)
            """
        ),
        {
            "id": document_id,
            "case_id": case_id,
            "filename": filename,
            "file_path": file_path,
            "document_type": document_type,
        },
    )
    return document_id


def create_document_chunks(
    connection,
    document_id: str,
    chunks: Iterable[str],
    embeddings: Optional[list[Optional[list[float]]]] = None,
) -> int:
    count = 0
    for index, content in enumerate(chunks):
        embedding = None
        if embeddings and index < len(embeddings):
            embedding = embeddings[index]
        chunk_id = str(uuid4())
        connection.execute(
            text(
                """
                INSERT INTO document_chunks (id, document_id, chunk_index, content, token_count, embedding)
                VALUES (:id, :document_id, :chunk_index, :content, :token_count, :embedding)
                """
            ),
            {
                "id": chunk_id,
                "document_id": document_id,
                "chunk_index": index,
                "content": content,
                "token_count": None,
                "embedding": embedding,
            },
        )
        count += 1
    return count
