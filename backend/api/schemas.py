from pydantic import BaseModel
from typing import List, Dict

class AgentRequest(BaseModel):
    """
    Define o contrato de dados para as requisições que chegam à nossa API.
    Garante que o frontend sempre envie os dados no formato correto.
    """
    question: str
    conversation_id: str = None

class AgentResponse(BaseModel):
    """
    Define o contrato de dados para as respostas que a nossa API envia.
    Garante que a resposta para o frontend seja sempre consistente.
    """
    final_answer: str
    intermediate_steps: List[Dict]
    
