# relatorio.py

"""
Módulo responsável pela geração de relatórios
estatísticos com base nas ocorrências encontradas
durante o processamento dos arquivos.

O relatório organiza os dados por arquivo e
tipo de ocorrência, contabilizando registros
totais, válidos e inválidos.
"""

from collections import defaultdict


def gerar_relatorio(resultados):
    """
    Gera um relatório consolidado das ocorrências
    identificadas no sistema.

    A função percorre a lista de resultados
    processados e agrupa as informações por:
    - arquivo
    - tipo de ocorrência

    Para cada grupo são contabilizados:
    - total de ocorrências
    - quantidade de válidos
    - quantidade de inválidos

    Args:
        resultados (list[dict]):
            Lista contendo as ocorrências geradas
            durante as validações e inspeções.

            Cada ocorrência deve possuir:
            - arquivo
            - tipo
            - classificacao

    Returns:
        dict:
            Estrutura organizada contendo o resumo
            estatístico das ocorrências por arquivo.

            Exemplo:
            {
                "arquivo.csv": {
                    "email": {
                        "total": 10,
                        "validos": 8,
                        "invalidos": 2
                    }
                }
            }
    """
    
    relatorio = defaultdict(
        lambda: defaultdict(
            lambda: {
                "total": 0,
                "validos": 0,
                "invalidos": 0
            }
        )
    )

    for ocorrencia in resultados:

        arquivo = ocorrencia["arquivo"]

        tipo = ocorrencia["tipo"]

        classificacao = ocorrencia["classificacao"]

        relatorio[arquivo][tipo]["total"] += 1

        if classificacao == "valido":
            relatorio[arquivo][tipo]["validos"] += 1

        elif classificacao == "invalido":
            relatorio[arquivo][tipo]["invalidos"] += 1

    return {
        arquivo: dict(tipos)
        for arquivo, tipos in relatorio.items()
    }
