# Veredicta AI

Plataforma modular de IA generativa para inteligência documental jurídica.

## Estrutura inicial

- `backend/` API FastAPI e base para RAG/Multi-Agent
- `docker/` stack local com PostgreSQL 16 + pgvector
- `docs/` documentação técnica
- `tests/` testes automatizados
- `img/` assets visuais (`logo.png`, `fiveicon.ico`)

## Pré-requisitos

- Docker + Docker Compose

## Subir ambiente local

1. Revise as variáveis em `.env.example`.
2. No diretório `docker/`, execute:

```bash
docker compose --project-name veredicta-ai up --build -d
```

3. Acesse a API em `http://127.0.0.1:8011`.

## Coexistência com outros containers (CRM)

- Este projeto usa `--project-name veredicta-ai` para isolar nomes e rede.
- A API foi configurada para `127.0.0.1:8011` por padrão.
- A porta `8001` já está ocupada por `wk_ai_service` no host atual.
- O PostgreSQL do Veredicta não expõe porta no host (somente rede interna do compose), evitando conflito com bancos já em execução.
- Para parar somente o Veredicta:

```bash
docker compose --project-name veredicta-ai down
```

## Endpoints base

- `GET /health`
- `GET /metrics`
- `POST /upload`
- `POST /query`
- `POST /run-autonomous-review`

Os endpoints `query` e `run-autonomous-review` estão ativos como placeholders para as próximas fases do roadmap.

## Próximos passos imediatos

- Implementar pipeline de ingestão PDF
- Adicionar chunking token-aware
- Integrar embeddings e persistência vetorial
