# 1. Imagem Base: Começa com uma imagem Python oficial e leve.
FROM python:3.10-slim

# 2. Instalação de Dependências do Sistema:
#    Instala o poppler-utils, que é necessário para a biblioteca pdf2image
#    conseguir converter as páginas do PDF em imagens.
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 3. Diretório de Trabalho: Define o diretório padrão dentro do contêiner.
WORKDIR /app

# 4. Copiar e Instalar Dependências Python:
#    Copia o arquivo de requisitos primeiro para aproveitar o cache do Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar Código da Aplicação: Copia todo o resto do código do backend.
COPY . .

# 6. Expor a Porta: Informa ao Docker que o contêiner ouvirá na porta 8000.
EXPOSE 8000

# 7. Comando de Execução: Inicia o servidor Uvicorn para rodar a aplicação FastAPI.
#    O caminho 'api.main:app_fastapi' reflete a nossa estrutura de pastas modular.
CMD ["uvicorn", "api.main:app_fastapi", "--host", "0.0.0.0", "--port", "8000"]