# processador.py

"""
Módulo responsável pelo fluxo principal de
processamento dos arquivos.

Este módulo centraliza:
- leitura
- identificação
- extração
- validação
- estatísticas
- relatórios

O objetivo é desacoplar a lógica de negócio
da interface de apresentação.
"""

from leitor import (
    ler_arquivo,
    contar_linhas
)

from identificador import identificar_tipo

from extrator import extrair_padroes

from validador_csv import validar_csv

from estatisticas import gerar_estatisticas

from relatorio import gerar_relatorio


def processar_arquivo(
    caminho_arquivo,
    nome_arquivo
):
    """
    Executa o processamento completo de um arquivo.

    O fluxo inclui:
    - leitura do conteúdo
    - identificação do tipo
    - extração de padrões
    - validação estrutural de CSV
    - geração de estatísticas
    - geração de relatório

    Args:
        caminho_arquivo (str):
            Caminho completo do arquivo.

        nome_arquivo (str):
            Nome do arquivo analisado.

    Returns:
        dict:
            Estrutura contendo todas as
            informações processadas.
    """

    # ==========================================
    # LEITURA
    # ==========================================

    linhas = ler_arquivo(caminho_arquivo)

    # ==========================================
    # IDENTIFICAÇÃO
    # ==========================================

    tipo = identificar_tipo(linhas)

    # ==========================================
    # EXTRAÇÃO
    # ==========================================

    resultados = extrair_padroes(
        linhas,
        nome_arquivo
    )

    # ==========================================
    # VALIDAÇÃO CSV
    # ==========================================

    if tipo == "CSV":

        inconsistencias_csv = validar_csv(
            linhas,
            nome_arquivo
        )

        resultados.extend(
            inconsistencias_csv
        )

    # ==========================================
    # ESTATÍSTICAS
    # ==========================================

    estatisticas = gerar_estatisticas(
        resultados
    )

    # ==========================================
    # RELATÓRIO
    # ==========================================

    relatorio = gerar_relatorio(
        resultados
    )

    # ==========================================
    # ESTRUTURA FINAL
    # ==========================================

    return {
        "arquivo": nome_arquivo,
        "tipo": tipo,
        "quantidade_linhas": contar_linhas(linhas),
        "estatisticas": estatisticas,
        "relatorio": relatorio,
        "ocorrencias": resultados
    }