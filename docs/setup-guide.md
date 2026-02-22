# Setup Guide — Veredicta AI (Local)

## Pré-requisitos

- Docker Desktop 29.2.0+
- Docker Compose v5.0.2+
- Python 3.14.2 (local, para desenvolvimento)

## Startup local

### 1. Navegar para o diretório docker

```powershell
cd C:\xampp\htdocs\Veredicta\docker
```

### 2. Trazer serviços

```powershell
docker compose --project-name veredicta-ai up -d --build
```

**Nota**: A primeira execução leva 2-3 minutos para baixar imagens e instalar dependências Python.

### 3. Verificar status dos serviços

```powershell
docker compose --project-name veredicta-ai ps
```

Esperado:
```
NAME                         IMAGE                                 STATUS
veredicta-ai-postgres-1      pgvector/pgvector:pg16               healthy
veredicta-ai-backend-1       veredicta-ai-backend:latest          running
```

### 4. Testar health check da API

```powershell
curl http://127.0.0.1:8011/health
```

Resposta esperada:
```json
{
  "status": "ok",
  "service": "veredicta-ai"
}
```

## Troubleshooting

### API não responde em 127.0.0.1:8011

1. **Check logs do backend**:
```powershell
docker compose --project-name veredicta-ai logs backend --tail 50
```

2. **Check se há conflito de porta**:
```powershell
netstat -an | findstr :8011
```

3. **Derrubar e reconstruir do zero**:
```powershell
docker compose --project-name veredicta-ai down
docker system prune -f
docker compose --project-name veredicta-ai up -d --build
```

### Banco de dados sem conectar

1. **Check status do PostgreSQL**:
```powershell
docker compose --project-name veredicta-ai logs postgres --tail 30
```

2. **Verificar variáveis de ambiente** em `.env` ou reiniciar sem sobrescrita:
```powershell
docker compose --project-name veredicta-ai down
docker volume rm veredicta-ai_postgres_data
docker compose --project-name veredicta-ai up -d
```

## Endpoints disponíveis

- `GET /health` → Health check
- `GET /metrics` → Métricas brútas
- `POST /upload` → Upload de PDF e ingestão
- `POST /query` → Query RAG (placeholder)
- `POST /run-autonomous-review` → Multi-agent (placeholder)

## Documentação completa

Veja [README.md](../README.md) e [db_postgress.md](../db_postgress.md) para detalhes de uso e arquitetura.
