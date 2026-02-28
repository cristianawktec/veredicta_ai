"""
Test Gemini embeddings generation
TESTE CRÍTICO 2: Embeddings com Google Gemini
"""
import os
import pytest


@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "test_api_key",
    reason="Requires real GEMINI_API_KEY"
)
def test_gemini_embeddings_generated():
    """
    TESTE CRÍTICO 2: Validar que embeddings Gemini são gerados
    - Google Gemini responde
    - Embeddings têm dimensão 768
    - API key funciona
    """
    import google.generativeai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_EMBED_MODEL", "models/text-embedding-004")
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Test text
    test_text = "Teste de embedding para Veredicta AI"
    
    # Generate embedding
    result = genai.embed_content(
        model=model,
        content=test_text,
        task_type="retrieval_document"
    )
    
    embedding = result['embedding']
    
    # Assertions
    assert embedding is not None
    assert isinstance(embedding, list)
    assert len(embedding) == 768  # Gemini text-embedding-004 dimension
    assert all(isinstance(x, float) for x in embedding)
    
    print(f"✅ Gemini embedding generated: {len(embedding)} dimensions")
    print(f"✅ First 5 values: {embedding[:5]}")


def test_embedding_dimension():
    """Test that configured embedding dimension is correct"""
    # This validates the SQL schema matches Gemini
    expected_dimension = 768
    
    # Read from init.sql to verify
    from pathlib import Path
    init_sql = Path(__file__).parent.parent / "docker" / "init.sql"
    
    if init_sql.exists():
        content = init_sql.read_text()
        # Check if vector(768) is in the schema
        assert f"vector({expected_dimension})" in content
        print(f"✅ Database schema configured for {expected_dimension} dimensions")
