# backend/core/nodes/data_collection.py
import pandas as pd
from typing import Dict

# Importa as estruturas de dados e as ferramentas que criámos
from core.schemas import AgentState
from core.tools.search import buscar_noticias_recentes
from core.tools.sentiment import analisar_sentimento_noticias
from core.tools.knowledge_retriever import buscar_contexto_teorico
from core.tools.structured_data_retriever import buscar_dados_de_dividendos 
from core.config import llm

def coletar_informacoes(state: AgentState) -> Dict:
    """
    Nó 1: O Coletor de Inteligência.
    Este nó orquestra o uso de todas as ferramentas para reunir o contexto necessário.
    """
    question = state["question"]
    steps = state.get("intermediate_steps", [])
    steps.append({"node": "coletar_informacoes", "status": "A iniciar a recolha de dados..."})
    print(f"--- A executar o nó: Coletar Informações para a pergunta: '{question}' ---")

    # Mapeamento simplificado da pergunta para ticker/empresa
    ticker, company_name = None, None
    pergunta_lower = question.lower()
    if "vale" in pergunta_lower or "vale3" in pergunta_lower:
        ticker, company_name = "VALE3", "Vale S.A."
    elif "petrobras" in pergunta_lower or "petr4" in pergunta_lower:
        ticker, company_name = "PETR4", "Petrobras"

    # --- Execução das Ferramentas ---

    # Ferramenta 1: RAG para buscar embasamento teórico
    contexto_teorico = buscar_contexto_teorico(question)
    steps.append({"node": "knowledge_retriever", "details": "Contexto teórico recuperado."})

    # Ferramenta 2: DuckDB para buscar dados de dividendos (agora como uma ferramenta)
    dados_dividendos_df = buscar_dados_de_dividendos(ticker)
    steps.append({"node": "consulta_dados_estruturados", "details": f"Encontrados {len(dados_dividendos_df)} registos de dividendos para {ticker}."})
    
    # Ferramenta 3 e 4: Busca de Notícias e Análise de Sentimento
    analise_sentimento = "Nenhuma empresa alvo identificada para busca de notícias."
    noticias = []
    if company_name:
        noticias = buscar_noticias_recentes(company_name)
        for noticia in noticias:
            print(f"Noticia: {noticia}")
        steps.append({"node": "buscar_noticias", "details": f"Encontradas {len(noticias)} notícias."})
        analise_sentimento = analisar_sentimento_noticias(noticias, llm)
        steps.append({"node": "analisar_sentimento", "details": "Análise de sentimento concluída."})
    
    # Adiciona o contexto teórico à análise de notícias para o LLM final ter tudo
    analise_final_noticias_e_teoria = f"Análise de Sentimento das Notícias:\n{analise_sentimento}\n\n---\n\nContexto Teórico Relevante dos Documentos:\n{contexto_teorico}"
    
    informacao_encontrada = not dados_dividendos_df.empty or len(noticias) > 0

    # Retorna um dicionário com as atualizações para o estado do agente
    return {
        "dados_dividendos": dados_dividendos_df,
        "analise_noticias": analise_final_noticias_e_teoria,
        "informacao_encontrada": informacao_encontrada,
        "intermediate_steps": steps
    }
