import asyncio
import uuid

# Importa o nosso agente LangGraph já compilado
from graph import app_langgraph

async def run_test(question: str, thread_id: str):
    """Função auxiliar para invocar o agente e imprimir os resultados."""
    inputs = {
        "question": question,
        # O histórico de mensagens é gerido pelo checkpointer,
        # por isso começamos com uma lista vazia ou não o passamos.
    }
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"\n>>> A testar pergunta: '{question}' (Conversa ID: {thread_id})")
    
    final_state = None
    async for event in app_langgraph.astream(inputs, config=config):
        print("[PASSO INTERMEDIÁRIO]", event)
        # Procura a resposta final dentro do dicionário do nó
        for value in event.values():
            if isinstance(value, dict) and "final_answer" in value:
                final_state = value
                break

    if final_state:
        print("\n[RESPOSTA FINAL GERADA]")
        print(final_state.get("final_answer"))
    else:
        print("\n[ERRO] Nenhuma resposta final foi gerada.")

async def main():
    """
    Função principal que executa os três cenários de teste.
    """
    print("--- A INICIAR O TESTE FINAL DO CORE DO AGENTE ---")

    # --- TESTE 1: Caminho com Sucesso (Petrobras) ---
    # Este teste deve acionar todas as ferramentas e gerar uma resposta completa.
    # print("\n--- CENÁRIO 1: TESTE DO CAMINHO COM SUCESSO ---")
    # await run_test(
    #     question="Faça uma análise completa da Vale, considerando dividendos e notícias.",
    #     thread_id=f"test-thread-{uuid.uuid4()}"
    # )

    #--- TESTE 2: Caminho "Plano B" (Empresa sem dados) ---
    # Este teste deve acionar a aresta condicional para o nó 'plano_b'.
    print("\n\n--- CENÁRIO 2: TESTE DO 'PLANO B' ---")
    await run_test(
        question="O que me pode dizer sobre uma empresa fictícia chamada XYZ Corp?",
        thread_id=f"test-thread-{uuid.uuid4()}"
    )

    # # --- TESTE 3: Memória Conversacional (Vale) ---
    # # Este teste verifica se o agente se lembra do contexto entre perguntas.
    # print("\n\n--- CENÁRIO 3: TESTE DA MEMÓRIA CONVERSACIONAL ---")
    # conversa_vale_id = f"test-thread-{uuid.uuid4()}"
    
    # # Pergunta 1
    # await run_test(
    #     question="Quais são os dados de dividendos mais recentes da Vale?",
    #     thread_id=conversa_vale_id
    # )
    
    # # Pergunta 2 (na mesma conversa)
    # # O agente deve saber que "ela" se refere à Vale.
    # await run_test(
    #     question="E qual a análise de sentimento das notícias sobre ela?",
    #     thread_id=conversa_vale_id
    # )

    print("\n\n--- TESTE FINAL CONCLUÍDO ---")

if __name__ == "__main__":
    asyncio.run(main())
