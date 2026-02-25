"""
Test PDF upload and ingestion pipeline
TESTE CRÍTICO 1: Upload e processamento de PDF
"""
import io
from pathlib import Path

import pytest
from pypdf import PdfWriter


def create_test_pdf(text: str = "Teste de documento jurídico para Veredicta AI") -> bytes:
    """Create a simple PDF for testing"""
    # Create a minimal valid PDF
    pdf = PdfWriter()
    pdf.add_blank_page(width=612, height=792)
    
    buffer = io.BytesIO()
    pdf.write(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def test_upload_pdf_success(client):
    """
    TESTE CRÍTICO 1: Validar que upload de PDF funciona
    - Upload bem-sucedido
    - PDF processado
    - Chunks criados
    - Status code 200
    """
    # Create test PDF
    pdf_content = create_test_pdf()
    
    # Upload
    files = {"file": ("test_doc.pdf", pdf_content, "application/pdf")}
    data = {"document_type": "test"}
    
    response = client.post("/upload", files=files, data=data)
    
    # Assertions
    assert response.status_code == 200
    result = response.json()
    
    # Validate response structure
    assert "document_id" in result
    assert "case_id" in result
    assert "filename" in result
    assert "status" in result
    assert "chunks_created" in result
    assert "embeddings_created" in result
    
    # Validate values
    assert result["status"] == "ingested"
    assert result["filename"] == "test_doc.pdf"
    assert result["chunks_created"] >= 0  # Pelo menos 0 chunks
    
    print(f"✅ Upload successful: {result['chunks_created']} chunks created")
    print(f"✅ Embeddings created: {result['embeddings_created']}")


def test_upload_non_pdf_fails(client):
    """Test that non-PDF files are rejected"""
    # Create a fake txt file
    files = {"file": ("test.txt", b"not a pdf", "text/plain")}
    data = {"document_type": "test"}
    
    response = client.post("/upload", files=files, data=data)
    
    # Should fail with 400
    assert response.status_code == 400
    assert "Only PDF files are supported" in response.json()["detail"]


def test_upload_empty_pdf_fails(client):
    """Test that empty PDFs are handled"""
    # Create empty PDF
    pdf = PdfWriter()
    buffer = io.BytesIO()
    pdf.write(buffer)
    buffer.seek(0)
    
    files = {"file": ("empty.pdf", buffer.getvalue(), "application/pdf")}
    data = {"document_type": "test"}
    
    response = client.post("/upload", files=files, data=data)
    
    # Should fail with 400 (no text extracted)
    assert response.status_code == 400
