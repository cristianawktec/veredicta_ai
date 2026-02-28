# Veredicta AI - Test Suite

## 🧪 Suite de Testes com pytest

### Testes Críticos Implementados

#### ✅ **TESTE 1: Upload de PDF** (`test_upload.py`)
- Validar upload bem-sucedido
- Procesamento de PDF
- Criação de chunks
- Rejeição de não-PDFs
- Validação de PDFs vazios

#### ✅ **TESTE 2: Embeddings Gemini** (`test_embeddings.py`)
- Geração de embeddings com Google Gemini
- Validação de dimensão (768)
- Funcionamento da API key
- Configuração correta

#### ✅ **TESTE 3: Database & Vector Storage** (`test_database.py`)
- Conexão com PostgreSQL
- Extensão pgvector instalada
- Tabelas existem
- Coluna embedding configurada (vector 768)
- Roundtrip de vetores (salvar/recuperar)

#### ✅ **TESTE BÁSICO: Health Check** (`test_health.py`)
- API respondendo
- Endpoints básicos

---

## 🚀 Como Executar

### Pré-requisitos
```bash
# Instalar dependências
pip install -r backend/requirements.txt

# Ter PostgreSQL rodando (via Docker)
cd docker
docker compose --project-name veredicta-ai up -d
```

### Executar Todos os Testes
```bash
pytest
```

### Executar Teste Específico
```bash
pytest tests/test_upload.py
pytest tests/test_embeddings.py
pytest tests/test_database.py
```

### Executar com Coverage
```bash
pytest --cov=backend/app --cov-report=html
```

### Executar Apenas Testes Rápidos (sem integração)
```bash
pytest -m "not integration"
```

---

## 📋 Environment Variables Necessárias

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_EMBED_MODEL=models/text-embedding-004
DATABASE_URL=postgresql+psycopg2://veredicta_user:veredicta_pass@localhost:5432/veredicta
```

---

## 🎯 Objetivos dos Testes

1. **Garantir backend sólido** antes de criar Dashboard
2. **Validar integração Gemini** funcionando 100%
3. **Confirmar persistência** de vetores no PostgreSQL
4. **Prevenir regressões** em futuras mudanças

---

## 📊 Próximos Passos

Após testes passarem:
- ✅ Merge feature/pytest-suite → main
- 🚀 Iniciar feature/dashboard-mvp
- 🎨 Implementar 4 módulos do Dashboard
