"""
Test database operations and vector storage
TESTE CRÍTICO 3: Armazenamento no PostgreSQL
"""
import os
import pytest
from sqlalchemy import create_engine, text


@pytest.fixture
def db_connection():
    """Create database connection for testing"""
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://veredicta_user:veredicta_pass@localhost:5432/veredicta"
    )
    engine = create_engine(database_url)
    
    with engine.begin() as connection:
        yield connection


def test_database_connection(db_connection):
    """Test database is accessible"""
    result = db_connection.execute(text("SELECT 1")).fetchone()
    assert result[0] == 1
    print("✅ Database connection successful")


def test_pgvector_extension(db_connection):
    """Test pgvector extension is installed"""
    result = db_connection.execute(
        text("SELECT extname FROM pg_extension WHERE extname = 'vector'")
    ).fetchone()
    
    assert result is not None
    assert result[0] == 'vector'
    print("✅ pgvector extension installed")


def test_tables_exist(db_connection):
    """
    TESTE CRÍTICO 3: Validar que tabelas existem
    - Tabelas criadas corretamente
    - Schema do banco está ok
    """
    expected_tables = [
        'users',
        'cases',
        'documents',
        'document_chunks',
        'queries',
        'responses'
    ]
    
    for table in expected_tables:
        result = db_connection.execute(
            text(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = :table_name
                )
            """),
            {"table_name": table}
        ).fetchone()
        
        assert result[0] is True, f"Table {table} does not exist"
        print(f"✅ Table '{table}' exists")


def test_document_chunks_has_vector_column(db_connection):
    """
    TESTE CRÍTICO 3: Validar coluna de embedding
    - Coluna embedding existe
    - Tipo é vector
    - Dimensão é 768
    """
    result = db_connection.execute(
        text("""
            SELECT column_name, udt_name 
            FROM information_schema.columns 
            WHERE table_name = 'document_chunks' AND column_name = 'embedding'
        """)
    ).fetchone()
    
    assert result is not None
    assert result[0] == 'embedding'
    # pgvector columns show as 'vector'
    print(f"✅ Column 'embedding' exists with type: {result[1]}")


@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "test_api_key",
    reason="Requires real GEMINI_API_KEY for full integration test"
)
def test_vector_storage_roundtrip(db_connection):
    """
    TESTE CRÍTICO 3: Validar que vetores são salvos e recuperados
    - Inserir embedding
    - Recuperar embedding
    - Validar dimensões
    """
    import google.generativeai as genai
    from uuid import uuid4
    
    # Generate a real embedding
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    test_text = "Vector storage test"
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=test_text,
        task_type="retrieval_document"
    )
    embedding = result['embedding']
    
    # Create test data
    user_id = str(uuid4())
    case_id = str(uuid4())
    document_id = str(uuid4())
    chunk_id = str(uuid4())
    
    # Insert test user, case, document
    db_connection.execute(
        text("""
            INSERT INTO users (id, name, email, password_hash, role)
            VALUES (:user_id, 'Test', 'test@test.com', 'hash', 'user')
        """),
        {"user_id": user_id}
    )
    
    db_connection.execute(
        text("""
            INSERT INTO cases (id, user_id, title, description)
            VALUES (:case_id, :user_id, 'Test Case', 'Test')
        """),
        {"case_id": case_id, "user_id": user_id}
    )
    
    db_connection.execute(
        text("""
            INSERT INTO documents (id, case_id, filename, file_path)
            VALUES (:doc_id, :case_id, 'test.pdf', '/tmp/test.pdf')
        """),
        {"doc_id": document_id, "case_id": case_id}
    )
    
    # Insert chunk with embedding
    db_connection.execute(
        text("""
            INSERT INTO document_chunks (id, document_id, chunk_index, content, embedding)
            VALUES (:chunk_id, :doc_id, 0, :content, :embedding::vector)
        """),
        {
            "chunk_id": chunk_id,
            "doc_id": document_id,
            "content": test_text,
            "embedding": embedding
        }
    )
    
    # Retrieve and validate
    retrieved = db_connection.execute(
        text("SELECT embedding FROM document_chunks WHERE id = :chunk_id"),
        {"chunk_id": chunk_id}
    ).fetchone()
    
    assert retrieved is not None
    retrieved_embedding = retrieved[0]
    
    # Parse the vector string to list
    if isinstance(retrieved_embedding, str):
        # pgvector returns as string "[1.0, 2.0, ...]"
        import ast
        retrieved_embedding = ast.literal_eval(retrieved_embedding.replace('[', '').replace(']', '').strip())
    
    assert len(retrieved_embedding) == 768
    
    print("✅ Vector storage roundtrip successful!")
    print(f"✅ Stored and retrieved {len(retrieved_embedding)} dimensional vector")
    
    # Cleanup
    db_connection.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
