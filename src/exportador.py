# exportador.py
"""
Módulo responsável pela exportação dos dados
processados pelo sistema.

Atualmente, o módulo realiza a conversão e
armazenamento das informações no formato JSON.
"""

import json
import os


def salvar_json(nome_arquivo, dados):
    #Nota: Quero trocar essa parte de criar automaticamente e ja deixar
    #a pasta saida para remover o s.makedirs(pasta_saida, exist_ok=True)
    """
    Salva os dados processados em um arquivo JSON.

    A função cria automaticamente a pasta de saída
    caso ela não exista, gera o caminho do arquivo
    e realiza a serialização dos dados utilizando
    o módulo json.

    O arquivo é salvo com indentação para facilitar
    a leitura humana e utilizando codificação UTF-8.

    Args:
        nome_arquivo (str):
            Nome utilizado na criação do arquivo JSON.

        dados (dict | list):
            Estrutura de dados que será convertida
            para JSON.

    Returns:
        None:
            A função apenas salva o arquivo e exibe
            uma mensagem de confirmação no terminal.
    """

    pasta_saida = "../saida"

    # os.makedirs(pasta_saida, exist_ok=True)

    caminho_saida = os.path.join(
        pasta_saida,
        f"{nome_arquivo}.json"
    )

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

    print(f"\n[JSON SALVO] {caminho_saida}")
