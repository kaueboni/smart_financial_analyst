# backend/core/config.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import redis 
from langgraph.checkpoint.redis import RedisSaver

# Carrega as variáveis de ambiente (API Keys) do arquivo .env na raiz do projeto
load_dotenv()

# --- CONFIGURAÇÃO DAS API KEYS ---
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- INICIALIZAÇÃO DOS CLIENTES DE SERVIÇOS ---

# Inicializa o modelo de LLM da OpenAI uma única vez para ser reutilizado em toda a aplicação.
# Usamos o gpt-4o por suas capacidades multimodais e de raciocínio.
llm = ChatOpenAI(model="gpt-4o", temperature=0.0, api_key=OPENAI_API_KEY)

# --- CONFIGURAÇÃO DA MEMÓRIA (CHECKPOINTER) ---

# Conecta ao serviço do Redis que está a correr no outro contêiner Docker.
# O nome do host 'redis' é resolvido pela rede interna do Docker Compose.
# redis_conn = redis.Redis.from_url("redis://redis:6379/0")

# Cria o Checkpointer (a "memória" persistente do nosso agente).
# O LangGraph usará este objeto para salvar e carregar o estado de cada conversa.
# memory = RedisSaver(url="redis://localhost:6379/0")
