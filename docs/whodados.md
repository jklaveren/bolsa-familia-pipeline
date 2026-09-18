# Sistema de Inteligência Empresarial e CRM — WhoDados (Cliente B2B: NRA Advocacia)

> 📦 **Stack da Aplicação:** Next.js + FastAPI + Supabase (PostgreSQL) + Anthropic Claude AI + Python ETL.

---

## 📌 Visão Geral

O WhoDados é uma plataforma B2B multitenant (multiempresa com controle hierárquico de acessos) **em produção e utilizada ativamente pelo escritório NRA Advocacia**, integrando:
- **Inteligência Corporativa & Dados Públicos:** Análise de empresas, investigação de sócios, grupos econômicos e dívidas ativas federais.
- **Pesquisa Autônoma com IA (Anthropic Claude):** Integração com agentes de IA da Anthropic para automação de pesquisas e análises investigativas.
- **CRM & Gestão de Tarefas:** Acompanhamento de leads, pipeline comercial e administração de tarefas internas.
- **Campanhas Multicanal:** Disparo automatizado de campanhas por E-mail e WhatsApp.

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│  VERCEL (Next.js) - Frontend (`whodados/frontend/`)          │
│  ✅ Dashboard, CRM, Campanhas, Gestão de Tarefas            │
└──────────────────────┬──────────────────────────────────────┘
                       │  API REST
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  RENDER (FastAPI) - Backend (`whodados/backend/`)           │
│  ✅ JWT Auth, CRM, Campanhas WhatsApp/Email, Claude AI      │
└──────────────────────┬──────────────────────────────────────┘
                       │  SQLAlchemy
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  SUPABASE (PostgreSQL) - Banco de dados multitenant         │
│  ✅ Hierarquias, Empresas, Sócios, Dívidas, CRM, Tarefas    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Estrutura do Projeto (`whodados/`)

```
whodados/
├── backend/                      # FastAPI (deploy no Render)
│   ├── main.py                   # Entry point
│   ├── endpoints.py              # Endpoints da API (/empresas, /crm, /campaigns, etc.)
│   ├── ai_service.py             # Integração com Anthropic Claude AI
│   └── requirements.txt          # Dependências da API
├── frontend/                     # Next.js (deploy na Vercel)
│   ├── src/app/                  # Páginas (Dashboard, CRM, Tarefas, Campanhas)
│   ├── src/components/           # Componentes UI
│   └── package.json              # Dependências do frontend
├── pipeline/                     # Pipeline ETL de dados
│   ├── pipeline.py               # Script principal / subcomandos ETL
│   └── out/                      # CSVs gerados (.gitignored)
└── render.yaml                   # Configuração do Render
```
