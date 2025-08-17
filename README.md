# Smart Financial Analyst

Este projeto é um agente financeiro inteligente com backend em FastAPI e frontend em Streamlit. O Docker Compose é utilizado para orquestrar os serviços da aplicação.

## Pré-requisitos
- Docker e Docker Compose instalados
- (Opcional) Python 3.10+ para desenvolvimento local

## Passos para rodar a aplicação do zero

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd smart_financial_analyst
   ```

2. **Configure o arquivo `.env`:**
   - Crie um arquivo `.env` na raiz do projeto com suas variáveis de ambiente (exemplo: `OPENAI_API_KEY=...`).

3. **Suba os containers:**
   ```bash
   docker-compose up --build
   ```

4. **Acesse a aplicação:**
   - Backend (API): http://localhost:8000/docs
   - Frontend (Streamlit): http://localhost:8501

5. **Testes rápidos:**
   - Para rodar ingestão de documentos:
     ```bash
     docker-compose exec backend python scripts/ingest_documents.py
     ```
   - Para rodar testes do grafo:
     ```bash
     docker-compose exec backend python core/graph_test.py
     ```

## Estrutura do Projeto
- `backend/` — FastAPI, lógica do agente, ingestão de dados
- `frontend/` — Streamlit, interface do usuário
- `docker-compose.yml` — Orquestração dos serviços

## Observações
- O backend e o frontend recarregam automaticamente ao salvar alterações (hot reload).
- O arquivo `.env` nunca deve ser versionado (veja `.gitignore`).
- Para customizar a base de conhecimento, adicione PDFs em `backend/core/knowledge_base/` e rode o script de ingestão.

---

Dúvidas? Consulte a documentação dos arquivos ou abra uma issue!
