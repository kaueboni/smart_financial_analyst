from typing import List
from langchain_openai import ChatOpenAI

def analisar_sentimento_noticias(noticias: List[dict], llm_instance: ChatOpenAI) -> str:
    """
    Ferramenta 2: Usa um LLM para analisar o sentimento de uma lista de notícias
    do ponto de vista de um investidor.
    """
    if not noticias:
        return "Nenhuma notícia recente encontrada para análise de sentimento."

    print("-> A executar ferramenta de análise de sentimento...")
    noticias_formatadas = "\n".join([f"- Título: {n['title']}\n  Trecho: {n['snippet']}" for n in noticias])
    
    prompt = f"""
    Você é um analista financeiro experiente e cético. A sua tarefa é analisar o sentimento das seguintes notícias do ponto de vista de um investidor.
    Classifique o sentimento geral como 'Positivo', 'Negativo' ou 'Neutro'.
    Justifique a sua resposta numa única frase curta e objetiva, explicando se as notícias sugerem uma potencial valorização, desvalorização ou estabilidade para as ações da empresa.
    
    Notícias para analisar:
    {noticias_formatadas}
    """
    
    try:
        response = llm_instance.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"  -> Erro na ferramenta de análise de sentimento: {e}")
        return "Não foi possível realizar a análise de sentimento das notícias."