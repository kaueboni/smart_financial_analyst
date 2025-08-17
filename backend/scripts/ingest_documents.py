import os
import shutil
import base64
from io import BytesIO
from dotenv import load_dotenv
from typing import List

# Importadores e Ferramentas de LangChain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage

# Bibliotecas para manipulação de PDF e Imagens
from pdf2image import convert_from_path
from PIL import Image

# --- CONFIGURAÇÃO ---
# Carrega as variáveis de ambiente (necessário para a API Key da OpenAI)
load_dotenv()

# Define os caminhos para a base de conhecimento e para o vector store
KNOWLEDGE_BASE_DIR = "core/knowledge_base"
VECTOR_STORE_DIR = "core/vector_store"

# Inicializa o LLM Multimodal (GPT-4o é uma excelente escolha)
llm_vision = ChatOpenAI(model="gpt-4o", max_tokens=2048, api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image: Image.Image) -> str:
    """Converte uma imagem PIL para uma string base64."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def summarize_page_multimodal(file_path: str, page_number: int) -> Document:
    """
    Converte uma página de PDF em imagem, extrai o texto e usa um LLM multimodal
    para gerar um resumo detalhado da página.
    """
    print(f"  -> Processando multimodalmente a página {page_number + 1}...")
    
    # 1. Converte a página específica em uma imagem
    try:
        image = convert_from_path(file_path, first_page=page_number + 1, last_page=page_number + 1)[0]
        image_base64 = encode_image(image)
    except Exception as e:
        print(f"    -> Erro ao converter página em imagem: {e}")
        return None

    # 2. Extrai o texto da página específica
    try:
        loader = PyPDFLoader(file_path)
        text_content = loader.load()[page_number].page_content
    except Exception as e:
        print(f"    -> Erro ao extrair texto da página: {e}")
        text_content = "" # Continua mesmo se não houver texto

    # 3. Cria a mensagem para o LLM multimodal
    try:
        msg = llm_vision.invoke(
            [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": """
                            Você é um analista financeiro especialista. Sua tarefa é analisar o conteúdo de uma página de um relatório financeiro.
                            A página contém tanto texto quanto elementos visuais (gráficos, tabelas).
                            
                            Analise a imagem e o texto fornecidos e crie um resumo detalhado em markdown.
                            Descreva os principais insights, números e tendências apresentados. Se houver um gráfico, explique o que ele representa, seus eixos, dados e a conclusão que pode ser tirada dele.
                            Seu resumo deve ser completo e preciso, integrando as informações de ambas as fontes (texto e imagem).
                            """
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_base64}"}
                        },
                        {
                            "type": "text",
                            "text": f"--- TEXTO EXTRAÍDO DA PÁGINA ---\n\n{text_content}"
                        }
                    ]
                )
            ]
        )
        summary = msg.content
    except Exception as e:
        print(f"    -> Erro na chamada ao LLM multimodal: {e}")
        return None

    # 4. Retorna o resumo como um objeto Document
    source_info = f"{os.path.basename(file_path)} - Página {page_number + 1}"
    return Document(page_content=summary, metadata={"source": source_info})


def ingest_documents():
    """
    Função principal que processa os documentos usando uma abordagem multimodal.
    """
    print("--- Iniciando o processo de ingestão MULTIMODAL ---")

    if os.path.exists(VECTOR_STORE_DIR):
        print(f"Removendo o Vector Store antigo em: {VECTOR_STORE_DIR}")
        shutil.rmtree(VECTOR_STORE_DIR)
    
    all_summaries: List[Document] = []
    pdf_files = [f for f in os.listdir(KNOWLEDGE_BASE_DIR) if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, pdf_file)
        print(f"\nProcessando arquivo: {pdf_file}")
        
        try:
            # Descobre o número de páginas para iterar
            num_pages = len(PyPDFLoader(file_path).load())
            
            for i in range(num_pages):
                summary_doc = summarize_page_multimodal(file_path, i)
                if summary_doc:
                    all_summaries.append(summary_doc)
        except Exception as e:
            print(f"  -> ERRO GRAVE ao processar o arquivo {pdf_file}: {e}")
            continue # Pula para o próximo arquivo

    if not all_summaries:
        print("Nenhum resumo foi gerado. Encerrando.")
        return

    print(f"\nTotal de {len(all_summaries)} resumos de página gerados com sucesso.")
    
    # O resto do processo é o mesmo: dividir os RESUMOS (não o texto original) e criar embeddings
    print("Dividindo os resumos em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(all_summaries)
    print(f"Resumos divididos em {len(chunks)} chunks.")

    print("Criando embeddings e armazenando no Vector Store...")
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings,
        persist_directory=VECTOR_STORE_DIR
    )

    print("\n--- Processo de ingestão MULTIMODAL concluído com sucesso! ---")


if __name__ == "__main__":
    ingest_documents()
