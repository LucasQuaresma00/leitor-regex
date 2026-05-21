"""
Módulo responsável pela exportação dos resultados em JSON.
"""

import json
import os


# Configuração centralizada da pasta de saída
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_SAIDA = os.path.join(BASE_DIR, "saida")


def garantir_pasta_saida():
    """Cria a pasta de saída se ela não existir."""
    os.makedirs(PASTA_SAIDA, exist_ok=True)


def salvar_json(nome_arquivo: str, dados: dict | list):
    """
    Salva os dados em formato JSON na pasta 'saida'.
    
    Args:
        nome_arquivo (str): Nome do arquivo (sem .json)
        dados (dict | list): Dados a serem salvos
    """
    garantir_pasta_saida()

    caminho_completo = os.path.join(PASTA_SAIDA, f"{nome_arquivo}.json")

    try:
        with open(caminho_completo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        
        print(f"✅ [JSON SALVO] {nome_arquivo}.json")
    except Exception as e:
        print(f"❌ Erro ao salvar {nome_arquivo}.json: {e}")


def salvar_csv(nome_arquivo: str, dados: list[dict]):
    """Futuro: Função para salvar em CSV (opcional)."""
    pass