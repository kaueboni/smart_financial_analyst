# ----------------------------------------------------
# Conteúdo para o ficheiro: backend/core/nodes/generation.py
# ----------------------------------------------------
from typing import Dict
from langchain_core.messages import HumanMessage, AIMessage

# Importa as estruturas de dados e o cliente LLM
from core.schemas import AgentState
from core.config import llm

def gerar_resposta_com_llm(state: AgentState) -> Dict:
    """
    Nó 2: O Redator Final.
    Usa o LLM da OpenAI para sintetizar todo o contexto recolhido numa resposta final.
    """
    print("--- A executar o nó: Gerar Resposta com LLM ---")
    question = state["question"]
    # chat_history = state.get("messages", [])
    steps = state["intermediate_steps"]
    steps.append({"node": "gerar_resposta_llm", "status": "A gerar a análise final com o LLM..."})
    
    contexto_dividendos = "Nenhum dado sobre dividendos foi encontrado."
    if not state["dados_dividendos"].empty:
        try:
            contexto_dividendos = state["dados_dividendos"].to_markdown(index=False)
        except Exception:
            contexto_dividendos = state["dados_dividendos"].to_string(index=False)
    
    contexto_noticias_e_teoria = state["analise_noticias"]
    
    system_prompt = """
    Você é um assistente financeiro, prestativo e neutro. A sua tarefa é fornecer uma análise concisa sobre uma empresa com base nos dados fornecidos e no histórico da conversa.
    Estruture a sua resposta da seguinte forma:
    1.  **Análise de Dados:** Comente sobre o histórico recente de dividendos, usando os dados tabulares fornecidos, mas NÃO utilize formatação Markdown (itálico, negrito, etc.) em valores numéricos.
    2.  **Cenário Atual:** Com base na análise de sentimento das notícias e no contexto teórico dos documentos, comente sobre o cenário atual da empresa.
    3.  **Aviso Legal:** Sempre termine com um aviso de que esta não é uma recomendação de investimento e que os dados são para fins demonstrativos.
    Seja claro, objetivo e não faça previsões. Apenas analise os dados fornecidos.
    """

    prompt_messages = [HumanMessage(content=system_prompt)]
    #prompt_messages.extend(chat_history) # Adiciona o histórico da conversa

    user_prompt = f"""
    Pergunta do Utilizador: {question}
    ---
    Dados de Dividendos:
    {contexto_dividendos}
    ---
    Análise de Notícias e Contexto Teórico:
    {contexto_noticias_e_teoria}
    """
    prompt_messages.append(HumanMessage(content=user_prompt))
    
    try:
        print("\n-> A invocar o LLM para gerar a resposta final...")
        response = llm.invoke(prompt_messages)
        resposta_final = response.content
    except Exception as e:
        print(f"Erro ao invocar o LLM: {e}")
        resposta_final = "Ocorreu um erro ao tentar gerar a resposta com o LLM. Por favor, tente novamente mais tarde."
    
    # Atualiza o histórico de mensagens para a próxima interação
    #novo_historico = chat_history + [HumanMessage(content=question), AIMessage(content=resposta_final)]
    print(resposta_final)
    #return {"final_answer": resposta_final, "messages": novo_historico, "intermediate_steps": steps}
    return {"final_answer": resposta_final, "intermediate_steps": steps}


def plano_b(state: AgentState) -> Dict:
    """
    Nó 3: A Rota de Escape.
    Fornece uma resposta padrão quando nenhuma informação útil é encontrada.
    """
    print("--- A executar o nó: Plano B ---")
    question = state["question"]
    chat_history = state.get("messages", [])
    steps = state["intermediate_steps"]
    steps.append({"node": "plano_b", "status": "A acionar a rota de escape..."})

    resposta_final = "Desculpe, não consegui encontrar informações suficientes sobre a empresa mencionada nas minhas fontes de dados. Por favor, tente perguntar sobre tickers específicos como VALE3 ou PETR4, ou verifique se a base de conhecimento RAG foi carregada."
    
    #novo_historico = chat_history + [HumanMessage(content=question), AIMessage(content=resposta_final)]
    #return {"final_answer": resposta_final, "messages": novo_historico, "intermediate_steps": steps}
    return {"final_answer": resposta_final, "intermediate_steps": steps}

