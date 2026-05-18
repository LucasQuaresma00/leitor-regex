# leitor.py
"""
Módulo responsável pela leitura e identificação
de arquivos utilizados no sistema de inspeção.
"""

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DADOS = os.path.join(BASE_DIR, "dados")


def ler_arquivo(nome_arquivo):
    """
    Lê um arquivo localizado na pasta de dados do projeto.

    A função monta o caminho absoluto do arquivo com base
    na pasta 'dados', realiza a leitura do conteúdo e
    retorna uma lista contendo cada linha sem espaços
    extras ou quebras de linha.

    Args:
        nome_arquivo (str): Nome do arquivo que será lido.

    Returns:
        list[str]: Lista contendo as linhas do arquivo já tratadas.

    Raises:
        FileNotFoundError:
            Caso o arquivo não exista, a função exibe
            uma mensagem de erro e retorna uma lista vazia.
    """

    caminho_arquivo = os.path.join(PASTA_DADOS, nome_arquivo)

    try:

        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        return [linha.strip() for linha in linhas]

    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {caminho_arquivo}")
        return []


def contar_linhas(linhas):
    """
    Conta a quantidade de linhas presentes em uma lista.

    Args:
        linhas (list): Lista contendo as linhas do arquivo.

    Returns:
        int: Quantidade total de linhas.
    """
     
    return len(linhas)


def identificar_tipo(nome_arquivo):
    """
    Identifica o tipo do arquivo com base em sua extensão
    ou nome.

    Regras utilizadas:
    - '.csv' -> CSV
    - '.log' -> LOG
    - arquivos contendo 'chat' -> CHAT
    - demais casos -> TEXTO LIVRE

    Args:
        nome_arquivo (str): Nome do arquivo analisado.

    Returns:
        str: Tipo identificado do arquivo.
    """

    extensao = os.path.splitext(nome_arquivo)[1]

    if extensao == ".csv":
        return "CSV"

    if extensao == ".log":
        return "LOG"

    if "chat" in nome_arquivo.lower():
        return "CHAT"

    return "TEXTO LIVRE"
