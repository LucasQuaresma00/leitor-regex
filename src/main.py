# main.py
"""
Módulo principal do sistema de processamento
de arquivos com expressões regulares.

Este módulo coordena todo o fluxo da aplicação:
- leitura dos arquivos
- identificação do tipo
- extração de padrões
- validação
- geração de estatísticas
- criação de relatórios
- exportação dos resultados em JSON
"""

import os

from leitor import (
    ler_arquivo,
    contar_linhas,
    identificar_tipo
)

from extrator import extrair_padroes
from exportador import salvar_json
from estatisticas import gerar_estatisticas
from validador_csv import validar_csv
from relatorio import gerar_relatorio


PASTA_DADOS = "../dados"

ARQUIVOS = [
    "01_atendimentos_bagunçados.txt",
    "02_logs_mistos.log",
    "03_mensagens_chat.txt",
    "04_exportacao_suja.csv"
]


def mostrar_amostra(linhas, quantidade=3):
    """
    Exibe uma pequena amostra do conteúdo
    do arquivo no terminal.

    Args:
        linhas (list[str]):
            Lista contendo as linhas do arquivo.

        quantidade (int, optional):
            Quantidade máxima de linhas exibidas.
            Valor padrão: 3.

    Returns:
        None:
            A função apenas imprime informações
            no terminal.
    """
    print("\n--- AMOSTRA ---")

    for linha in linhas[:quantidade]:
        print(linha)


def mostrar_resultados(resultados, limite=10):
    """
    Exibe os padrões encontrados durante
    o processamento do arquivo.

    Args:
        resultados (list[dict]):
            Lista contendo as ocorrências
            identificadas.

        limite (int, optional):
            Quantidade máxima de resultados
            exibidos no terminal.
            Valor padrão: 10.

    Returns:
        None:
            A função apenas imprime informações
            no terminal.
    """

    print("\n--- PADRÕES ENCONTRADOS ---")

    print(f"\nTotal de ocorrências: {len(resultados)}")
    
    for ocorrencia in resultados[:limite]:

        print(
            f"[{ocorrencia['tipo'].upper()}] "
            f"{ocorrencia['valor']} "
            f"-> {ocorrencia['classificacao']}"
        )


def main():
    """
    Executa o fluxo principal do sistema.

    O processamento realizado inclui:
    - leitura dos arquivos
    - identificação do tipo de conteúdo
    - exibição de amostras
    - extração de padrões utilizando regex
    - validação estrutural de arquivos CSV
    - geração de estatísticas
    - geração de relatórios
    - exportação dos resultados em JSON

    Returns:
        None:
            A função executa o sistema completo
            e exibe os resultados no terminal.
    """
    
    print("=" * 60)
    print("PROCESSADOR DE ARQUIVOS COM REGEX")
    print("=" * 60)
    todos_resultados = []

    for nome_arquivo in ARQUIVOS:

        caminho = os.path.join(PASTA_DADOS, nome_arquivo)

        linhas = ler_arquivo(caminho)

        tipo = identificar_tipo(nome_arquivo)

        print(f"\nArquivo: {nome_arquivo}")
        print(f"Tipo: {tipo}")
        print(f"Quantidade de linhas: {contar_linhas(linhas)}")

        # Mostrar amostra
        mostrar_amostra(linhas)

        # Extrair padrões
        resultados = extrair_padroes(linhas, nome_arquivo)
        todos_resultados.extend(resultados)

        # ======================================
        # VALIDAR CSV
        # ======================================

        if tipo == "CSV":

            inconsistencias_csv = validar_csv(
                linhas,
                nome_arquivo
            )

            resultados.extend(
                inconsistencias_csv
            )


        # Mostrar resultados
        mostrar_resultados(resultados)

        # Estrutura JSON
        estrutura_json = {
            "arquivo": nome_arquivo,
            "tipo": tipo,
            "quantidade_linhas": contar_linhas(linhas),
            "resultados": resultados
        }

        # Nome do arquivo de saída
        nome_saida = nome_arquivo.split(".")[0]

        # Salvar JSON
        salvar_json(nome_saida, estrutura_json)

    print("\n" + "=" * 60)
    print("ESTATÍSTICAS GERAIS")
    print("=" * 60)

    estatisticas = gerar_estatisticas(
    todos_resultados
    )

    # ======================================
    # RELATÓRIO
    # ======================================

    relatorio = gerar_relatorio(
        todos_resultados
    )

    salvar_json(
        "relatorio",
        relatorio
    )


    # ======================================
    # JSON GERAL
    # ======================================

    estrutura_geral = {
        "estatisticas": estatisticas,
        "ocorrencias": todos_resultados
    }

    salvar_json(
        "resultados_gerais",
        estrutura_geral
    )


    # ======================================
    # TOTAL POR TIPO
    # ======================================

    print("\n--- TOTAL POR TIPO ---")

    for tipo, total in estatisticas[
        "total_por_tipo"
    ].items():

        print(f"{tipo.upper()}: {total}")

    # ======================================
    # VALIDOS / INVALIDOS
    # ======================================

    print("\n--- VÁLIDOS / INVÁLIDOS ---")

    for tipo, dados in estatisticas[
        "validos_invalidos"
    ].items():

        print(f"\n{tipo.upper()}")

        for status, quantidade in dados.items():

            print(f"  {status}: {quantidade}")

    # ======================================
    # DISTRIBUIÇÃO POR ARQUIVO
    # ======================================

    print("\n--- DISTRIBUIÇÃO POR ARQUIVO ---")

    for arquivo, dados in estatisticas[
        "distribuicao_arquivos"
    ].items():

        print(f"\n{arquivo}")

        for tipo, quantidade in dados.items():

            print(f"  {tipo}: {quantidade}")



if __name__ == "__main__":
    main()
