"""
Test query endpoint behavior
"""


def test_query_success_with_mocked_service(client, monkeypatch):
    def fake_run_rag_query(question: str, top_k: int):
        assert question == "Qual o resumo do documento?"
        assert top_k == 3
        return {
            "answer": "Resumo preliminar.",
            "sources": ["contrato.pdf [chunk 0]"],
            "confidence_score": 0.81,
        }

    monkeypatch.setattr("app.routers.query.run_rag_query", fake_run_rag_query)

    response = client.post(
        "/query",
        json={"question": "Qual o resumo do documento?", "top_k": 3},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"] == "Resumo preliminar."
    assert payload["sources"] == ["contrato.pdf [chunk 0]"]
    assert payload["confidence_score"] == 0.81


def test_query_returns_503_when_service_fails(client, monkeypatch):
    def fake_run_rag_query(_question: str, _top_k: int):
        raise RuntimeError("service unavailable")

    monkeypatch.setattr("app.routers.query.run_rag_query", fake_run_rag_query)

    response = client.post(
        "/query",
        json={"question": "Teste de falha controlada", "top_k": 2},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "Failed to execute RAG query"
