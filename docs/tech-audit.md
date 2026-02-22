# Inventário Técnico do Ambiente (Host Local)

Data da auditoria: 2026-02-22
Projeto: Veredicta AI

## Tecnologias requeridas no roadmap

### Runtime e Linguagem
- Python: 3.14.2 (detectado)
- Docker: 29.2.0 (detectado)
- Docker Compose: v5.0.2 (detectado)

### Banco e Infra
- PostgreSQL (cliente `psql` no host): não encontrado
- Nginx (binário no host Windows): não encontrado

Observação:
- A ausência de `psql` e `nginx` no Windows local não impede o projeto, pois o banco roda em container e o Nginx ficará na VPS.

## Estado dos containers já ativos (coexistência)

- wk_crm_laravel -> porta 8000 publicada
- wk_ai_service -> porta 8001 publicada
- wk_postgres -> porta 5432 publicada
- wk_pgadmin -> porta 5050 publicada
- wk_redis -> porta 6379 publicada

Impacto no Veredicta:
- Porta 8000 conflita com CRM
- Porta 8001 conflita com `wk_ai_service`
- Porta 5432 conflita com `wk_postgres` se publicada no host

## Padrão adotado no Veredicta

- API do Veredicta: 127.0.0.1:8011 (evita conflito)
- PostgreSQL do Veredicta: sem publicação de porta no host (somente rede interna do compose)
- Compose com `--project-name veredicta-ai` para isolamento de rede e recursos

## Banco alinhado com db_postgress.md

Arquivo base aplicado:
- docker/init.sql

Tabelas criadas no bootstrap:
- users
- cases
- documents
- document_chunks
- queries
- responses
- retrieved_chunks
- agent_executions
- evaluations

Recursos aplicados:
- `CREATE EXTENSION vector`
- `ivfflat` index em `document_chunks.embedding`
- FKs para rastreabilidade e auditoria
