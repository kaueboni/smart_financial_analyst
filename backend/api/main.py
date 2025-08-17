from fastapi import FastAPI
from .schemas import AgentRequest, AgentResponse  # Importa os schemas da API
from core.graph import app_langgraph             # Importa o agente compilado do core

# Inicializa a aplicação FastAPI
app_fastapi = FastAPI(
    title="API do Agente Financeiro",
    description="Camada de API que serve a lógica do agente financeiro do módulo core."
)

@app_fastapi.post("/invoke_agent", response_model=AgentResponse)
async def invoke_agent_endpoint(request: AgentRequest):
    """
    Recebe uma pergunta, passa para o core do agente e retorna a resposta.
    Este endpoint é o ponto de entrada principal para o frontend.
    """
    print(f"--- A receber requisição para a conversa ID: {request.conversation_id} ---")
    
    # A entrada para o grafo deve corresponder à estrutura do AgentState
    inputs = {
        "question": request.question,
        # O histórico de mensagens é gerido e carregado automaticamente
        # pelo checkpointer do Redis, por isso não precisamos de o passar aqui.
    }
    
    # Configuração para identificar a thread da conversa para o checkpointer
    # config = {"configurable": {"thread_id": request.conversation_id}}


    
    # Invoca o agente de forma assíncrona, passando a entrada e a configuração da thread
    final_state = await app_langgraph.ainvoke(inputs)
    # final_state = await app_langgraph.ainvoke(inputs, config=config)

    # Retorna a resposta no formato definido pelo AgentResponse
    return AgentResponse(
        final_answer=final_state.get("final_answer", "Ocorreu um erro ao gerar a resposta."),
        intermediate_steps=final_state.get("intermediate_steps", [])
    )
