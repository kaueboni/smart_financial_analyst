# backend/core/schemas.py
import pandas as pd
from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Define a estrutura de dados central (o "estado") do nosso agente.
    É um dicionário que carrega todas as informações através dos nós do grafo LangGraph.
    Cada nó pode ler e escrever neste estado.
    """
    # Pergunta original do utilizador
    question: str
    
    # Histórico da conversa para manter o contexto
    messages: List[BaseMessage]
    
    # Dados recolhidos pelas ferramentas
    dados_dividendos: pd.DataFrame
    analise_noticias: str
    
    # Flag de controlo para a lógica de bifurcação
    informacao_encontrada: bool
    
    # Resposta final gerada para o utilizador
    final_answer: str
    
    # Log dos passos intermédios para depuração e transparência
    intermediate_steps: List[dict]