from serpapi import GoogleSearch
from core.config import SERPAPI_API_KEY

def buscar_noticias_recentes(company_name: str) -> list:
    """
    Ferramenta 1: Busca notícias recentes sobre uma empresa usando a API do SerpApi.
    """
    if not SERPAPI_API_KEY:
        print("Aviso: Chave de API do SerpApi não configurada. A saltar a busca de notícias.")
        return []
    
    print(f"-> A executar ferramenta de busca de notícias para: {company_name}")
    params = {
        "q": f"notícias sobre as ações da empresa {company_name}",
        "tbm": "nws",  # tbm=nws para buscar na aba de Notícias
        "api_key": SERPAPI_API_KEY,
        "num": 5,      # Pega os 5 resultados mais recentes
        "gl": "br",    # Procura no Google Brasil
        "hl": "pt-br"  # Define o idioma para português do Brasil
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results.get("news_results", [])
        
        # Simplifica os resultados para conter apenas o título e um trecho
        simplified_news = [{"title": news.get("title"), "snippet": news.get("snippet")} for news in news_results]
        return simplified_news
    except Exception as e:
        print(f"  -> Erro na ferramenta de busca de notícias: {e}")
        return []

