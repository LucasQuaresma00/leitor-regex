"""
Módulo responsável pela leitura dos arquivos.
"""

import os

# Configuração base (centralizada)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DADOS = os.path.join(BASE_DIR, "dados")


def ler_arquivo(nome_arquivo: str):
    """
    Lê um arquivo da pasta 'dados' e retorna as linhas limpas.
    """
    caminho_arquivo = os.path.join(PASTA_DADOS, nome_arquivo)

    try:
        with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
            linhas = f.readlines()
        return [linha.strip() for linha in linhas if linha.strip()]  # remove linhas vazias
    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {nome_arquivo}")
        return []
    except Exception as e:
        print(f"[ERRO] Falha ao ler {nome_arquivo}: {e}")
        return []


def contar_linhas(linhas: list) -> int:
    return len(linhas)


def ler_arquivo_completo(nome_arquivo: str) -> str:
    """Retorna o conteúdo completo como string (útil para algumas extrações)."""
    linhas = ler_arquivo(nome_arquivo)
    return "\n".join(linhas)