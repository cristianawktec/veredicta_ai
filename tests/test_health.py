"""
Test basic API health and functionality
"""


def test_health_endpoint(client):
    """Test /health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "veredicta-ai"


def test_root_endpoint_404(client):
    """Test root endpoint returns 404 (não configurado)"""
    response = client.get("/")
    assert response.status_code == 404
