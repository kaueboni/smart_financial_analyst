# frontend/app.py
import streamlit as st
import requests
import uuid
import time

# --- CONFIGURAÇÕES DA APLICAÇÃO ---

# URL da nossa API FastAPI. O nome 'backend' é resolvido pela rede interna do Docker.
API_URL = "http://backend:8000/invoke_agent"

# Configuração da página do Streamlit
st.set_page_config(page_title="Smart Financial Analyst", layout="wide")

st.title("🤖 Smart Financial Analyst ")
st.markdown("""
Bem-vindo! Sou um agente de IA projetado para o ajudar a analisar dados financeiros.
Posso consultar dados de dividendos, buscar notícias recentes na web e analisar relatórios financeiros (PDFs) que foram carregados na minha base de conhecimento.
""")

# --- GESTÃO DA SESSÃO DE CONVERSA ---

# Inicializa o histórico de mensagens da UI se ainda não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Gera um ID de conversa único para esta sessão de navegador se ainda não existir
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

# --- FUNÇÃO DE COMUNICAÇÃO COM O BACKEND ---

def call_agent_api(question: str, conv_id: str):
    """
    Envia a pergunta e o ID da conversa para a API do backend e retorna a resposta.
    """
    try:
        # Faz a requisição POST para o endpoint do nosso agente
        response = requests.post(
            API_URL, 
            json={"question": question, "conversation_id": conv_id},
            timeout=120 # Timeout de 2 minutos para permitir o processamento do LLM
        )
        # Levanta um erro para respostas com status de erro (4xx ou 5xx)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Retorna uma mensagem de erro se a comunicação com o backend falhar
        return {"error": f"Erro de comunicação com o backend: {e}"}

# --- CONSTRUÇÃO DA INTERFACE DE CHAT ---

# Exibe as mensagens do histórico na UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"],unsafe_allow_html=True)

# Aguarda por uma nova entrada do utilizador
if prompt := st.chat_input("Faça a sua pergunta..."):
    # Adiciona a mensagem do utilizador ao histórico da UI e exibe-a
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt,unsafe_allow_html=True)

    # Exibe a resposta do agente
    with st.chat_message("assistant"):
        # Mostra um spinner enquanto o agente está a "pensar"
        with st.spinner("O Smart Financial Analyst está a analisar... Por favor, aguarde."):
            # Chama a API do backend com a pergunta e o ID da sessão
            api_response = call_agent_api(prompt, st.session_state.conversation_id)

        # Verifica se a API retornou um erro
        if "error" in api_response:
            st.error(api_response["error"])
        else:
            # Exibe a resposta final do agente
            final_answer = api_response.get("final_answer", "Não foi possível obter uma resposta.")
            st.markdown(final_answer,unsafe_allow_html=True)
            
            # Adiciona a resposta do agente ao histórico da UI
            st.session_state.messages.append({"role": "assistant", "content": final_answer})

            # (Opcional) Exibe os passos intermédios num expander para depuração
            with st.expander("Ver o Raciocínio do Agente"):
                steps = api_response.get("intermediate_steps", [])
                for step in steps:
                    st.write(f"**Nó/Ferramenta:** `{step.get('node')}`")
                    st.write(f"**Detalhes:** {step.get('details') or step.get('status')}")
                    st.divider()
