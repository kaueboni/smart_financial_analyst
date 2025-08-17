# backend/core/tools/data_retriever.py
import pandas as pd
import duckdb

def buscar_dados_de_dividendos(ticker: str) -> pd.DataFrame:
    """
    Ferramenta 4: Busca dados estruturados sobre dividendos a partir de uma
    fonte de dados local usando DuckDB.
    """
    if not ticker:
        return pd.DataFrame()

    print(f"-> A executar ferramenta de dados para o ticker: {ticker}")
    try:
        # O caminho para o ficheiro de dados reflete a estrutura dentro do contêiner
        query = f"SELECT * FROM read_csv_auto('core/data/dividendos.csv') WHERE ticker = '{ticker}' ORDER BY data_pagamento DESC;"
        dados_df = duckdb.sql(query).fetchdf()
        return dados_df
    except Exception as e:
        print(f"  -> Erro na ferramenta de busca de dados (DuckDB): {e}")
        return pd.DataFrame()