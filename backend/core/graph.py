from langgraph.graph import StateGraph, END

# Importa as estruturas de dados e a memória que definimos
from core.schemas import AgentState
# from core.config import memory

# Importa as funções que representam cada nó do nosso fluxo
from core.nodes.data_collection import coletar_informacoes
from core.nodes.generation import gerar_resposta_com_llm, plano_b

def deve_gerar_resposta(state: AgentState) -> str:
    """
    Esta é a nossa Aresta Condicional (Conditional Edge).
    É a função de tomada de decisão do agente. Com base no estado,
    ela decide qual nó será executado a seguir.
    """
    print("--- A avaliar a condição: Informação encontrada? ---")
    if state["informacao_encontrada"]:
        print("-> Decisão: Sim, informação encontrada. A encaminhar para a geração da resposta.")
        print(f"Informação encontrada: {state['informacao_encontrada']}")
        return "gerar_resposta_llm"
    else:
        print("-> Decisão: Não, informação insuficiente. A acionar o Plano B.")
        return "plano_b"

# --- Construção do Grafo ---

# 1. Inicializa o grafo, associando-o à nossa estrutura de estado
workflow = StateGraph(AgentState)

# 2. Adiciona os nós ao grafo
# Cada nó é associado a uma função que ele irá executar
workflow.add_node("coletar_informacoes", coletar_informacoes)
workflow.add_node("gerar_resposta_llm", gerar_resposta_com_llm)
workflow.add_node("plano_b", plano_b)

# 3. Define as arestas (as conexões entre os nós)

# Define o ponto de entrada do grafo
workflow.set_entry_point("coletar_informacoes")

# Adiciona a aresta de decisão
workflow.add_conditional_edges(
    "coletar_informacoes", # Nó de origem
    deve_gerar_resposta,   # Função de decisão
    {
        # Mapeia o resultado da decisão para o próximo nó
        "gerar_resposta_llm": "gerar_resposta_llm",
        "plano_b": "plano_b",
    }
)

# Define os pontos de saída do grafo
# Após executar 'gerar_resposta' ou 'plano_b', o fluxo termina.
workflow.add_edge("gerar_resposta_llm", END)
workflow.add_edge("plano_b", END)

# 4. Compila o grafo num objeto executável, incluindo a memória
# A partir deste ponto, o nosso agente está "vivo" e pronto para ser usado.
app_langgraph = workflow.compile()
