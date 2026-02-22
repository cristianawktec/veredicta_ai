# Arquitetura Base — Veredicta AI

## Camadas

1. Ingestion Layer
2. Embedding & Vector Storage
3. RAG Engine
4. Multi-Agent Orchestration
5. Guardrails & Evaluation
6. API Layer
7. Deployment Layer

## Estado atual

- Fase 1 inicializada
- API FastAPI disponível com endpoints base
- Banco PostgreSQL com `pgvector` habilitado via Docker
- Tabelas `documents` e `chunks` criadas no bootstrap

## Evolução planejada

- Fase 2: Ingestion + Embeddings
- Fase 3: RAG Engine
- Fase 4: Multi-Agent com LangGraph
- Fase 5: Guardrails + RAGAS
- Fase 6: API completa e métricas reais
- Fase 7: Deploy AWS + Nginx
