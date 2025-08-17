# 1. Imagem Base: Utiliza a mesma imagem Python leve para consistência.
FROM python:3.10-slim

# 2. Diretório de Trabalho: Define o diretório padrão.
WORKDIR /app

# 3. Copiar e Instalar Dependências Python:
#    Instala as poucas bibliotecas necessárias para o frontend.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar Código da Aplicação: Copia o código da interface do usuário.
COPY . .

# 5. Expor a Porta: Expõe a porta padrão do Streamlit, 8501.
EXPOSE 8501

# 6. Comando de Execução: Inicia o servidor do Streamlit.
#    --server.address 0.0.0.0 é essencial para tornar a interface
#    acessível a partir do seu navegador.
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]