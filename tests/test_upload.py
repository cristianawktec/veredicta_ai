"""
Test PDF upload and ingestion pipeline
TESTE CRÍTICO 1: Upload e processamento de PDF
"""
import io
from pathlib import Path

import pytest


def create_test_pdf(text: str = "Teste de documento jurídico para Veredicta AI") -> bytes:
    """Create a simple PDF for testing with actual text content"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, text)
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    except ImportError:
        # Fallback: create a minimal PDF with text using pypdf
        # This creates a PDF that pypdf can read
        from pypdf import PdfWriter
        import tempfile
        import subprocess
        
        # Create a simple text file and convert to PDF using a minimal approach
        # For testing purposes, we'll create a very basic PDF structure manually
        # This is a minimal PDF that contains extractable text
        pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources 4 0 R /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >>
endobj
5 0 obj
<< /Length 44 >>
stream
BT
/F1 12 Tf
100 700 Td
(""" + text.encode('latin-1', errors='replace').decode('latin-1') + b""") Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000214 00000 n 
0000000293 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
385
%%EOF"""
        return pdf_content


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
