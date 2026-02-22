# 🗄 Veredicta AI – Database Architecture (PostgreSQL + pgvector)

---

## 📌 Visão Geral

Este documento descreve a modelagem do banco de dados do projeto **Veredicta AI**,
uma plataforma enterprise de IA Generativa com arquitetura RAG e Multi-Agent.

Banco de dados escolhido:

- PostgreSQL 16
- Extensão pgvector para armazenamento de embeddings
- Estrutura preparada para auditoria, rastreabilidade e futura evolução para SaaS

---

# 🔧 Inicialização do PostgreSQL com pgvector

## Docker Compose Base

```yaml
version: '3.9'

services:
  postgres:
    image: ankane/pgvector:latest
    container_name: veredicta-postgres
    environment:
      POSTGRES_DB: veredicta
      POSTGRES_USER: veredicta_user
      POSTGRES_PASSWORD: veredicta_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Subir container:

```bash
docker-compose up -d
```

Acessar banco:

```bash
docker exec -it veredicta-postgres psql -U veredicta_user -d veredicta
```

Habilitar extensão:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

# 🧠 Modelo Entidade-Relacionamento (MER)

## 🔹 1. users

Tabela preparada para futura evolução SaaS.

| Campo | Tipo |
|-------|------|
| id | UUID (PK) |
| name | VARCHAR |
| email | VARCHAR UNIQUE |
| password_hash | TEXT |
| role | VARCHAR |
| created_at | TIMESTAMP |

Relacionamento:
- 1 user → N cases

---

## 🔹 2. cases

Representa um processo ou contexto documental.

| Campo | Tipo |
|-------|------|
| id | UUID (PK) |
| user_id | UUID (FK → users) |
| title | VARCHAR |
| description | TEXT |
| status | VARCHAR |
| created_at | TIMESTAMP |

Relacionamento:
- 1 case → N documents
- 1 case → N queries

---

## 🔹 3. documents

Armazena metadados dos documentos.

| Campo | Tipo |
|-------|------|
| id | UUID (PK) |
| case_id | UUID (FK → cases) |
| filename | VARCHAR |
| file_path | TEXT |
| document_type | VARCHAR |
| created_at | TIMESTAMP |

Relacionamento:
- 1 document → N document_chunks

---

## 🔹 4. document_chunks

Base do RAG.

| Campo | Tipo |
|-------|------|
| id | UUID (PK) |
| document_id | UUID (FK → documents) |
| chunk_index | INTEGER |
| content | TEXT |
| token_count | INTEGER |
| embedding | VECTOR(1536) |
| created_at | TIMESTAMP |

Observações:
- Embedding armazenado usando pgvector
- Indexação vetorial via ivfflat recomendada

Exemplo de índice:

```sql
CREATE INDEX idx_chunks_embedding
ON document_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

---

## 🔹 5. queries

Registro de perguntas realizadas.

| Campo | Tipo |
|-------|------|
| id | UUID (PK) |
| case_id | UUID (FK → cases) |
| user_id | UUID (FK → users) |
| query_text | TEXT |
| mode | VARCHAR (rag | multi_agent) |
| created_at | TIMESTAMP |

Relacionamento:
- 1 query → 1 response
- 1 query → N retrieved_chunks
- 1 query → N agent_executions

---

## 🔹 6. responses

Armazena a resposta gerada pelo modelo.

| Campo | Tipo |
|-------|------|
| id | UUID (PK) |
| query_id | UUID (FK → queries) |
| response_text | TEXT |
| confidence_score | FLOAT |
| latency_ms | INTEGER |
| created_at | TIMESTAMP |

---

## 🔹 7. retrieved_chunks

Tabela de auditoria do contexto usado na resposta.

| Campo | Tipo |
|-------|------|
| id | UUID (PK) |
| query_id | UUID (FK → queries) |
| chunk_id | UUID (FK → document_chunks) |
| similarity_score | FLOAT |

Permite:
- Rastreabilidade total
- Debug de contexto
- Auditoria jurídica

---

## 🔹 8. agent_executions

Log detalhado da execução de cada agente.

| Campo | Tipo |
|-------|------|
| id | UUID (PK) |
| query_id | UUID (FK → queries) |
| agent_name | VARCHAR |
| input_payload | JSONB |
| output_payload | JSONB |
| execution_order | INTEGER |
| created_at | TIMESTAMP |

Permite:
- Observabilidade
- Debug multi-agent
- Replay de execução

---

## 🔹 9. evaluations

Tabela para avaliação automática (RAGAS) ou humana.

| Campo | Tipo |
|-------|------|
| id | UUID (PK) |
| response_id | UUID (FK → responses) |
| faithfulness_score | FLOAT |
| relevance_score | FLOAT |
| contextual_precision | FLOAT |
| evaluated_at | TIMESTAMP |

---

# 📐 Relacionamentos Resumidos

users
 └── cases
      └── documents
           └── document_chunks

cases
 └── queries
      ├── responses
      ├── retrieved_chunks
      └── agent_executions
             └── evaluations (via responses)

---

# 🎯 Decisões Arquiteturais

- PostgreSQL escolhido por robustez e maturidade enterprise
- pgvector permite busca vetorial nativa
- JSONB usado para flexibilidade em agentes
- UUID utilizado para melhor escalabilidade distribuída
- Separação clara entre:
  - Dados brutos (documents)
  - Representação vetorial (document_chunks)
  - Interações do usuário (queries/responses)
  - Governança (retrieved_chunks, evaluations)

---

# 🚀 Próximos Passos

1. Criar migrations SQL iniciais
2. Configurar índices vetoriais
3. Implementar camada ORM (SQLAlchemy)
4. Conectar pipeline de embeddings
5. Validar performance de busca k-NN

---

# 📌 Objetivo Estratégico

Este modelo foi projetado para:

- Sustentar arquitetura RAG enterprise
- Permitir execução multi-agent auditável
- Suportar governança e métricas
- Evoluir para SaaS multi-tenant no futuro

