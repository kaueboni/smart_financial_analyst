import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Define o caminho para o Vector Store que foi criado pelo script de ingestão
VECTOR_STORE_DIR = "core/vector_store"

def buscar_contexto_teorico(question: str) -> str:
    """
    Ferramenta 3 (RAG): Busca nos documentos processados (Vector Store) os trechos
    mais relevantes para responder a uma pergunta, fornecendo embasamento teórico.
    """
    print("-> A executar ferramenta de RAG para buscar contexto teórico...")
    if not os.path.exists(VECTOR_STORE_DIR):
        return "A base de conhecimento (Vector Store) não foi encontrada. Execute o script de ingestão primeiro."

    try:
        # Inicializa o modelo de embeddings (o mesmo usado na ingestão)
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Carrega o Vector Store do disco
        vector_store = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embeddings)
        
        # Realiza uma busca por similaridade para encontrar os 4 chunks mais relevantes
        results = vector_store.similarity_search(question, k=4)
        
        if not results:
            return "Nenhum contexto teórico relevante encontrado na base de conhecimento."
            
        # Formata os resultados num único bloco de texto
        context = "\n\n---\n\n".join([doc.page_content for doc in results])
        return context
    except Exception as e:
        print(f"  -> Erro na ferramenta de RAG: {e}")
        return "Ocorreu um erro ao tentar acessar à base de conhecimento."