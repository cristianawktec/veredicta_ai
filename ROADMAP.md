# 🚀 Veredicta  AI
## Enterprise Generative AI Platform for Legal Document Intelligence

---

## 📌 Visão Geral

Veredicta  AI é uma plataforma modular de Inteligência Artificial Generativa
voltada para análise documental jurídica utilizando:

- RAG (Retrieval-Augmented Generation)
- Arquitetura Multi-Agent
- Banco Vetorial com PostgreSQL + pgvector
- Python como linguagem principal
- Deploy cloud-ready (AWS)

O objetivo é demonstrar arquitetura enterprise para aplicações GenAI
em ambientes corporativos e jurídicos.

---

# 🏗 Arquitetura Macro

## Camadas do Sistema

1. Ingestion Layer
2. Embedding & Vector Storage
3. RAG Engine
4. Multi-Agent Orchestration
5. Guardrails & Evaluation
6. API Layer
7. Deployment Layer

---

# 🛠 Stack Tecnológica

## Linguagem Principal
- Python 3.11+

## Backend
- FastAPI
- Pydantic
- Uvicorn

## IA / GenAI
- LangChain
- LangGraph (Multi-Agent)
- OpenAI API (ou modelo open-source)
- RAGAS (avaliação)

## Banco de Dados
- PostgreSQL 16
- pgvector (vector storage)

## Infraestrutura
- Docker
- Docker Compose
- AWS EC2 (ou ECS)
- Nginx

## Observabilidade
- Logging estruturado (Python logging)
- Métricas de latência
- Score de confiança de resposta

---

# 📈 Roadmap de Implementação

---

# � Status de Implementação Atual

## ✅ Concluído

### Fase 1 - Estrutura Base (100%)
- ✅ Repositório Git + GitHub
- ✅ Estrutura de pastas organizada
- ✅ Ambiente Python 3.11 configurado
- ✅ PostgreSQL 16 + pgvector via Docker
- ✅ FastAPI backend operacional
- ✅ Deploy VPS (veredictaia.consultoriawk.com)
- ✅ Nginx reverse proxy + SSL/HTTPS

### Fase 2 - Ingestion & Embeddings (90%)
- ✅ Upload de PDFs (POST /upload)
- ✅ Extração de texto com PyPDF
- ✅ Chunking com RecursiveCharacterTextSplitter
- ✅ **Google Gemini AI integrado** (text-embedding-004, 768 dims)
- ✅ Modelagem completa do banco de dados
- ✅ Vector storage (pgvector) operacional
- ✅ Testes automatizados (pytest) - **CONCLUÍDO (10 passed, 2 skipped)**

## 🔄 Em Desenvolvimento

### Fase 8 - Dashboard & Frontend (MVP)
- ✅ Scaffold inicial React + TypeScript + Vite criado em `frontend/`
- ✅ Módulo 1 (Overview) concluído
- ✅ Módulo 2 (Upload & Analysis) concluído
- ✅ UI base com Tailwind + componentes estilo shadcn concluída

### Fase 3 - RAG Engine (Iniciado)
- 📍 **ATUAL:** Query Pipeline MVP em desenvolvimento na branch `feature/rag-query-pipeline-mvp`

## ⏳ Pendente

- ❌ Fase 3 - RAG Engine (Query Pipeline)
- ❌ Fase 4 - Multi-Agent (LangGraph)
- ❌ Fase 5 - Guardrails & Avaliação
- ❌ Fase 6 - API Layer completa
- ❌ Fase 7 - Deploy avançado
- ❌ **Fase 8 - Dashboard & Frontend** (NOVA)

---

# �🔵 Fase 1 — Estrutura Base do Projeto

## 1. Inicialização do Repositório

- Criar repositório Git
- Definir estrutura de pastas
Veredicta -ai/
backend/
docs/
docker/
tests/


## 2. Setup Ambiente Python

- Criar ambiente virtual
- Instalar dependências:
  - fastapi
  - langchain
  - langgraph
  - psycopg2
  - sqlalchemy
  - pgvector
  - openai
  - ragas

## 3. Configurar PostgreSQL + pgvector via Docker

- Criar docker-compose com:
  - PostgreSQL
  - pgvector habilitado
  - Backend FastAPI

---

# 🔵 Fase 2 — Ingestion & Embeddings Pipeline

## 4. Document Loader

- Upload de PDFs
- Extração de texto (PyPDF)

## 5. Chunking Inteligente

- Token-aware chunking
- Overlap estratégico

## 6. Geração de Embeddings

- Utilizar OpenAI embeddings
- Armazenar vetores no PostgreSQL (pgvector)

## 7. Modelagem do Banco

Tabela documents
Tabela chunks
Campo embedding (vector)

---

# 🔵 Fase 3 — Implementação do RAG Engine

## 8. Query Pipeline

- Receber pergunta
- Gerar embedding da query
- Executar busca vetorial (k-NN)
- Recuperar top-k chunks

## 9. Context Assembly

- Montar prompt com fontes
- Incluir citações obrigatórias

## 10. Geração de Resposta

- Chamada LLM
- Retorno estruturado:
  - Resposta
  - Fontes utilizadas
  - Score de confiança

---

# 🔵 Fase 4 — Arquitetura Multi-Agent (LangGraph)

## 11. Definir Agentes

- Planner Agent
- Retriever Agent
- Analyzer Agent
- Validator Agent
- Report Generator Agent

## 12. Orquestração com LangGraph

- Definir estado global
- Fluxo condicional
- Comunicação A2A

## 13. Execução Autônoma

Endpoint:

POST /run-autonomous-review

Entrada:
- Caso jurídico
- Documentos associados

Saída:
- Relatório técnico estruturado

---

# 🔵 Fase 5 — Guardrails & Avaliação

## 14. Implementar Guardrails

- Limite de escopo
- Verificação de fontes
- Filtro de alucinação

## 15. Avaliação com RAGAS

- Precisão contextual
- Faithfulness
- Relevância

---

# 🔵 Fase 6 — API Layer

Endpoints:

POST /upload
POST /query
POST /run-autonomous-review
GET /metrics
GET /health

---

# 🔵 Fase 7 — Dashboard & Interface Visual

## 18. Frontend Web Application

### Tecnologias Sugeridas:
- **React.js** ou **Next.js** (framework moderno)
- **TypeScript** (type safety)
- **TailwindCSS** ou **Material-UI** (design system)
- **React Query** (gerenciamento de estado/API)
- **Chart.js** ou **Recharts** (gráficos)

### Funcionalidades Core:

#### 📄 Gestão de Documentos
- Upload de PDFs (drag & drop)
- Visualização de documentos processados
- Status de processamento
- Preview de PDFs
- Download de documentos

#### 🔍 Interface de Consulta RAG
- Campo de busca semântica
- Exibição de respostas com citações
- Destaque de trechos relevantes
- Score de confiança visual
- Histórico de consultas

#### 📊 Dashboard Analítico
- Total de documentos processados
- Total de consultas realizadas
- Gráficos de uso por período
- Métricas de performance (latência)
- Score médio de confiança

#### ⚖️ Gestão de Casos Jurídicos
- Lista de casos/processos
- Criação de novos casos
- Associação de documentos a casos
- Timeline de atividades
- Filtros e busca

#### 👥 Gestão de Usuários/Profissionais
- Cadastro de profissionais (Advogados, Juízes, Peritos)
- Controle de acesso por caso
- Roles e permissões
- Histórico de ações

#### 🤖 Interface Multi-Agent
- Iniciar análise autônoma
- Visualização do fluxo de agentes
- Progresso em tempo real
- Relatório técnico formatado
- Export PDF/DOCX

#### ⚙️ Configurações
- Gerenciamento de API keys
- Configuração de modelos de IA
- Parâmetros de chunking
- Limites e quotas

### Arquitetura Frontend:
```
frontend/
├── src/
│   ├── components/
│   │   ├── DocumentUpload/
│   │   ├── QueryInterface/
│   │   ├── Dashboard/
│   │   ├── CaseManagement/
│   │   └── UserManagement/
│   ├── pages/
│   ├── services/
│   │   └── api.ts (integração com backend)
│   ├── hooks/
│   ├── utils/
│   └── App.tsx
├── public/
├── package.json
└── tsconfig.json
```

---

# 🔵 Fase 8 — Deploy & Infraestrutura

## 19. Containerização Completa

- Dockerfile backend
- Dockerfile frontend
- Docker Compose produção (multi-container)

## 20. Deploy Cloud

- EC2 configurado
- Nginx reverse proxy (backend + frontend)
- SSL
- CI/CD pipeline
- Monitoramento e logs

---

# 📊 Roadmap Temporal (8 Semanas)

Semana 1-2:
- ✅ Setup infra + pgvector
- ✅ Pipeline embeddings com Gemini
- 🔄 Suite de testes (pytest)

Semana 3:
- RAG funcional com citações
- Busca vetorial otimizada

Semana 4-5:
- Multi-agent com LangGraph
- Avaliação + Guardrails

Semana 6-7:
- **Dashboard & Frontend completo**
- Gestão de casos e usuários
- Interface RAG intuitiva

Semana 8:
- Deploy final
- Documentação técnica
- Testes end-to-end

---

# 🎯 Diferenciais Técnicos

- Arquitetura modular enterprise
- RAG com citação obrigatória
- Multi-agent com estado explícito
- Avaliação automatizada (RAGAS)
- **Dashboard profissional para gestão jurídica**
- **Interface intuitiva para análise de documentos**
- **Gestão completa de casos e profissionais**
- Pronto para expansão SaaS

---

# 📌 Objetivo Estratégico

Demonstrar capacidade de:

- Projetar arquiteturas GenAI
- Implementar RAG avançado
- Construir sistemas multi-agente
- Aplicar boas práticas de governança de IA
- Deploy em ambiente cloud-ready

---

# 🧠 Autor

Cristian MS  
Software Architect & Judicial IT Expert  