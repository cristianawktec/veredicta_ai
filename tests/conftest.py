"""
Pytest configuration and fixtures
"""
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.main import app


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def sample_pdf_path():
    """Path to a sample PDF for testing"""
    # You can add a real test PDF here
    return Path(__file__).parent / "fixtures" / "sample.pdf"


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set test environment variables"""
    monkeypatch.setenv("GEMINI_API_KEY", "test_api_key")
    monkeypatch.setenv("GEMINI_EMBED_MODEL", "models/text-embedding-004")
    monkeypatch.setenv("DATABASE_URL", os.getenv("DATABASE_URL", "postgresql+psycopg2://veredicta_user:veredicta_pass@localhost:5432/veredicta_test"))
