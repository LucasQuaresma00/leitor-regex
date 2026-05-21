"""
Módulo responsável pelo fluxo completo de processamento
de cada arquivo. Atua como orquestrador.
"""

from leitor import ler_arquivo, contar_linhas
from identificador import identificar_tipo
from extrator import extrair_padroes
from validador_csv import validar_csv
from estatisticas import gerar_estatisticas
from relatorio import gerar_relatorio


def processar_arquivo(caminho_arquivo: str, nome_arquivo: str) -> dict:
    """
    Executa o processamento completo de um único arquivo.
    """

    # Leitura
    linhas = ler_arquivo(caminho_arquivo)

    # Identificação
    tipo_arquivo = identificar_tipo(linhas)

    print(f"   Tipo detectado: {tipo_arquivo}")
    print(f"   Linhas: {contar_linhas(linhas)}")

    # Extração de padrões
    ocorrencias = extrair_padroes(linhas, nome_arquivo)

    # Validação específica para CSV
    if tipo_arquivo == "CSV":
        inconsistencias = validar_csv(linhas, nome_arquivo)
        ocorrencias.extend(inconsistencias)
        print(f"   Inconsistências CSV encontradas: {len(inconsistencias)}")

    # Estatísticas e Relatório
    estatisticas = gerar_estatisticas(ocorrencias)
    relatorio = gerar_relatorio(ocorrencias)

    return {
        "arquivo": nome_arquivo,
        "tipo": tipo_arquivo,
        "quantidade_linhas": contar_linhas(linhas),
        "linhas": linhas,                    # útil para amostra
        "ocorrencias": ocorrencias,
        "estatisticas": estatisticas,
        "relatorio": relatorio
    }